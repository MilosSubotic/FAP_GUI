# adc_lvds_backend.py
# Only this file touches juliacall for the ADC_LVDS path.
# Julia bootstrap (env vars, jl.include) happens ONCE in app.py, before this
# module is imported — this file assumes juliacall is already usable.

import os
from pathlib import Path
from juliacall import Main as jl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
jl.include(os.path.join(THIS_DIR, "adc_lvds_backend.jl"))   


def capture(ch: int, n: int):
    """Blocking. Must be called on the Qt main thread only."""
    samples = jl.capture(n)
    import numpy as np
    return np.array(samples, dtype=np.float64) 

def start(ch: int = 1):
    jl.start(ch)

def stop(ch: int = 1):
    jl.stop(ch)

def is_running(ch: int = 1) -> bool:
   return jl.is_running(ch)

def t_axis(f_smpl: float, record_length: int):
    import numpy as np
    return np.array(jl.t_axis(f_smpl, record_length), dtype=np.float64)