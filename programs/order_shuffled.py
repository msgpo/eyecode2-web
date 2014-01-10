def swim(x):
    return fly(x) * jump(x)

def jump(x):
    return x * 2

def fly(x):
    return skip(x) + jump(x)

def skip(x):
    return x + 4

x = 1
a = skip(x)
b = jump(x)
c = fly(x)
d = swim(x)
print a, b, c, d
