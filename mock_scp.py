from scope_interface import Scope

import numpy as np
import time


class MockDevice:
    def __init__(self):
        self.is_running = False
        self.measure_mode = "BLOCK"
        self.sample_rate = 1e6
        self.record_length = 1e3

    def start(self):
        print("[MOCK] start")
        self.is_running = True

    def stop(self):
        print("[MOCK] stop")
        self.is_running = False

    @property
    def is_data_ready(self):
        time.sleep(0.02)
        return True

    def get_data(self):
        print("[MOCK] get_data")
        t = np.linspace(0, 1, self.record_length)
        ch1 = np.sin(2 * np.pi * 5 * t)
        ch2 = np.sin(2 * np.pi * 5 * t)
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
        print(f"[MOCK] set called, changed={changed}")
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