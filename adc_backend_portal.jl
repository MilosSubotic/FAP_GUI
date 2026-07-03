include("DAQ_Zynq_GUI/SW/Portal/Portal_inc.jl")
include(joinpath(@__DIR__, "globalUSBvariables.jl"))

const GATE = PG_ADC_PMOD_0

function capture_samples(ch::Int, n::Int)

    println("A")

    if adc_portal[] === nothing
        println("B")
        adc_portal[] = Portal_Wormhole(BACKEND_USB, GATE)
        println("C")
    end

    println("D")

    portal = adc_portal[]

    println("E")

    adc = ADC_PMOD_CTRL(portal)

    println("F")

    samples = zeros(UInt32, n)

    println("G")

    try
        println("H")

        cnv_trig(adc, ch, n)

        println("I")

        while true
            sleep(0.1)

            progress = cnv_progress(adc)
            println("Progress: $progress%")

            progress == 100 && break
        end

        println("J")

        read_buf!(adc, ch, samples)

        println("K")

    finally
        println("L")
        close(adc.portal)
        println("M")
        adc_portal[] = nothing
    end

    println("N")

    return samples
end