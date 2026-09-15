
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

function mon_probe_py()

    dac = DAC_Jmp(get_portal(), PG_DAC_JMP)

    try
        while probe(dac);  sleep(0.0005); end   # wait FE
        while !probe(dac); sleep(0.0005); end   # wait RE
        t_probe_start = time()
        while probe(dac);  sleep(0.0005); end   # wait FE
        t_probe_end = time()

		t_probe_ms = (t_probe_end - t_probe_start)*1e3

		println("T_PROBE_MS = $t_probe_ms")
    catch e
        println("MON_PROBE_PY ERROR: $e")
    end
end
