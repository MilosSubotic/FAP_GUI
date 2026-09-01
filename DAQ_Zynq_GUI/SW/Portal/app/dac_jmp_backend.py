from juliacall import Main as jl
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

from juliacall import Main as jl

import numpy as np

jl.include(os.path.join(THIS_DIR, "dac_jmp_backend.jl"))


def set_cfg(
        t_pump,
        t_probe,
        f_2larmor,
        V_pump1,
        V_pump2,
        V_probe):
    
    print("===== DAC_JMP CONFIG =====")
    print("t_pump     =", t_pump)
    print("t_probe    =", t_probe)
    print("f_2larmor  =", f_2larmor)
    print("V_pump1    =", V_pump1)
    print("V_pump2    =", V_pump2)
    print("V_probe    =", V_probe)

    jl.set_cfg_py(
        t_pump,
        t_probe,
        f_2larmor,
        V_pump1,
        V_pump2,
        V_probe
    )


def probe():
    return bool(jl.probe_py())