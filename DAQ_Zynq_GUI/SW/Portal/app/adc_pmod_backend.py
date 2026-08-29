# adc_pmod_backend.py
# Only this file touches juliacall for the ADC_PMOD path.
# Julia bootstrap (env vars, jl.include) happens ONCE in app.py, before this
# module is imported — this file assumes juliacall is already usable.

import os
from pathlib import Path
from juliacall import Main as jl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
jl.include(os.path.join(THIS_DIR, "adc_pmod_backend.jl"))   # renamed from adc_backend_portal.jl

VREF = 3.3
BITS = 12
F_SMPL = 118000          # the ONE real, fixed rate for this hardware — not user-selectable

def capture(ch: int, n: int):
    """Blocking. Must be called on the Qt main thread only."""
    samples = jl.capture(ch, n)
    import numpy as np
    return np.array(samples, dtype=np.uint32)

def is_running(ch: int) -> bool:
    return jl.is_running(ch)

def start(ch: int):
    print(f"Starting ADC_PMOD capture on channel {ch}...")
    jl.start(ch)

def stop(ch: int):
    print(f"Stopping ADC_PMOD capture on channel {ch}...")
    jl.stop(ch)

def t_axis(n):
    import numpy as np
    return np.arange(n) / F_SMPL * 1000.0