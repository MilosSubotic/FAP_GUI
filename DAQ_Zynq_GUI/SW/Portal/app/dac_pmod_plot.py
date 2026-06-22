import os
import shutil
from pathlib import Path

def find_project_root(start: Path):
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Project root not found")

current = Path(__file__).resolve()
project_root = find_project_root(current)

julia_path = shutil.which("julia")
if julia_path:
    os.environ["PYTHON_JULIACALL_EXE"] = julia_path
else:
    raise FileNotFoundError("Could not find 'julia' in the system PATH.")

os.environ["PYTHON_JULIACALL_PROJECT"] = str(project_root) + "/DAQ_Zynq_GUI/SW/Portal/app"

from juliacall import Main as jl

import numpy as np
import matplotlib.pyplot as plt

jl.include("dac_backend_portal.jl")

VREF_MV = 2500.0
BITS = 16
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
    return samples / ((1 << BITS) - 1) * VREF_MV

def waveform_to_dac(samples_v):
    samples_v = np.asarray(samples_v, dtype=float)

    # Pomeri bipolaran signal oko sredine DAC opsega
    samples_v = samples_v + 1.25

    return np.clip(
        samples_v / 2.5 * ((1 << 16) - 1),
        0,
        (1 << 16) - 1
    ).astype(np.uint32)

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

if __name__ == "__main__":
    

    samples = generate_sine()

    plot_waveform(
        samples,
        title="DAC PMOD — Sine"
    )

    jl.send_samples(jl.Vector[jl.UInt32](samples.tolist()))