"""
本章节主要内容
1.如何玩Reversegam
2.bool（）函数
3.模拟在Reversegam游戏板上的移动；
4.编写一个ReversegamAi程序；

Reversegam游戏规则
游戏版 8*8格子
玩家 黑棋 白棋  游戏中 X O 代替黑白棋
黑方玩家和白方玩家轮流下一轮自己颜色的棋子。在新的棋子和同一颜色的另一个棋子之间，如果有对手的任何棋子，都将使其反转。游戏目标是让你的棋子尽可能地多过对方。

实现 运用到笛卡尔坐标x，y

"""
import random
import sys

WIDTH = 8
HEIGHT = 8
LIST = [['X'] * WIDTH for i in range(WIDTH)]


def drawBoard(board):
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y + 1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y + 1))
    print(' +--------+')
    print('  12345678')


# 创建一个新的游戏板数据结构
def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board


# 判定一次落子是否有效

def isValidMove(board, tile, xstart, ystart):
    # 检查空格是否为空,检查XY坐标是否在游戏板上
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tileToFlip = []

    for xdirection, ydirection in  [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        # 第一次 x += 是要判定加上去的坐标 是否有对方棋子霸占，如果有霸占 才能继续下一个判定，
        # 第二次 在一层的基础上，进行检查，是否有自己的棋子，如果有，则反转
        # 1.x,y必须在游戏版上面（2）.必须被对方玩家的棋子霸占：
        # 有效移动是指，移动必须至少反转一个棋子，否则66行while不能执行。
        while isOnBoard(x, y) and board[x][y] == otherTile:  # 检测对方的
            x += xdirection
            y += ydirection

            if isOnBoard(x, y) and board[x][y] == tile:  # 检测自己的棋子

                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tileToFlip.append([x, y])

    if len(tileToFlip) == 0:
        return False
    return tileToFlip


# 找到在哪里反转的

# 判断有效的坐标

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1


# 得到所有有效移动的一个列表
# valid有效的
# tile棋子
# board游戏版
# getBoardWithValidMoves返回一个数据结构，所有有效移动的格子都使用 ‘.’字符表示.
def getBoardWithValidMoves(board, tile):
    boardCopy = getBoardCopy(board)  # 创建Board数据结构的一个副本

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy


def getValiddMoves(board, tile):
    validMoves = []

    for x in range(WIDTH):
        for y in range(HEIGHT):
            # 循环每一个XY坐标
            if isValidMove(board, tile, x, y) != False:  # 返回可移动的列表
                validMoves.append([x, y])  # 添加可移动xy坐标
    return validMoves


def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


# 决定谁先走
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'player'
    else:
        return 'player'


# 在游戏版上落下一个棋子
def makeMove(board, tile, xstart, ystart):
    tilesToFilp = isValidMove(board, tile, xstart, ystart)
    if tilesToFilp == False:
        return False
    board[xstart, ystart] = tile
    for x, y in tilesToFilp:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    """复制一个空的游戏版
       然后从，board参数复制所有的格子
       Ai使用这个函数，从而得到一个可以修改的游戏版               """
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy


# 判断一个格子是否在角落上
def isOnCorner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


# 获取玩家的移动
def getPlayerMove(board, playerTile):
    DIGITSITO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move,"quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move
        if len(move) == 2 and move[0] in DIGITSITO8 and move[1] in DIGITSITO8:  # 这里判定是否是有效的移动
            x = int(move[0]) - 1
            y = int(move[0]) - 1
            print(isValidMove(board, playerTile, x, y))
            if isValidMove(board, playerTile, x, y) == False:  # 这里判定是否是正确的移动
                continue
            else:
                break  # 如果是可以移动，就可以退出循环
        else:
            print('That is not a valid move. Enter the column (1-8) and then the row (1-8).')
            print('For example. 81 will move on the top-right corner.')
    return [x, y]


# 获取计算机的移动
def getComputerMove(board, computerTile):
    possibleMoves = getValiddMoves(board, computerTile)
    random.shuffle(possibleMoves)  # 打乱获取可移动的列表
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    bestScore = -1  # 最佳移动的得分
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        # 一开始移动计算机可以下的位置，然后再计算当前计算机棋子的得分，得分高过bestScore的时候，记录移动，和移动
        # 第一次移动是10 但是第二次移动就变成了12的话那就是这个位置，是移动最大得分。
        score = getScoreOfBoard(boardCopy)[computerTile]  # = 10
        print(score)
        if score > bestScore:  # 计算机场上有棋子的时候 10 》 -1 10
            bestMove = [x, y]
            bestScore = score
    return bestMove


def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: %s points.Computer: %s points.' % (scores[playerTile], scores[computerTile]))
    # 代码解释


# 创建一个1 - 8 的列表用来表示 8*8 的输入范围

# 游戏开始
def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    # 检查僵局
    while True:
        playerValidMoves = getValiddMoves(board, playerTile)
        computerValidMoves = getValiddMoves(board, computerTile)
        print(playerValidMoves)
        print(computerValidMoves)
        if playerValidMoves == [] and computerValidMoves == []:
            return board
        elif turn == 'player':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)
                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:

                    makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'
        elif turn == 'computer':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile)
                input('Press Enter to see the compute\'s move.')
                move = getComputerMove(board, computerTile)
                print(move)
                makeMove(board, computerTile, move[0], move[1])

                drawBoard(board)
            turn = 'player'


print('Welcome to Reverssegam!')

playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)

    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored %s points. 0 scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer best you by  %s points! Congratulations!' % (
                    scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
