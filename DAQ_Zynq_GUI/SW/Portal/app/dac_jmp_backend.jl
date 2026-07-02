include(joinpath(@__DIR__, "..", "Portal_inc.jl"))

const GATE = PG_DAC_JMP

portal = Portal_Wormhole(BACKEND_USB, GATE)
dac = DAC_Jmp(portal)

function set_cfg_py(
    t_pump,
    t_probe,
    f_2larmor,
    V_pump1,
    V_pump2,
    V_probe
)
    println("SET_CFG_PY ENTER")

    
    set_cfg!(
        dac,
        t_pump=t_pump,
        t_probe=t_probe,
        f_2larmor=f_2larmor,
        V_pump1=V_pump1,
        V_pump2=V_pump2,
        V_probe=V_probe
    )

    println("SET_CFG_PY EXIT")
end


function probe_py()
    return probe(dac)
end