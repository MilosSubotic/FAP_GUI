import time
import numpy as np
import matplotlib.pyplot as plt

#Za pravilno pozivanje julie
import os

os.environ["PYTHON_JULIACALL_EXE"] = "/home/lazar-zubovic/julia-1.9.4/bin/julia"
os.environ["PYTHON_JULIACALL_PROJECT"] = "/home/lazar-zubovic/Desktop/LPRS2_2026/DAQ_Zynq_GUI/SW/Portal/app"

from juliacall import Main as jl
jl.include("adc_backend_portal.jl")

PG_ADC_PMOD_0 = 6
PG_ADC_PMOD_1 = 7

GATE      = PG_ADC_PMOD_0
N         = 1 << 8      #TREBA KAO PARAMETAR
VREF      = 3.3
BITS      = 12
F_SMPL    = 118000      
LIVE_LOOP = True

def adc_to_mv(sample):
    return sample * VREF * 1000 / ((1 << BITS) - 1)

def t_axis(n):
    return np.arange(n) / F_SMPL * 1000.0

def capture(ch, n):
    # Poziv Julia funkcije
    samples = jl.capture_samples(ch, n)

    # Julia Vector -> NumPy
    return np.array(samples, dtype = np.uint32)

"""def capture(gate, ch, n):
    portal = Portal_Wormhole(BACKEND_USB, gate)
    adc = ADC_PMOD_CTRL(portal)
    samples = np.zeros(n, dtype=np.uint32)
    try:
        cnv_trig(adc, ch, n)
        while True:
            time.sleep(0.1)
            progress = cnv_progress(adc)
            print(f"Progress: {progress}%")
            if progress == 100:
                break
        read_buf(adc, ch, samples)
    finally:
        adc.portal.close()
    return samples"""


#plt.ion()

#fig, ax = plt.subplots(figsize=(12, 8))

def plot_samples(samples, title_str="ADC PMOD capture"):

    mv = adc_to_mv(samples)
    t = t_axis(len(samples))

    ax.cla()

    ax.plot(
        t,
        mv,
        marker='o',
        markersize=3,
        linewidth=1.5,
        label="Signal"
    )

    ax.set_title(title_str)
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Voltage [mV]")

    ax.legend(loc="upper right")
    ax.grid(True)

    fig.canvas.draw_idle()
    fig.canvas.flush_events()

"""def plot_samples(samples, title_str="ADC PMOD capture"):
    mv = adc_to_mv(samples)
    t = t_axis(len(samples))
    print(f"Min: {mv.min():.2f} mV   Max: {mv.max():.2f} mV")
    plt.figure(figsize=(12, 8))
    plt.plot(t, mv, marker='o', markersize=3, linewidth=1.5, label="Signal")
    plt.title(title_str)
    plt.xlabel("Time [ms]")
    plt.ylabel("Voltage [mV]")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()"""

if __name__ == "__main__":
    ch = 1  #A0 - 1, A1 - 2     #TREBA KAO PARAMETAR
    if LIVE_LOOP:
        iter = 1
        while True:
            print(f"\n─── Iteration {iter} ───")
            samples = capture(ch, N)
            plot_samples(samples, title_str=f"ADC PMOD — iter {iter}")
            iter += 1
            time.sleep(0.5)
    else:
        samples = capture(GATE, ch, N)
        plot_samples(samples)