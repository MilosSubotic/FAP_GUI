#!/usr/bin/env julia

f_smpl = 5000000
ms_to_smpl(ms) = round(Int, ms/1000*f_smpl)

N_smpls = Int(1 << 16)# 256k samples, ~2.1s at 5MHz
1

plot_between = 1:round(Int, 1 * N_smpls)  # show 
#plot_between = 1:round(Int, 0.003 * f_smpl)  # show 3ms = 3 periods of 1kHz
#plot_between = 1:Int(1 << 15) # Around of 1 period.
#plot_between = ms_to_smpl(38):ms_to_smpl(73) # Probing signal
#plot_between = ms_to_smpl(1):ms_to_smpl(2) # Probing signal

include(joinpath(@__DIR__, "..", "priv", "adc_lvds_cfg.jl"))
    
function capture(n::Int)
	raw_samples = zeros(UInt32, n)

    adc = ADC_DMA(get_portal(), PG_ADC_DMA)
    try
		cnv_trig(adc, n)

		while true
			sleep(0.1)
			progress = cnv_progress(adc)
			println("Progress $progress%")
			if progress == 100
				break
			end
		end

		read_buf!(adc, raw_samples)
		println("raw min/max: ", minimum(raw_samples), " ", maximum(raw_samples))
    
	catch e
		println("Capture error: $e")
		rethrow()          # let caller know it failed
	end

	BITS = 18

    unscaled = zeros(Int32, n)
    unscaled = Int32[
	reinterpret(Int32, ts << (32-BITS)) >> (32-BITS) for ts in raw_samples
	]
	samples = zeros(UInt32, n)
    scale = 15/(1 << BITS)
    samples = unscaled.*scale

    return samples         # <-- here: returned on success
end

function start(ch::Int = 1)

    adc = ADC_DMA(get_portal(), PG_ADC_DMA)
	write_word(adc, adc_lvds_cfg.RM_en, 1)
end

function stop(ch::Int = 1)

	adc = ADC_DMA(get_portal(), PG_ADC_DMA)
	write_word(adc, adc_lvds_cfg.RM_en, 0)
end

function is_running(ch::Int = 1)::Bool

    adc = ADC_DMA(get_portal(), PG_ADC_DMA)
	val = zeros(UInt32, 1)
	read_word(adc, adc_lvds_cfg.RM_en, val)
    return val[1] != 0
end

function t_axis(f_smpl::Float64, record_length::Int)
	T = 1/f_smpl
	t = collect(0:record_length-1) .* T
	return t
end

#


