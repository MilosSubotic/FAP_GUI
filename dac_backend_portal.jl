include(joinpath(@__DIR__,
    "DAQ_Zynq_GUI",
    "SW",
    "Portal",
    "Portal_inc.jl"))

const GATE = PG_DAC_PMOD_0

const VREF_MV = 2500.0
const BITS = 16
const F_SMPL = 118000

mv_to_dac(mv::Real)::UInt32 =
    UInt32(round(clamp(mv, 0, VREF_MV) / VREF_MV * ((1 << BITS) - 1)))

function gen_sine(
    n::Int,
    periods::Int = 1,
    Vpp::Float64 = VREF_MV,
    Vcenter::Float64 = VREF_MV / 2
)

    amp_mv = clamp(Vpp / 2, 0.0, VREF_MV / 2)
    amp_code = amp_mv / VREF_MV * ((1 << BITS) - 1)

    mid_code = mv_to_dac(Vcenter)

    [
        UInt32(round(
            mid_code +
            amp_code * sin(2π * periods * (i-1) / n)
        ))
        for i in 1:n
    ]
end

function send_samples(samples::Vector{UInt32})

    println("D0")

    portal = Portal_Wormhole(BACKEND_USB, GATE)

    println("D1")

    dac = DAC_PMOD_CTRL(portal)

    println("D2")

    try

        dma = dma_write_done(dac)

        println("DMA = ", dma)

        if dma == 1

            println("Writing buffer")

            write_buf(dac, samples)

            println("CPU done")

            cpu_write_done(dac)

        else

            println("DMA not ready")

        end

        println("Triggering")

        cnv_trig(dac, length(samples))

        println("Samples count = ", length(samples))

        for i in 1:30
            sleep(0.1)

            p = cnv_progress(dac)
            d = dma_write_done(dac)

            println("progress=$p dma=$d")
        end

        println("DAC playback complete.")

    finally

        println("Closing USB...")

        close(dac.portal)

    end

    return true

end

function make_sine(
    n::Int = 1024,
    periods::Int = 1,
    Vpp::Float64 = 1000.0,
    Vcenter::Float64 = 1250.0
)

    return gen_sine(n, periods, Vpp, Vcenter)
end

function play_sine(
    n::Int = 1024,
    periods::Int = 1,
    Vpp::Float64 = 1000.0,
    Vcenter::Float64 = 1250.0
)

    samples = gen_sine(n, periods, Vpp, Vcenter)

    send_samples(samples)

    return samples
end