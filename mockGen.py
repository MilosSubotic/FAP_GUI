#from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_plot as adc
from DAQ_Zynq_GUI.SW.Portal.app import dac_pmod_plot as dac
import array as array
import numpy as np
from juliacall import Main as jl

class FakeGen:
    def __init__(self):
        self.output_enable = False


class mockGen:
    def __init__(self):
        self.gen = FakeGen()
        self.data = None

        print("Generator povezan")

    def arbLoad(self, arb):
        print("ARB MIN =", np.min(arb))
        print("ARB MAX =", np.max(arb))
        print("ARB LEN =", len(arb))

        if self.gen is False:
            return False
        if len(arb) == 0:
            print("Empty waveform!")
            return False
        try:
            #self.data = np.array(arb, dtype=float)
            self.data = dac.waveform_to_dac(arb)

            print(f"Mock: Loaded {len(self.data)} samples")

            self.dac_to_mv()
        except Exception as e:
            print("Mock error:", e)
            return False

        return True
    
    def plot(self):
        dac.plot_waveform(self.data)

    def dac_to_mv(self):
        self.generated_signal = dac.dac_to_mv(self.data)
    
    def start(self):

        if self.data is None:
            return

        jl.send_samples(
            jl.Vector[jl.UInt32](self.data.tolist())
        )

        self.gen.output_enable = True

        print("Waveform sent")

    def stop(self):
        self.gen.output_enable = False
        print("Mock: stopped")
