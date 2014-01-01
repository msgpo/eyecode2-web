def purple(x):
    return orange(x) * blue(x)

def blue(x):
    return x * 2

def orange(x):
    return green(x) + blue(x)

def green(x):
    return x + 4

x = 1
a = green(x)
b = blue(x)
c = orange(x)
d = purple(x)
print a, b, c, d
