counter = 0
team = [0, 0, 0, 0, 0]

def tail(heights):
    temp = []
    for i in range(1, len(heights)):
        temp.append(heights[i])
    return temp

def bball_sub(heights):
    global counter, team
    if not ((counter == 5) or (len(heights) == 0)):
        height = heights[0]
        heights = tail(heights)
        if height > 180:
            team[counter] = height
            counter += 1
        bball_sub(heights)

heights = [190, 135, 185, 200, 195, 190, 215]
bball_sub(heights)
print team
