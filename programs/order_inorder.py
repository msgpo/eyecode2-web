def skip(x):
    return x + 4

def jump(x):
    return x * 2

def fly(x):
    return skip(x) + jump(x)

def swim(x):
    return fly(x) * jump(x)

x = 1
a = skip(x)
b = jump(x)
c = fly(x)
d = swim(x)
print a, b, c, d
