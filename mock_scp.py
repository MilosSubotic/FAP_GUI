from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_plot as adc
#from DAQ_Zynq_GUI.SW.Portal.app import dac_pmod_plot as dac
from scope_interface import Scope

import threading
import numpy as np
import time

from multiprocessing import Process, Queue

def worker(q, n):
    import os
    import threading

    print("PID =", os.getpid())
    print("THREAD =", threading.get_ident())
    print("worker process start")

    from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_plot as adc

    raw = adc.capture(1, n)

    print("capture done")

    q.put(raw)

    print("queue put done")

ADC_SAMPLE_RATE = 118000   # Hz, pravi ADC PMOD rate
ADC_BITS        = 12
ADC_VREF        = 3.3
ADC_N_SAMPLES   = 256       # po kanalu, matches standalone skriptu



class MockDevice:
    def __init__(self):
        self.is_running = False
        self.measure_mode = "BLOCK"
        self.sample_rate = ADC_SAMPLE_RATE
        self.record_length = ADC_N_SAMPLES

    def start(self):
        # print("[MOCK] start")
        self.is_running = True

    def stop(self):
        # print("[MOCK] stop")
        self.is_running = False

    @property
    def is_data_ready(self):
        time.sleep(0.02)
        return True

    def get_data(self):

        q = Queue()

        p = Process(
            target=worker,
            args=(q, self.record_length)
        )

        print("before process")

        p.start()

        print("before q.get")

        raw = q.get()

        print("after q.get")

        p.join()

        ch1 = adc.adc_to_mv(raw)
        ch2 = np.zeros_like(ch1)

        return [ch1, ch2]
    


class mockSCP(Scope):  # ili MockScope ako pratiš abstrakciju
    def __init__(self):
        self.scp = MockDevice()
        self.status_settings_changed = False
        self.channels = 2
        self.srs = {  # list of available sample rates @ 16 bit resolution
            "6.25 M": 6250000,
            "3.125 M": 3125000,
            "1.25 M": 1250000,
            "625 k": 625000
        }
        self.trigger_name = "Generator"
    def set(self,
            mode="block",
            sample_rate=1e6,
            record_length=1e3,
            CH_ranges=None,
            CH_couplings=None,
            trigger_source="Generator"):

        changed = False

        # mode
        new_mode = "BLOCK" if mode == "block" else "STREAM"
        if self.scp.measure_mode != new_mode:
            self.scp.measure_mode = new_mode
            changed = True

        # sample rate
        if self.scp.sample_rate != sample_rate:
            self.scp.sample_rate = sample_rate
            changed = True

        # record length
        if self.scp.record_length != int(record_length):
            self.scp.record_length = int(record_length)
            changed = True

        self.status_settings_changed = changed
        # print(f"[MOCK] set called, changed={changed}")
        return changed

    def getBlock(self):
        self.scp.start()

        while not self.scp.is_data_ready:
            time.sleep(0.01)

        data = self.scp.get_data()
        self.scp.stop()
        return data

    def getBlockS(self):
        if self.scp.is_running:
            self.scp.stop()

        self.scp.start()

        while True:
            while not self.scp.is_data_ready:
                time.sleep(0.01)

            yield self.scp.get_data()

    def set_trigger(self, trigger_source="Generator"):
        print(f"[MOCK] set_trigger called: {trigger_source}")

        changed = False

        if self.trigger_source != trigger_source:
            self.trigger_source = trigger_source
            changed = True

        # simulacija logike iz pravog uređaja
        if trigger_source == "Generator":
            print("[MOCK] Trigger = Generator (auto periodic)")
        else:
            print(f"[MOCK] Trigger = Channel {trigger_source}")

        # simuliraj da treba restart ako je scope running
        if self.scp.is_running:
            print("[MOCK] restarting scope due to trigger change")
            self.scp.stop()
            time.sleep(0.01)
            self.scp.start()

        self.status_settings_changed = changed
        return changed