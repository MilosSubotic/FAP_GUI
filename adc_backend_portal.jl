include("/home/lazar-zubovic/Desktop/FAP_GUI/DAQ_Zynq_GUI/SW/Portal/Portal_inc.jl")

const GATE = PG_ADC_PMOD_0

function capture_samples(ch::Int, n::Int)

    println("J1")

    portal = Portal_Wormhole(BACKEND_USB, GATE)

    println("J2")

    adc = ADC_PMOD_CTRL(portal)

    println("J3")

    samples = zeros(UInt32, n)

    try
        println("J4 before cnv_trig")

        cnv_trig(adc, ch, n)

        println("J5 after cnv_trig")

        while true
            sleep(0.1)

            progress = cnv_progress(adc)
            println("Progress: $progress%")

            progress == 100 && break
        end

        println("J6 before read_buf")

        read_buf!(adc, ch, samples)

        println("J7 after read_buf")

    finally
        println("J8 closing")
        close(adc.portal)
    end

    println("J9 return")

    return samples
end