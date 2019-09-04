"""

本章介绍
两个人玩的游戏，一个玩家 一个电脑 两个旗子 X O ，玩家交替画下 X O
胜利条件 在九宫格内 一条对角线上画下3个标记 就获胜。
平局条件 当游戏版画完，仍然没有玩家获胜，则平局

这个项目初步接触 Ai 人工智能
主要内容：
1.人工智能
2.列表引用
3.短路运算
4。None值

1.绘制游戏版
2.让玩家选择旗子
3. 随机决定谁先落旗
4.记录玩家的落棋操作
5.判定玩家是否胜利
6.判定游戏版是否填满，如果填满还没胜利就平局
7.创建一个游戏版副本
8.判定游戏的格子是否是空的
9.获取玩家落棋输入
"""

import random
import copy


# 绘制游戏版
def drawBoard(board):
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def inputPlayerLetter():  # 让玩家选择X或者O
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O ?')
        letter = input().upper()  # 获取玩家输入 更新变量
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():  # 决定谁先走
    if random.randint(0, 1) == 0:
        return 'Computer'
    else:
        return 'player'


def makeMove(board, letter, move):
    # board列表  letter == 玩家的旗子 move 移动的位置
    board[move] = letter


def isWinner(bo, le):
    print()
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[3] == le and bo[2] == le and bo[1] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le))


# 复制一个游戏版给AI算法要规划其移动的时候，它有时候只需要对游戏版的一个临时副本做出改动，而不需要修改实际的游戏版。
# getBoardCopy 创建一个游戏版
# 副本
def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


# 判定游戏版上的格子是否为空格
def isSpaceFree(board, move):
    return board[move] == ' '


def getPlayMove(board):
    move = ' '
    # 这里判定是如果为空格就退出循环，如果格子不为空，则重新输入
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move?(1-9)')
        move = input()
        if  move not in '1 2 3 4 5 6 7 8 9'.split():
            print('输入有误，请输入(1-9)')
            move = ' '
        print(move)
    return int(move) # 这里就确定了，玩家输入的位置是空格子，可以落棋。


def chooseRanddomMoveFromList(board,movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board,i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

#这下面的代码创建AI机器人的操作

def getComputerMove(board,computerLetter):
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

  # 这里判断自己落子是否能获胜
    for i in range(1,10): # 循环看下的每一步棋，会触发什么结果
        boardCopy = getBoardCopy(board) # 创建一个副本游戏版

        if isSpaceFree(boardCopy,i): #判定现在的位置是否空格
            makeMove(boardCopy,computerLetter,i) #如果不是空格把i放上
            if isWinner(boardCopy,computerLetter):
                return i # 如果这个位置能赢，直接返回该位置
    #机器人，首先最重要的是，先确认下的这一步棋能不能赢，如果能赢，立刻下。
    #如果不行，就判断，玩家下一步是否能赢，如果能赢，立刻断路
    for i in range(1,10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy,i):
            makeMove(boardCopy,playerLetter,i)
            if isWinner(boardCopy,playerLetter):
                return i

    #通过第一阶段没匹配成功的话 进入第二个判断条件 判定角 中心 边 是否有空位
    #获取1379这四个角落是否
    move = chooseRanddomMoveFromList(board,[1,3,7,9])
    if move != None:
        return move

    if isSpaceFree(board,5):
        return 5

    return chooseRanddomMoveFromList(board,[2,4,6,8])

#判断游戏版是否满了
def isBoardFull(board):
    #循环只要有一个空格，就返回False 没有空格就True
    for i in range(1,10):
        if isSpaceFree(board,i):
            return False
    return True

print('Welcome to Tic-Tac-Toe!')

while True:
    theBoard = [' '] * 10
    playerLetter,computerLetter = inputPlayerLetter() # inputPlayerLetter方法返回两个参数
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsplaying = True

    while gameIsplaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayMove(theBoard)
            makeMove(theBoard,playerLetter,move)

            if isWinner(theBoard,playerLetter):
                drawBoard(theBoard)
                print('Win')
                gameIsplaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            move = getComputerMove(theBoard,computerLetter)
            makeMove(theBoard,computerLetter,move)
            if isWinner(theBoard,computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsplaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'

    print('Do you want to play again?')
    if not input().lower().strip().startswith('y'):
        break


