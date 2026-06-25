import time
import DAQ_Zynq_GUI.SW.Portal.app.jmp_backend as jmp_backend


def mon_probe():

    print("Waiting for falling edge...")

    while jmp_backend.probe():
        time.sleep(0.001)

    print("Waiting for rising edge...")

    while not jmp_backend.probe():
        time.sleep(0.001)

    t0 = time.time()

    print("Waiting for falling edge...")

    while jmp_backend.probe():
        time.sleep(0.001)

    t1 = time.time()

    print(f"Probe = {(t1 - t0) * 1000:.2f} ms")


print("Initial probe")
mon_probe()

print("Writing configuration")

jmp_backend.set_cfg(
    t_pump=10e-3,
    t_probe=20e-3,
    f_2larmor=10e3,
    V_pump1=0.5,
    V_pump2=1.5,
    V_probe=1.0,
)

print("Configured")

mon_probe()