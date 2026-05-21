include("../Portal_inc.jl")

const GATE = PG_ADC_PMOD_0

function capture_samples(ch::Int, n::Int)

    portal = Portal_Wormhole(BACKEND_USB, GATE)
    adc = ADC_PMOD_CTRL(portal)

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

    finally
        close(adc.portal)
    end

    return samples
end