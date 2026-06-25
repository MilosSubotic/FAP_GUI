include(joinpath(@__DIR__, "..", "Portal_inc.jl"))

const GATE = PG_DAC_JMP

function set_cfg_py(
    t_pump,
    t_probe,
    f_2larmor,
    V_pump1,
    V_pump2,
    V_probe
)
    println("SET_CFG_PY ENTER")
    portal = Portal_Wormhole(BACKEND_USB, GATE)
    dac = DAC_Jmp(portal)

    try
        set_cfg!(
            dac,
            t_pump=t_pump,
            t_probe=t_probe,
            f_2larmor=f_2larmor,
            V_pump1=V_pump1,
            V_pump2=V_pump2,
            V_probe=V_probe
        )

    finally
        close(portal)
    end
    println("SET_CFG_PY EXIT")
end


function probe_py()

    portal = Portal_Wormhole(BACKEND_USB, GATE)
    dac = DAC_Jmp(portal)

    try
        return probe(dac)

    finally
        close(portal)
    end
end