import matplotlib.pyplot as plt
import numpy as np

PG_SV_CPU = 0
PG_ADC_DMA = 1
PG_DAC_JMP = 2
PG_ADC_POLL = 3
PG_DAC_PMOD_0 = 4
PG_DAC_PMOD_1 = 5
PG_ADC_PMOD_0 = 6
PG_ADC_PMOD_1 = 7

GATE       = PG_ADC_PMOD_0   # Change to PG_ADC_PMOD_1 if needed
N          = 1 << 8       # Number of samples
VREF       = 3.3            # Reference voltage (V)
BITS       = 12              # ADC resolution
F_SMPL     = 270_270      # Sample rate in Hz — adjust to your actual rate
LIVE_LOOP  = True           # true = repeated capture loop, false = single shot
