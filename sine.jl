import Pkg
if !haskey(Pkg.project().dependencies, "Plots")
    Pkg.add("Plots")
end
using Plots


function f(sample_rate, freq)
    fs = sample_rate
    frequency = freq
    x = 0:1/fs:1
    y = sin.(2*pi*x*frequency)



    #display(plot(x, y, label="sine", xlabel="Time", ylabel="Amplitude", title="Sine Wave"))
    p = plot(x, y)
    savefig(p, "sine.png")
    gui(p)

    return y
end


f(1000,2)
