import os

os.environ["PYTHON_JULIACALL_EXE"] = "/home/lazar-zubovic/julia-1.9.4/bin/julia"
os.environ["PYTHON_JULIACALL_PROJECT"] = "/home/lazar-zubovic/Desktop/LPRS2_2026/DAQ_Zynq_GUI/SW/Portal/app"

from juliacall import Main as jl

import numpy as np
import matplotlib.pyplot as plt

jl.include("dac_backend_portal.jl")

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
    return samples / ((1 << BITS) - 1) * VREF_MV

def t_axis(n):
    return np.arange(n) / F_SMPL * 1e6  # us

def plot_waveform(samples, title="DAC waveform"):

    mv = dac_to_mv(samples)

    t = t_axis(len(samples))

    print(f"Min: {mv.min():.2f} mV")
    print(f"Max: {mv.max():.2f} mV")

    plt.figure(figsize=(12, 6))

    plt.plot(
        t,
        mv,
        marker='o',
        markersize=3,
        linewidth=1.5,
        label="DAC output"
    )

    plt.axhline(
        0,
        linestyle='--',
        linewidth=1,
        label="0 mV"
    )

    plt.axhline(
        VREF_MV / 2,
        linestyle='--',
        linewidth=1,
        label="VREF/2"
    )

    plt.axhline(
        VREF_MV,
        linestyle='--',
        linewidth=1,
        label="VREF"
    )

    plt.title(title)
    plt.xlabel("Time [us]")
    plt.ylabel("Voltage [mV]")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


#------------MAIN----------------
VREF_MV = 2500.0
BITS = 16
F_SMPL = 118000

samples = generate_sine()

plot_waveform(
    samples,
    title="DAC PMOD — Sine"
)

jl.send_samples(jl.Vector[jl.UInt32](samples.tolist()))