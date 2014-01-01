def green(x):
    return x + 4

def blue(x):
    return x * 2

def orange(x):
    return green(x) + blue(x)

def purple(x):
    return orange(x) * blue(x)

x = 1
a = green(x)
b = blue(x)
c = orange(x)
d = purple(x)
print a, b, c, d
