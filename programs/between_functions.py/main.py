from helpers import between, common

x = [2, 8, 7, 9, -5, 0, 2]
y = [1, -3, 10, 0, 8, 9, 1]

xy_common = common(x, y)
x_between = between(x, 2, 10)
y_between = between(y, -2, 9)
xy_btwn_common = common(y_between, x_between)

print xy_common
print x_between
print y_between
print xy_btwn_common
