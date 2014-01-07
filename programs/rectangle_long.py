def area(left, top, right, bottom):
    width = right - left
    height = top - bottom
    return width * height

r1_left = 0
r1_top = 5
r1_bottom = 10
r1_right = 10
r1_area = area(r1_left, r1_bottom, r1_right, r1_top)
print r1_area

r2_right = 15
r2_top = 7
r2_bottom = 12
r2_left = 10
r2_area = area(r2_left, r2_top, r2_right, r2_bottom)
print r2_area

r3_left = 6
r3_right = 10
r3_top = 4
r3_bottom = 9
r3_area = area(r3_left, r3_top, r3_right, r3_bottom)
print r3_area
