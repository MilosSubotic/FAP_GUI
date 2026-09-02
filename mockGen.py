from DAQ_Zynq_GUI.SW.Portal.app import dac_jmp_backend as dac_jmp
from DAQ_Zynq_GUI.SW.Portal.app import dac_pmod_backend as dac_pmod
import array as array
import numpy as np

dac_type = ["DAC_JMP", "DAC_PMOD"]

DAC_SAMPLE_RATE = 268800.0   # Hz, pravi DAC PMOD rate

class mockGen:
    def __init__(self, dac_type="DAC_JMP"):
        self.output_enable = False
        self.dac_type = dac_type
        if self.dac_type == "DAC_JMP":
            self.gen = dac_jmp
        elif self.dac_type == "DAC_PMOD":
            self.gen = dac_pmod  # Placeholder for DAC_PMOD backend
        self.data = None

        print("Generator povezan")

    def set_cfg(
            self,
            t_pump,
            t_probe,
            f_2larmor,
            V_pump1,
            V_pump2,
            V_probe):
        self.gen.set_cfg(
            t_pump,
            t_probe,
            f_2larmor,
            V_pump1,
            V_pump2,
            V_probe
        )
    
    def arbLoad(self, arb):
        print("ARB MIN =", np.min(arb))
        print("ARB MAX =", np.max(arb))
        print("ARB LEN =", len(arb))

        self.original_arb = np.array(arb, dtype=float)

        if self.dac_type == "DAC_JMP":
            print("DAC_JMP: waveform generated in hardware")
            self.data = None
            return True

        if self.dac_type == "DAC_PMOD":
            try:
                self.data = self.gen.waveform_to_dac(arb)

                print("DAC UNIQUE =", len(np.unique(self.data)))
                print("DAC MIN =", np.min(self.data))
                print("DAC MAX =", np.max(self.data))

                self.dac_to_mv()

                return True

            except Exception as e:
                print("DAC_PMOD error:", e)
                return False

        return False
    
    def plot(self):
        self.gen.plot_waveform(self.data)

    def dac_to_mv(self):
        self.generated_signal = self.gen.dac_to_mv(self.data)
    
    def start(self):
        try:
            if self.dac_type == "DAC_JMP":
                # DAC_JMP is already configured through set_cfg().
                # No waveform samples need to be sent.
                print("DAC_JMP: hardware waveform started/configured")
                self.output_enable = True
                return

            if self.dac_type == "DAC_PMOD":
                if self.data is None:
                    print("DAC_PMOD: no waveform loaded")
                    return

                print("before send")
                print("samples len =", len(self.data))
                print("samples min =", np.min(self.data))
                print("samples max =", np.max(self.data))

                self.gen.send_samples(self.data)

                print("SEND OK")
                self.output_enable = True

        except Exception as e:
            print("SEND FAILED")
            print(e)
            raise

    def stop(self):
        self.output_enable = False
        print("Mock: stopped")
