#!/usr/bin/env julia


const ADC_PMOD_VREF_MV = 3300.0
const ADC_PMOD_BITS = 12
const F_SMPL = 118000

# ── Helpers ───────────────────────────────────────────────────────────────────

adc_to_mv(sample::Integer) = sample * ADC_PMOD_VREF_MV / ((1 << ADC_PMOD_BITS) - 1)
t_axis(n) = collect(0:n-1) ./ F_SMPL .* 1000  # ms

include(joinpath(@__DIR__, "..", "priv", "adc_pmod_ctrl_cfg.jl"))
    
function capture(ch::Int, n::Int)

    if ch == 0
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_0)
    elseif ch == 1
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_1)
    else
        error("Channel must be 0 or 1") 
    end
    
    samples = zeros(UInt32, n)
    try
        cnv_trig(adc, ch, n)
        while true
            sleep(0.1)
            progress = cnv_progress(adc)
            println("Progress: $progress%")
            progress == 100 && break
        end
        read_buf!(adc, ch, samples)
    catch e
        println("Capture error: $e")
        rethrow()          # let caller know it failed
    end
    return adc_to_mv(samples)         # <-- here: returned on success
end

function is_running(ch::Int)::Bool
    
    if ch == 0
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_0)
    elseif ch == 1
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_1)
    else
        error("Channel must be 0 or 1") 
    end
    
    return read_word(adc, adc_pmod_ctrl_cfg.RM_ch_enable) & (1 << ch) != 0
end

function start(ch::Int)
    println("Starting ADC_PMOD capture on channel $ch...")

    if ch == 0
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_0)
    elseif ch == 1
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_1)
    else
        error("Channel must be 0 or 1")
    end

    println("Dummy function, already started in capture()")
end

function stop(ch::Int)
    println("Stopping ADC_PMOD capture on channel $ch...")
    if ch == 0
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_0)
    elseif ch == 1
        adc = ADC_PMOD_CTRL(get_portal(), PG_ADC_PMOD_1)
    else
        error("Channel must be 0 or 1")
    end

    write_word(adc, adc_pmod_ctrl_cfg.RM_ch_enable, 0)
    
end
