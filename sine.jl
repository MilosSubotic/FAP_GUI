function f(sample_rate, freq)
    fs = sample_rate
    x = 0:1/fs:1
    y = sin.(2*pi*freq .* x)

    return y
end
