a = True
b = False
c = True
x = 10

if ((not a and not b and c) or
    (not c and b and not a) or
    (not c and not b and not a) or
    (b and not a and c)):
    x = x / 2

if ((a and c and b) or
    (not b and not a and c) or
    (not c and not b and not a) or
    (a and b and not c)):
    x = x + 1

print x
