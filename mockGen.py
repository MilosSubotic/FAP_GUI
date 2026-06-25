#from DAQ_Zynq_GUI.SW.Portal.app import adc_pmod_plot as adc
from DAQ_Zynq_GUI.SW.Portal.app import dac_pmod_plot as dac
import array as array
import numpy as np
from juliacall import Main as jl
import matplotlib.pyplot as plt

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
        print("ARB FIRST 50 =")
        print(arb[:50])
        

        # Sacuvaj originalni ArbCalc signal
        self.original_arb = np.array(arb, dtype=float)
        np.savetxt(
            "/tmp/arbcalc_signal.txt",
            arb,
            fmt="%.10f"
        )

        print("Saved ArbCalc signal -> /tmp/arbcalc_signal.txt")

        """plt.figure()
        plt.plot(arb)
        plt.title("arbcalc output")
        plt.show()"""

        if self.gen is False:
            return False
        if len(arb) == 0:
            print("Empty waveform!")
            return False

        try:
            self.data = dac.waveform_to_dac(arb)

            print("DAC UNIQUE =", len(np.unique(self.data)))
            print("DAC MIN =", np.min(self.data))
            print("DAC MAX =", np.max(self.data))

            # Sacuvaj DAC kodove
            np.savetxt(
                "/tmp/dac_samples.txt",
                self.data,
                fmt="%u"
            )

            print("Saved DAC samples -> /tmp/dac_samples.txt")

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

        try:
            print("before send")

            print("samples len =", len(self.data))
            print("samples min =", np.min(self.data))
            print("samples max =", np.max(self.data))

            print("creating julia vector")

            vec = jl.Vector[jl.UInt32](self.data.tolist())

            print("vector created")

            jl.send_samples(vec)

            print("send returned")

            print("SEND OK")

        except Exception as e:
            print("SEND FAILED")
            print(e)
            raise

        self.gen.output_enable = True

    print("Waveform sent")

    def stop(self):
        self.gen.output_enable = False
        print("Mock: stopped")
