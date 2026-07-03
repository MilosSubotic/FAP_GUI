include("../Portal_inc.jl")
include(joinpath(@__DIR__, "..", "..", "..", "..", "globalUSBvariables.jl"))

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

    if dac_pmod_portal[] === nothing
        dac_pmod_portal[] = Portal_Wormhole(BACKEND_USB, GATE)
    end

    portal = dac_pmod_portal[]
    dac = DAC_PMOD_CTRL(portal)

    try

        while dma_write_done(dac) != 1
            sleep(0.01)
        end

        write_buf(dac, samples)

        cpu_write_done(dac)

        cnv_trig(dac, length(samples))

        for i in 1:20

            sleep(0.1)

            progress = cnv_progress(dac)

            println("Progress: $progress")

        end

    finally
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