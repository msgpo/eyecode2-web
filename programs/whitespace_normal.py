intercept = 1
slope = 5

x_base = 0
y_base = slope * x_base + intercept
print x_base, y_base

x_other = x_base + 1
y_other = slope * x_other + intercept
print x_other, y_other

x_end = x_base + x_other + 1
y_end = slope * x_end + intercept
print x_end, y_end
