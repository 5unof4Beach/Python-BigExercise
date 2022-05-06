import numpy
import math

# Constant values representing directions
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
DIR = 0



def move(flattenedGrid, key):
    # temp = grid
    size = int(math.sqrt(len(flattenedGrid)))
    grid = numpy.zeros((size, size), dtype=int)

    for i in range(size):
        grid[i][:] = flattenedGrid[i*size : size*(i + 1)]

    for i in range(size):
        flipped = False
        if key in 'lr':  # nếu nhập vào là l hoặc r thì lấy hàng
            row = grid[i, :]
        else:
            row = grid[:, i]  # u hoăc d thì lấy cột

        if key in 'rd':  # nếu là r hoặc d thì lật ngược list để có thể tận dụng hàm get num
            flipped = True
            row = row[::-1]

        notZeros = _get_num(row)  # list những số != 0 trong hàng
        newRow = numpy.zeros_like(row)  # tạo một hàng mới chỉ chứa số 0 có kích cỡ giống hàng cũ
        newRow[:len(notZeros)] = notZeros  # gắn các giá trị != 0 vào mảng mới

        if flipped:
            newRow = newRow[::-1]

        if key in 'lr':
            grid[i, :] = newRow
        else:
            grid[:, i] = newRow

    return grid.flatten()

def _get_num(row):
    notZeros = row[row != 0]
    res = []
    skip = False
    for i in range(len(notZeros)):
        if skip:
            skip = False
            continue
        if i != len(notZeros) - 1 and notZeros[i] == notZeros[i + 1]:  # nếu 2 số liền nhau mà giống nhau thì cộng lại và cho vào mảng mới
            sum = notZeros[i] * 2
            res.append(sum)
            skip = True
        else:
            res.append(notZeros[i])
    return res

def movable(grid, direction):
    if all(grid.flatten() == move(grid, direction)):
        return False
    else:
        return True


# Heuristic giving bonus points for every empty tile on the board
def emptyTilesHeuristic(grid):
    zeros = 0
    for i in range(16):
        if grid[i] == 0:
            zeros += 1

    return zeros

# Heuristic giving bonus points for maximum value on the board
def maxValueHeuristic(grid):
    maximumValue = -1
    for i in range(16):
        maximumValue = max(maximumValue, grid[i])

    return maximumValue

# Heuristic giving bonus points for minimizing differences between adjacent tiles
def smoothnessHeuristic(grid):
    smoothness = 0
    for i in range(4):
        current = 0
        while current < 4 and grid[4*i + current] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1
            if next >= 4:
                break

            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    for i in range(4):
        current = 0
        while current < 4 and grid[current*4 + i] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[4*next + i]:
                next += 1
            if next >= 4:
                break

            currentValue = grid[current*4 + i]
            nextValue = grid[next*4 + i]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    return smoothness*10

# Heurisitc giving bonus poitns for monotonic rows of tiles
def monotonicityHeurictic(grid):
    monotonicityScores = [0, 0, 0, 0]

    # left/right direction
    for i in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1

            if next >= 4:
                next -= 1
            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]

            if currentValue > nextValue:
                monotonicityScores[0] += nextValue - currentValue
            elif nextValue > currentValue:
                monotonicityScores[1] += currentValue - nextValue

            current = next
            next += 1

    #up/down direction
        for i in range(4):
            current = 0
            next = current + 4
            while next < 4:
                while next < 4 and grid[i + 4*next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                currentValue = grid[i + 4*current]
                nextValue = grid[i + 4*next]

                if currentValue > nextValue:
                    monotonicityScores[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    monotonicityScores[3] += currentValue - nextValue
            current = next
            next += 1

    return 20* max(monotonicityScores[0], monotonicityScores[1]) + max(monotonicityScores[2], monotonicityScores[3])

# Heuristic giving bonus points for placing tile with maximum value at the corner of the board
def positionOfMaxValueHeuristic(grid):
    maxValue = maxValueHeuristic(grid)
    if maxValue == grid[0] or maxValue == grid[3] or maxValue == grid[12] or maxValue == grid[15]:
        return 5000
    else:
        return -5000

scoreGrid = {4:[
                1000 , 700, 400, 200,
                 700, 300, 100, 100,
                 400, 100, 100, 100,
                 200, 100, 100, 100
                 ],
            8:[
                10000 , 7000, 4000, 1000, 1000, 1000, 700, 500,
                 7000, 3000, 1000, 1000, 1000, 1000, 1000, 1000,
                 4000, 1000, 500, 500,500, 500, 500, 500,
                 500, 500, 500, 500,500, 500, 500, 500,
                 500, 500, 500, 500,500, 500, 500, 500,
                 500, 500, 500, 500,500, 500, 500, 500,
                 500, 500, 500, 500,500, 500, 500, 500,
                 500, 500, 500, 500,500, 500, 500, 500
            ]   }

def weightedTilesHeuristic(grid):
    size = int(math.sqrt(len(grid)))

    weightedGrid = scoreGrid[size]
    score = 0
    for i in range(size**2):
        score += grid[i] * weightedGrid[i]

    return score


# Function returning score of the given graph   
# Feel free to modify it and play with the constants :)
def getScore(grid):
    emptyTilesScore = emptyTilesHeuristic(grid) * 100
    maxValueScore = maxValueHeuristic(grid) * 4
    smoothnessScore = smoothnessHeuristic(grid) * 10
    monotonicityScore = monotonicityHeurictic(grid) * 40
    positionOfMaxValueScore = positionOfMaxValueHeuristic(grid) * 5
    weightedTilesScore = weightedTilesHeuristic(grid)

    # Exemplary score, try to modify it along with constants above
    # Little change can make huge difference
    return weightedTilesScore + smoothnessScore + emptyTilesScore






