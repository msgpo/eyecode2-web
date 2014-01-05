a = True
b = False
c = True
x = 10

if ((not a and b and c) or
    (b and not c and a) or
    (c and not a and b) or
    (not b and not c and not a)):
    x = x / 2

if ((b and c and a) or
    (not a and not b and c) or
    (not c and not a and b) or
    (not b and not c and not a)):
    x = x + 1

print x
