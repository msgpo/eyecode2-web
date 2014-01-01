x = [2, 8, 7, 9, -5, 0, 2]
y = [1, -3, 10, 0, 8, 9, 1]

xy_common = []
for x_i in x:
    if x_i in y:
        xy_common.append(x_i)

x_between = []
for x_i in x:
    if (2 < x_i) and (x_i < 10):
        x_between.append(x_i)

y_between = []
for y_i in y:
    if (-2 < y_i) and (y_i < 9):
        y_between.append(y_i)

xy_btwn_common = []
for y_i in y_between:
    if y_i in x_between:
        xy_btwn_common.append(y_i)

print xy_common
print x_between
print y_between
print xy_btwn_common
