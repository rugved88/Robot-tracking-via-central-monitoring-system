import queue




def printMaze(maze, path=""):
    start = 10000
    m = 0
    while (start == 10000):
        for x, pos in enumerate(maze[m]):
            if pos == "O":
                start = x  # index
                m=m-1
        m = m + 1

    i = start
    j = m
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))

    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(col + " ", end="")
        print()


def valid(maze, moves):
    start = 10000
    m = 0
    while (start == 10000):
        for x, pos in enumerate(maze[m]):
            if pos == "O":
                start = x  # index
                m=m-1
        m = m + 1

    i = start
    j = m
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == "#"):
            return False

    return True


def findEnd(maze, moves):
    global z
    start = 10000
    m=0
    while(start == 10000):
        for x, pos in enumerate(maze[m]):
            if pos == "O":
                start = x # index
                m=m-1
        m=m+1

    i = start
    j = m
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if maze[j][i] == "X":
        print("Found: " + moves)
        printMaze(maze, moves)
        z = moves
        return True

    return False


z=""
# MAIN ALGORITHM
def main1(array):
    nums = queue.Queue()
    nums.put("")
    add = ""
    #maze = createMaze2()
    maze = array

    while not findEnd(maze, add):
        add = nums.get()
        # print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)
    return z
