def area(left, top, right, bottom):
    width = right - left
    height = top - bottom
    return width * height

r1_x1 = 0
r1_y1 = 5
r1_y2 = 10
r1_x2 = 10
r1_area = area(r1_x1, r1_y2, r1_x2, r1_y1)
print r1_area

r2_x2 = 15
r2_y1 = 7
r2_y2 = 12
r2_x1 = 10
r2_area = area(r2_x1, r2_y1, r2_x2, r2_y2)
print r2_area

r3_x1 = 6
r3_x2 = 10
r3_y1 = 4
r3_y2 = 9
r3_area = area(r3_x1, r3_y1, r3_x2, r3_y2)
print r3_area
