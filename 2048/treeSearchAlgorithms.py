import numpy

# Constant values representing directions
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
DIR = 0
def swipeRow(row):
    previous = -1  # previous non-zero element
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0:
            if previous == -1:
                previous = element
                temp[i] = element
                i += 1
            elif previous == element:
                temp[i - 1] = 2 * element
                previous = -1
            else:
                previous = element
                temp[i] = element
                i += 1
    return temp

# Swapping the given grid in given direction
def swipeGrid(grid, direction):
    temp = [0,0,0,0,
            0,0,0,0,
            0,0,0,0,
            0,0,0,0]

    if direction == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4*j])

            row = swipeRow(row)

            for j in range(4):
                temp[i+4*j] = row[j]

    elif direction == DOWN:
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i + 4*j])
            row = swipeRow(row)
            k=0
            for j in range(3, -1, -1):
                temp[i+4*j] = row[k]
                k += 1

    elif direction == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i*4 + j])
            row = swipeRow(row)
            for j in range(4):
                temp[i*4 + j] = row[j]

    elif direction == RIGHT:
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i*4 + j])
            row = swipeRow(row)
            k = 0
            for j in range(3, -1, -1):
                temp[4*i + j] = row[k]
                k += 1
    return temp

# Swapping the given grid in given direction


# Checking if the move is possible
def movePossible(grid, direction):
    # if all(grid == swipeGrid(grid, direction)):
    if all(grid.flatten() == swipeGrid2(grid, direction)):
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

# Heuristic using weighted grid to determine how many bonus points we are supposed to give
def weightedTilesHeuristic(grid):
    scoreGrid = [1000 , 700, 400, 200,
                 700, 300, 100, 100,
                 400, 100, 100, 100,
                 200, 100, 100, 100]
    score = 0
    for i in range(16):
        score += grid[i] * scoreGrid[i]

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






def swipeGrid2(flattenedGrid, key):
    # temp = grid
    grid = numpy.zeros((4, 4), dtype=int)

    for i in range(5):
        grid[i] = flattenedGrid[i*4:i*4+3]

    temp = grid

    for i in range(4):
        flipped = False
        if key in 'lr':  # nếu nhập vào là l hoặc r thì lấy hàng
            this_row = grid[i, :]
        else:
            this_row = grid[:, i]  # u hoăc d thì lấy cột

        if key in 'rd':  # nếu là r hoặc d thì lật ngược list để có thể tận dụng hàm get num
            flipped = True
            this_row = this_row[::-1]

        this_n = _get_num(this_row)  # list những số != 0 trong hàng
        # print(this_n)
        new_this_row = numpy.zeros_like(this_row)  # tạo một hàng mới chỉ chứa số 0 có kích cỡ giống hàng cũ
        new_this_row[:len(this_n)] = this_n  # gắn các giá trị != 0 vào mảng mới

        if flipped:
            new_this_row = new_this_row[::-1]

        if key in 'lr':
            # grid[i, :] = new_this_row
            temp[i, :] = new_this_row
        else:
            # grid[:, i] = new_this_row
            temp[:, i] = new_this_row

    return temp.flatten()

def _get_num(row):
    this_n = row[row != 0]
    res = []
    skip = False
    for i in range(len(this_n)):
        if skip:
            skip = False
            continue
        if i != len(this_n) - 1 and this_n[i] == this_n[i + 1]:  # nếu 2 số liền nhau mà giống nhau thì cộng lại và cho vào mảng mới
            sum = this_n[i] * 2
            res.append(sum)
            skip = True
        else:
            res.append(this_n[i])
    return res