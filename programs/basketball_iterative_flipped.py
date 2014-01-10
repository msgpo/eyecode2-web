def bball_sub(heights, counter, team):
    while not ((counter == 5) or (len(heights) == 0)):
        height = heights[0]
        heights = t(heights)
        if height > 180:
            team[counter] = height
            counter += 1

def t(heights):
    temp = []
    for i in range(1, len(heights)):
        temp.append(heights[i])
    return temp

counter = 0
team = [0, 0, 0, 0, 0]
heights = [190, 135, 185, 200, 195, 190, 215]
bball_sub(heights, counter, team)
print team
