
import array as array
import numpy as np

class FakeGen:
    def __init__(self):
        self.output_enable = False


class mockGen:
    def __init__(self):
        self.gen = FakeGen()
        print("Generator povezan")

    def arbLoad(self, arb, amplitude=1, frequency=10, offset=0.0):
        if self.gen is False:
            return False
        try:
            self.data = np.array(arb, dtype=float)
            self.amplitude = amplitude
            self.frequency = frequency
            self.offset = offset

            print(f"Mock: Loaded {len(self.data)} samples")
        except Exception as e:
            print("Mock error:", e)
            return False

        return True
    
    def start(self):
        if self.data is None:
            print("No waveform loaded!")
            return

        self.gen.output_enable = True
        # ako postoji signal onda se generator pali

        samples = 10000

        # napravi indeks koji se vrti kroz arb
        idx = np.arange(samples) % len(self.data)

        repeated = self.data[idx]
        self.generated_signal = self.amplitude * repeated + self.offset
        print("Mock: Signal generated")

    def stop(self):
        self.gen.output_enable = False
        print("Mock: stopped")
