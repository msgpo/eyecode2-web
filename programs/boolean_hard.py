a = True
b = False
c = True
d = True
e = False
x = 10

if ((not a and ((not b and not c) or (b and c))) or
    (a and not b and c)):
    x = x / 2

if ((not (a or b)) and c != d) or not e:
    x = x + 1

print x
