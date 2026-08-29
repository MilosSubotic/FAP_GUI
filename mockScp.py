
from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_backend as adc_pmod
from DAQ_Zynq_GUI.SW.Portal.app import adc_lvds_backend as adc_lvds
from scope_interface import Scope
from multiprocessing import Process, Queue

import threading
import numpy as np
import time

ADC_SAMPLE_RATE = 118000   # Hz, pravi ADC PMOD rate

from dataclasses import dataclass, field

adc_type = ["ADC_PMOD", "ADC_LVDS"]

@dataclass
class AcqConfig:
    record_length: int = 1000
    sample_rate: float = ADC_SAMPLE_RATE
    measure_mode: str = "BLOCK"  # or "STREAM"


class MockDevice:
    def __init__(
            self, 
            adc_type = "ADC_PMOD",
            channel = 1,
            config: AcqConfig = None,
            ):
        self.adc_type = adc_type
        self.channel = channel
        if self.adc_type == "ADC_PMOD":
            self.scp = adc_pmod
        elif self.adc_type == "ADC_LVDS":
            self.scp = adc_lvds  # Placeholder for ADC_LVDS backend
        self.config = config or AcqConfig()
        self.record_length = self.config.record_length
        self.measure_mode = self.config.measure_mode
        if self.adc_type == "ADC_PMOD":
            self.sample_rate = ADC_SAMPLE_RATE
        else:
            self.sample_rate = self.config.sample_rate
        self.measure_mode = self.config.measure_mode

    @property
    #def start(self):
        #self.scp.start(self.channel, self.record_length)

    #def stop(self):
    #    self.scp.stop(self.channel)
    
    def is_running(self):
        time.sleep(0.02)
        return self.scp.is_running(self.channel)
    
    
    def get_data(self):
        raw = self.scp.capture(self.channel, self.record_length)
        ch1 = np.asarray(raw, dtype=np.float64)
        print(f"[MOCK] get_data: ch1 len={len(ch1)}, min={np.min(ch1)}, max={np.max(ch1)}")
        ch2 = np.zeros_like(ch1)   # single real channel; pad to match 2-channel shape
        return [ch1, ch2]

class mockScope(Scope):  # ili MockScope ako pratiš abstrakciju
    def __init__(self, 
                 adc_type="ADC_PMOD",
                 channel=1,
                 config: AcqConfig = None):
        self.scp = MockDevice(
            adc_type=adc_type,
            channel=channel,
            config=config or AcqConfig()
        )
            
        self
        self.status_settings_changed = False
        self.channels = 2
        self.srs = {  # list of available sample rates @ 18 bit resolution
            "5 M": 5000000,
            "2.5 M": 2500000,
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
        if self.scp.sample_rate != sample_rate and self.scp.adc_type == "ADC_PMOD":
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
       # if self.scp.is_running:
        #    self.scp.stop()
        #self.scp.start()
        data = self.scp.get_data()
        return data

    def getBlockS(self):
       # if self.scp.is_running:
        #   self.scp.stop()

        #self.scp.start()

        while True:
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
        #if self.scp.is_running:
            #print("[MOCK] restarting scope due to trigger change")
            #self.scp.stop()
            #time.sleep(0.01)
            #self.scp.start()

        self.status_settings_changed = changed
        return changed