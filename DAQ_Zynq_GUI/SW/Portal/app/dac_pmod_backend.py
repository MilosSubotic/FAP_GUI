import os
from pathlib import Path

from juliacall import Main as jl

import numpy as np
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

jl.include(os.path.join(THIS_DIR, "dac_pmod_backend.jl"))

VREF_MV = 2500.0
DAC_BITS = 16
F_SMPL = 118000

def generate_sine():
    samples = np.array(
        jl.make_sine(
            4096,
            4,
            1000.0,
            1250.0
        ),
        dtype=np.uint32
    )

    return samples

def dac_to_mv(samples):
    return samples / ((1 << DAC_BITS) - 1) * VREF_MV

def send_samples(samples):
    jl.send_samples(jl.Vector[jl.UInt32](samples.tolist()))

def waveform_to_dac(samples_v):
    samples_v = np.asarray(samples_v, dtype=float)

    # Pomeri bipolaran signal oko sredine DAC opsega
    samples_v = samples_v + 1.25

    return np.clip(
        samples_v / 2.5 * ((1 << DAC_BITS) - 1),
        0,
        (1 << DAC_BITS) - 1
    ).astype(np.uint32)

def t_axis(n):
    return np.arange(n) / F_SMPL * 1e6  # us




