#from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_plot as adc
from DAQ_Zynq_GUI.SW.Portal.app import dac_pmod_plot as dac
import array as array
import numpy as np

class FakeGen:
    def __init__(self):
        self.output_enable = False


class mockGen:
    def __init__(self):
        self.gen = FakeGen()
        self.data = None
        print("Generator povezan")

    def arbLoad(self, arb):
        if self.gen is False:
            return False
        if len(arb) == 0:
            print("Empty waveform!")
            return False
        try:
            #self.data = np.array(arb, dtype=float)
            self.data = dac.generate_sine()

            print(f"Mock: Loaded {len(self.data)} samples")
        except Exception as e:
            print("Mock error:", e)
            return False

        return True
    
    def plot(self):
        dac.plot_waveform(self.data)
    
    def start(self):
        if self.data is None or len(self.data) == 0:
            print("No waveform loaded!")
            return

        self.gen.output_enable = True

        print("Mock: Signal generated")

    def stop(self):
        self.gen.output_enable = False
        print("Mock: stopped")
