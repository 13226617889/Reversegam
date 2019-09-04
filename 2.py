import sys
import random
import time

WIDTH = 8
HEIGHT = 8


# 用isvalidmoves这个方法，如果输入是空的棋位，再进行，反转判定，如果没有的反转，则返回False，这是无效的移动。则重新输入
# 用while 实现循环，无效 control ，有效 跳出循环，判断这输入是有效的输入
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


list = [['X'] * 8 for i in range(8)]
list[3][2] = 'Z'


def getNewBoard():
    board = []
    for i in range(HEIGHT):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board


# 判断一次落子是否有效

def isValidMoves(board, tile, xstart, ystart):
    # 返回输入的X，y位置的可反转棋子位置。
    # 返回的是确定了有反转棋子的位置
    # 这里判定的是，是否有棋子。如果有则退出。
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        theTile = 'O'
    else:
        theTile = 'X'
    tilesToFlip = []
    # [4,6]
    # 在空的位置上进行方向判定
    # 前提是，用宽度和高度，循环每一个，x，y坐标，返回可移动列表。
    # 只循环空位置，如果有棋子的位置，则返回False
    # 如果该方向有对方的棋子，那么沿着该棋子的方向进行判定，如果遇到自己的棋子则，倒回去到开始x,y坐标，添加到可移动列表。
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        # 如果当前位置有对方的棋子，进行下一层判定
        # 位置就变成了对方的棋子，再在他原有的方向进行移动。
        while isOnBoard(x, y) and board[x][y] == theTile:
            x += xdirection
            y += ydirection
            # 在移动的时候进行判定，是否还是对方的棋子，如果是继续，知道超出宽度，或者，碰到自己的棋子。
            if isOnBoard(x, y) and board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    # 判定玩家输入是否是有效的移动46 33

    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip  # 返回的是可翻转的XY#这里两层判定，首先要判定，加上方向后，该位置是否有对方棋子。 #如果有对方棋子，进入下一层判定#判定


def getValidMoves(board, tile):
    ValidMoveList = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMoves(board, tile, x, y) != False:
                ValidMoveList.append([x, y])

    return ValidMoveList

def horn(x,y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)
def getboardCopy(board):
    BOARD = getNewBoard()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            BOARD[x][y] = board[x][y]
    return BOARD


def getComputerMoves(board,computerTile):
    possibleMoves = getValidMoves(board,computerTile) #这里返回是有效移动
    print(possibleMoves)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if horn(x, y):
            return [x, y]

    #这里就判定哪个位置的移动是最高分的
    #先移动这个位置，再调用计分的
    Score = -1
    for x, y in possibleMoves:
        boardCopy = getboardCopy(board)
        makemove(boardCopy, computerTile, x, y)
        bbscore = getScore(boardCopy)[computerTile]
        if bbscore > Score:
            bestMove = [x, y]
            Score = bbscore

    return bestMove




# 玩家输入
def enterXY():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def getplaymove(board, playTile):
    # 先判定输入的X，y宽度是否符合
    Dis = ('1 2 3 4 5 6 7 8').split()
    while True:
        move = input('请输入你的移动').lower()
        if move == 'quit' or move == 'hints':
            return move
        if len(move) == 2 and move[0] in Dis and move[1] in Dis:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMoves(board, playTile, x, y) == False:
                # 因为没法反转对面的所以，这是无效的输入
                # 走到这一步需要加多一层外面的判定，如果没有可移动的位置，则直接返回board，看谁的棋子多，则获胜
                continue
            else:
                break
    return [x, y]


def getScore(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':    
                oscore += 1
    return {'X': xscore, 'O': oscore}


def printScore(board, play, computer):
    score = getScore(board)
    print('You: %s points. Computer: %s points.' % (score[play], score[computer]))

def Tips(board,tile):
    Validmove = getboardCopy(board)
    for x, y in getValidMoves(Validmove,tile):
        Validmove[x][y] = '.'
    return Validmove


def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

#反转的方法
#makemove前提是传入有效的移动
def makemove(board,tile,xstar,ystar):
    isvalidmove = isValidMoves(board,tile,xstar,ystar)#得到反转的列表

    board[xstar][ystar] = tile

    for x, y in isvalidmove:
        board[x][y] = tile
    return True
# drawBoard(getNewBoard())
def whoGhostFirst():
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'computer'
def playGame(play, computer):
    shoW = False
    whoGhost = whoGhostFirst()
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'O'
    board[3][5] = 'X'
    board[4][5] = 'O'
    drawBoard(board)
    while True:
        playValidmove = getValidMoves(board, play)
        computerValidmove = getValidMoves(board, computer)
        if len(playValidmove) == 0 and len(computerValidmove) == 0:
            return board
        elif whoGhost == 'play':
            if playValidmove != []:
                if shoW:
                    tipsBoard = Tips(board,play)
                    drawBoard(tipsBoard)
                else:
                    drawBoard(board)
                printScore(board, play, computer)
                move = getplaymove(board, play)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()  # Terminate the program.
                elif move == 'hints':
                    shoW = not shoW
                    continue
                else:
                    makemove(board, play, move[0], move[1])
            whoGhost = 'computer'
        elif whoGhost == 'computer':
            if computerValidmove != []:
                drawBoard(board)
                printScore(board,play,computer)
                input('Press Enter to see the computer\'s move.')
                move = getComputerMoves(board,computer)
                makemove(board,computer,move[0],move[1])
            whoGhost = 'play'
play, computer = enterXY()

while True:
    RunGame = playGame(play, computer)
    scores = getScore()
    print('X scored %s points. 0 scored %s points.' % (scores['X'], scores['O']))
    if scores[play] > scores[computer]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[play] < scores[computer]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tim!')
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break

