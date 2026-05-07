from juliacall import Main as jl
import numpy as np


jl.include("sine.jl")

ch1 = np.array(jl.f(1000, 20))
ch2 = np.array(jl.f(1000, 30))

print(ch1)
print(ch2)