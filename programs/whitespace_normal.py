intercept = -1
slope = 3

x_base = 2
y_base = slope * x_base + intercept
print x_base, y_base

x_other = x_base + 1
y_other = slope * x_other + intercept
print x_other, y_other

x_end = x_base + x_other + 2
y_end = x_end * slope + intercept
print x_end, y_end
