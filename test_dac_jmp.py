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

def set_cfg_py(t_pump, t_probe, f_2larmor, V_pump1, V_pump2, V_probe):
    print("Initial probe")
    mon_probe()

    print("Writing configuration")

    jmp_backend.set_cfg(
        t_pump=t_pump,
        t_probe=t_probe,
        f_2larmor=f_2larmor,
        V_pump1=V_pump1,
        V_pump2=V_pump2,
        V_probe=V_probe,
    )

    print("Configured")

    mon_probe()

if __name__ == "__main__":
    set_cfg_py(10e-3, 20e-3, 10e3, 0.5, 1.5, 1.0)