
function set_cfg_py(
    t_pump,
    t_probe,
    f_2larmor,
    V_pump1,
    V_pump2,
    V_probe
)
    println("SET_CFG_PY ENTER")

    dac = DAC_Jmp(get_portal(), PG_DAC_JMP)

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
    catch e
        println("SET_CFG_PY ERROR: $e")
        rethrow()   
    end

    println("SET_CFG_PY EXIT")
end

function probe_py()

    dac = DAC_Jmp(get_portal(), PG_DAC_JMP)

    try
        return probe(dac)
    catch e
        println("PROBE_PY ERROR: $e")
    end
end
