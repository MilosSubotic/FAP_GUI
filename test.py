import os

os.environ["PYTHON_JULIACALL_EXE"] = "/home/lazar-zubovic/julia-1.9.4/bin/julia"
os.environ["PYTHON_JULIACALL_PROJECT"] = "/home/lazar-zubovic/Desktop/FAP_GUI"

from juliacall import Main as jl

print(jl.seval("sqrt(25)"))