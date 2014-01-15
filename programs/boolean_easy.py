a = True
b = False
c = True
d = True
e = False
x = 10

if ((not a and not b and not c) or
    (not a and b and c) or
    (a and not b and c)):
    x = x / 2

f = a or b
if (c != d or not f or not e):
    x = x + 1

print x
