


export 
	Portal_Wormhole,
	get_portal,
	close,
	BACKEND_USB,
	BACKEND_LAN,
	PG_SV_CPU,
	PG_ADC_DMA,
	PG_DAC_JMP,
	PG_ADC_POLL,
	PG_DAC_PMOD_0,
	PG_DAC_PMOD_1,
	PG_ADC_PMOD_0,
	PG_ADC_PMOD_1

PORTAL_MAX_PAYLOAD_SIZE = 256


import Pkg
for pkg in ["Plots", "GR", "GLMakie"]
    if !haskey(Pkg.project().dependencies, pkg)
        Pkg.add(pkg)
    end
end

include("../../Common/SW/Utils.jl")
using .Utils
include("../../Common/SW/Units.jl")
using .Units
push!(LOAD_PATH, "../../Common/SW/")
#using .Utils


import Base: close

include("backends/USB.jl")

@enum portal_backend_t BACKEND_USB BACKEND_LAN

include("priv/portal_gate.jl")

include("priv/wormhole.jl")

#include("priv/SV_CPU.jl")
include("priv/ADC_DMA.jl")
include("priv/DAC_Jmp.jl")
#include("priv/ADC_Pmod_Poll.jl")
include("priv/ADC_Pmod_Ctrl.jl")
include("priv/DAC_Pmod_Ctrl.jl")




