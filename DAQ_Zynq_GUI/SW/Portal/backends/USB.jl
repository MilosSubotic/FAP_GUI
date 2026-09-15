

USB_VENDOR_ID = 0x03FD
USB_PRODUCT_ID = 0x0000
USB_INTERFACE = 0
USB_ENDPOINT = 1
USB_TIMEOUT = 1000 # [ms]

install_if_not_installed(["libusb_jll"])

using libusb_jll

LIBUSB_ENDPOINT_IN  = 0x80
LIBUSB_ENDPOINT_OUT = 0x00
LIBUSB_ERROR_TIMEOUT = -7

# host-to-device.
ENDPOINT_TX = LIBUSB_ENDPOINT_OUT | USB_ENDPOINT
# device-to-host.
ENDPOINT_RX = LIBUSB_ENDPOINT_IN | USB_ENDPOINT

const LIBUSB_ERROR_NAMES = Dict(
    0   => "LIBUSB_SUCCESS",
    -1  => "LIBUSB_ERROR_IO (input/output error)",
    -2  => "LIBUSB_ERROR_INVALID_PARAM (invalid parameter)",
    -3  => "LIBUSB_ERROR_ACCESS (access denied, insufficient permissions)",
    -4  => "LIBUSB_ERROR_NO_DEVICE (device not found / has been disconnected)",
    -5  => "LIBUSB_ERROR_NOT_FOUND (entity not found)",
    -6  => "LIBUSB_ERROR_BUSY (resource busy)",
    -7  => "LIBUSB_ERROR_TIMEOUT (transfer timed out)",
    -8  => "LIBUSB_ERROR_OVERFLOW (overflow)",
    -9  => "LIBUSB_ERROR_PIPE (pipe error / endpoint stalled)",
    -10 => "LIBUSB_ERROR_INTERRUPTED (system call interrupted)",
    -11 => "LIBUSB_ERROR_NO_MEM (insufficient memory)",
    -12 => "LIBUSB_ERROR_NOT_SUPPORTED (operation not supported on this platform)",
    -99 => "LIBUSB_ERROR_OTHER (unknown/other error)",
)

libusb_error_string(code::Integer) =
    get(LIBUSB_ERROR_NAMES, code, "LIBUSB_ERROR_UNKNOWN (unrecognized code $code)")

mutable struct USB
	ctx::Ptr{Cvoid}
	handle::Ptr{Cvoid}
end


function USB()
	usb = USB(
		Ptr{Cvoid}(),
		C_NULL
	)

	r = ccall(
		(:libusb_init, libusb),
		Cint,
		(Ptr{Ptr{Cvoid}},),
		Ref(usb.ctx)
	)
	if r != 0
		throw("libusb_init() failed with $(r)!")
	end

	usb.handle = ccall(
		(:libusb_open_device_with_vid_pid, libusb),
		Ptr{Cvoid},
		(Ptr{Cvoid}, UInt16, UInt16),
		usb.ctx,
		USB_VENDOR_ID,
		USB_PRODUCT_ID
	)
	if usb.handle == C_NULL
		@ccall perror("Device not found"::Cstring)::Cvoid
		throw("libusb_open_device_with_vid_pid(): failed!")
	end

	r = ccall(
		(:libusb_claim_interface, libusb),
		Cint,
		(Ptr{Cvoid}, Cint),
		usb.handle,
		USB_INTERFACE
	)
	if r < 0
		throw("libusb_claim_interface(): failed with $(r)!")
	end

	if false
		#FIXME
		finalizer(
			function(usb::USB)
				#println("finilizing USB...")
				close(usb)
			end,
			usb
		)
	end

	return usb
end


function _bulk_transfer(usb, size, ptr, enpoint_tx_rx)

	transfered = Cint[0]
	r = ccall(
		(:libusb_bulk_transfer, libusb),
		Cint,
		(Ptr{Cvoid}, Cuchar, Ptr{Cuchar}, Cint, Ptr{Cint}, Cuint),
		usb.handle,
		enpoint_tx_rx,
		ptr,
		UInt32(size),
		transfered,
		USB_TIMEOUT
	)
	if r != 0
		throw("libusb_bulk_transfer(): failed with $(r) ($(libusb_error_string(r)))!")
	else
		if transfered[1] != size
			#throw("libusb_bulk_transfer(): Not all transfered!")
		end
	end
end

function write(usb::USB, size, ptr::Ptr{UInt8})
	@assert size <= 8+PORTAL_MAX_PAYLOAD_SIZE
	_bulk_transfer(usb, size, ptr, ENDPOINT_TX)
end

function read!(usb::USB, size, ptr::Ptr{UInt8})
	@assert size <= PORTAL_MAX_PAYLOAD_SIZE
	_bulk_transfer(usb, size, ptr, ENDPOINT_RX)
end

function close(usb::USB)
	# Guard against double-close
    if usb.handle == C_NULL
        return
    end
	#println("Closing USB...")

	ccall(
		(:libusb_close, libusb),
		Cvoid,
		(Ptr{Cvoid},),
		usb.handle
	)
	usb.handle = C_NULL
	ccall(
		(:libusb_exit, libusb),
		Cvoid,
		(Ptr{Cvoid},),
		usb.ctx
	)
	usb.ctx = C_NULL
end

