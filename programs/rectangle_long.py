def area(left, top, right, bottom):
    width = right - left
    height = top - bottom
    return width * height

r1_left = 0
r1_top = 0
r1_right = 10
r1_bottom = 10
r1_area = area(r1_left, r1_top, r1_right, r1_bottom)
print r1_area

r2_left = 5
r2_top = 5
r2_right = 10
r2_bottom = 10
r2_area = area(r2_left, r2_bottom, r2_right, r2_top)
print r2_area
