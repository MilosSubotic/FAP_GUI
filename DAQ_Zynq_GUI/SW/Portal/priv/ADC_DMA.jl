export 
	ADC_DMA,
	cnv_trig,
	cnv_progress,
	write_buf,
	read_buf!,
	write_word,
	read_word


push!(LOAD_PATH, joinpath(@__DIR__))
unique!(LOAD_PATH)
import adc_lvds_cfg


struct ADC_DMA
	portal::Portal_Wormhole
	gate::portal_gate_t
end

function write(adc::ADC_DMA, addr::UInt32, data::Array)
	write(adc.portal, adc.gate, addr, data)
end

function read!(adc::ADC_DMA, addr::UInt32, data::Array)
	read!(adc.portal, adc.gate, addr, data)
end


function cnv_trig(adc::ADC_DMA, samples::Int)
	write(adc, adc_lvds_cfg.CNV_TRIG_SIZE_ADDR, [Int32(samples)])
end

function cnv_progress(adc::ADC_DMA)::Int
	progress = Int32[-1]
	read!(adc,  adc_lvds_cfg.CNV_PROGRESS_ADDR, progress)
	return progress[1]
end

function write_buf(adc::ADC_DMA, samples::Vector{UInt32})
	write(adc, adc_lvds_cfg.BUF_ADDR, samples)
end

function read_buf!(adc::ADC_DMA, samples::Vector{UInt32})
	read!(adc, adc_lvds_cfg.BUF_ADDR, samples)
end

function write_word(adc::ADC_DMA, addr_W, val)
	data = UInt32[UInt32(val)]
	write(
		adc.portal,
		adc.gate,
		UInt32(addr_W*sizeof(UInt32)),
		data
	)
end

function read_word(adc::ADC_DMA, addr_W, t::Type = UInt32)
	data = zeros(UInt32, 1)
	read!(
		adc.portal,
		adc.gate,
		UInt32(addr_W*sizeof(UInt32)),
		data
	)
	return convert(t, data[1])
end
