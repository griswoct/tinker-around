#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-02-25
#
#break parse move out as a seperate function
#More Ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers and defenders are there on each piece
    #Identify checkmate
    #Identifies all valid move for selected piece

#VARIABLES (GLOBAL)
capture = False #Indicates a piece is being captured
check = False   #King is in Check
good = False    #Boolean to control loops
white = True    #Playing as white? (Boolean)
a = 52    #Board index starting location
b = 36    #Board index ending location
i = 0    #Integer index
j = 0    #Integer index
k = 0    #Integer index
fileA = [0,8,16,24,32,40,48,56] #Board indexes for A-file (edge of board)
fileB = [1,9,17,25,33,41,49,57] #Board indexes for B-file
fileH = [7,15,23,31,39,47,55,63]    #Board indexes for H-file (edge of board)
fileG = [6,14,22,30,38,46,54,62]    #Board indexes for G-file
locations = [0,0,0,0,0,0,0,0,0,0]   #Number and locations of pieces
move = 'e4'    #Chess move in algebraic notation
piece = 'P' #Letter indicating piece (capitalization indicates color)
square = 'e4'    #Selected square on the board (algebraic notation)
board = []    #Chess board configuration
board_old = []
pieces = ['K','k','Q','q','R','r','N','n','B','b','P','p']    #Valid chess pieces list
xblack = ['q','r','b','n','p']    #Capturable black pieces list (no King)
xwhite = ['Q','R','N','B','P']    #Capturable white pieces list (no King)

#FUNCTIONS
#Get Chess Board Setup
def GetBoard():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Default starting position
    fen = input("Enter D for default starting position, or board configuration in FEN notation: ")
    if fen == 'D' or fen == 'd':
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Chess starting position
    i = 0    #Position in fen array
    j = 0    #Board position
    while j < 64 and i < len(fen):    #Populate board array from FEN string
        if fen[i] == '/':    #Next rank
            if j % 8 != 0:    # '/' character encountered midway through a rank
                print("Error: unexpected / in the board configuration:")
                print(fen)
                break
            else:
                i += 1    #Ignore and go to to next character
        elif fen[i].isdigit() == True:
            if int(fen[i]) > 8:    #More than 8 empty squares in a rank isn't posible in normal chess
                print("Error: extra empty squares in the board configuration:")
                print(fen)
                break
            else:
                k = 0    #Number of empty squares added to rank
                while k < int(fen[i]):    #Add specified number of empty squares to board array
                    board.append(' ')
                    k += 1
                    j += 1
                i += 1    #Go to next character after adding empty squares
        elif fen[i] in pieces:    #Checks if character indicates valid chess piece
            board.append(fen[i])
            i += 1
            j += 1
        else:
            print("Error: ", fen[i], " is not a recognized piece.")
            break
    return board

#Validate Chess Board Configuration
def ValidBoard(board):
    if len(board) != 64:
        print("Error: incomplete board")    #Board array should have 64 elements
        return False
    for i in pieces:
        k = 0
        for j in board:
            if i == j:
                k += 1
        if k > 9:
            print("Error: excessive number of ", i)
            return False
        elif i == 'p' and k > 8:
            print("Error: more than 8 black Pawns")
            return False
        elif i == 'P' and k > 8:
            print("Error: more than 8 white Pawns")
            return False
        elif i == 'k' and k != 1:
            print("Error: there should be exactly 1 black King. Found ", k)
            return False
        elif i == 'K' and k != 1:
            print("Error: there should be exactly 1 white King. Found ", k)
        else:
            return True

#Display Chess Board on Terminal Screen
def ShowBoard(brd):
    i = 0    #Board position
    while i < 64:    #Display board
        print(brd[i:i+8])
        i += 8

#Convert Algebraic Notated Square to Board Index Number
def BoardIndex(sq):
    if len(sq) != 2:    #Board location should be 2 characters in algebraic notation
        return 64    #Invalid index indicating error
    elif not sq[1].isdigit: #Second digit in location should be a number
        return 64
    elif int(sq[1]) != 0 and int(sq[1]) != 9: #Rank 1-8
        if sq[0] == 'a' or sq[0] == 'A':
            i = (8 - int(sq[1])) * 8
        elif sq[0] == 'b' or sq[0] == 'B':
            i = (8 - int(sq[1])) * 8 + 1
        elif sq[0] == 'c' or sq[0] == 'C':
            i = (8 - int(sq[1])) * 8 + 2
        elif sq[0] == 'd' or sq[0] == 'D':
            i = (8 - int(sq[1])) * 8 + 3
        elif sq[0] == 'e' or sq[0] == 'E':
            i = (8 - int(sq[1])) * 8 + 4
        elif sq[0] == 'f' or sq[0] == 'F':
            i = (8 - int(sq[1])) * 8 + 5
        elif sq[0] == 'g' or sq[0] == 'G':
            i = (8 - int(sq[1])) * 8 + 6
        elif sq[0] == 'h' or sq[0] == 'H':
            i = (8 - int(sq[1])) * 8 + 7
        else:
            return 64
        if i < 0 or i > 63:
            return 64    #Invalid index indicating error
        else:
            return i

#Conver Board Index to Algebraic Notation
def BoardAlgebraic(i):
    if i % 8 == 0:
        spot = 'h'
    elif i % 8 == 1:
        spot = 'g'
    elif i % 8 == 2:
        spot = 'f'
    elif i % 8 == 3:
        spot = 'e'
    elif i % 8 == 4:
        spot = 'd'
    elif i % 8 == 5:
        spot = 'c'
    elif i % 8 == 6:
        spot = 'b'
    else:
        spot = 'a'
    if i < 8:
        spot += '8'
    elif i < 16:
        spot += '7'
    elif i < 24:
        spot += '6'
    elif i < 32:
        spot += '5'
    elif i < 40:
        spot += '4'
    elif i < 48:
        spot += '3'
    elif i < 56:
        spot += '2'
    else:
        spot += '1'
    return spot

#Verify the Piece "p" Can Be Captured
def ValidCapture(p):
    if white:
        if p in xblack:
            if not capture:
                if p == 'P' or p == 'p':
                    correct = piece + 'x' + move
                else:
                    correct = piece + 'x' + move[1:]
                print("Changing move to: ", correct)
            else:
                correct = move
            return correct
        else:    #A non-capturable piece is already on the square
            if p == 'k':
                print("You cannot capture the King")
            elif p in xwhite or p == 'K':
                print("Your ", p, " is already on ", square)
            else:
                print("Something went wrong. ", p, " is on ", square)
            return False
    else:
        if p in xwhite:
            if not capture:
                correct = piece + 'x' + move[1:]
                print("Changing move to: ", correct)
            else:
                correct = move
            return correct
        else:    #A non-capturable piece is already on the square
            if p == 'K':
                print("You cannot capture the King")
            elif p in xblack or p == 'k':
                print("Your ", p, " is already on ", square)
            else:
                print("Something went wrong. ", p, " is on ", square)
            return False

#Find the Number and Locations of Pieces "p"
def FindPieces(p):
    loc = [0,64,64,64,64,64,64,64,64,64]   #Count and up to 9 locations, 64 is off the board
    c = 0
    i = 0
    while i < 64:
        if board[i] == p:
            c += 1
            loc[0] = c
            loc[c] = i
        i += 1
    return loc

#Find which locations 'loc' can be a starting points for piece 'p' to get to square 'end'
def WhichPiece(p, loc, end):
    i = 1   #First location at locations[1]
    j = 0
    good = False
    while i <= loc[0]:    #locations[0] indicates the number of pieces found
        if loc[i] == 64:  #Invalid board index
            break
        elif j > 1: #More than one piece can move to square b
            break
        else:
            good = ValidPath(p, loc[i], end)    #piece on locations[i] can move to square b
            if good:
                j += 1
                start = loc[i]   #save starting location
                good = False
        i += 1
    if j > 1:
        #Need to select Pawn based on letter in the move
        start = input("Multiple pieces can make that move. Please enter the location of the intended piece: ")
        start = BoardIndex(start)
        #Check a is in locations, check a to b is a valid move for piece
        return start
    elif j == 0:
        print("Error: could not find a", p, "that can move to", square)
        return 64
    else:
        return start

#Backtracks along the path for that type of piece and returns the locations of that type of piece
def BackTrack(destination, type):
    origins = []
    color = not white   #include your own pieces, not your opponents
    if type == 'P' or type == 'p':
        reach = PawnMoves(destination, color)
    elif type == 'B' or type == 'b':
        reach = BishopMoves(destination, color)
    elif type == 'N' or type == 'n':
        reach = KnightMoves(destination, color)
    elif type == 'R' or type == 'r':
        reach = RookMoves(destination, color)
    elif type == 'Q' or type == 'q':
        reach = QueenMoves(destination, color)
    elif type == 'K' or type == 'k':
        reach = KingMoves(destination, color)
    i = 0
    while i < len(reach):
        if board[reach[i]] == type:
            origins.append(reach[i])
        i += 1
    #NEED TO UPDATE MOVE FUNCTIONS TO SPECIFY WHICH COLOR TO INCLUDE
    return origins

#Checks if a piece can move from origin to destination in a single move
def ValidPath(type, origin, destination):
    if type == 'P' or type == 'p':
        reach = PawnMoves(origin, white)
    elif type == 'B' or type == 'b':
        reach = BishopMoves(origin, white)
    elif type == 'N' or type == 'n':
        reach = KnightMoves(origin, white)
    elif type == 'R' or type == 'r':
        reach = RookMoves(origin, white)
    elif type == 'Q' or type == 'q':
        reach = QueenMoves(origin, white)
    elif type == 'K' or type == 'k':
        reach = KingMoves(origin, white)
    else:
        print("Error: couldn't determine possible moves for", type, "on", origin)
    print(type, "on", origin, "can reached:")   #for testing
    print(reach)    #for testing
    if destination in reach:
        return True
    else:
        return False

#Returns the squares a Pawn can move to
def PawnMoves(home, forwards):
    path = [home]
    if forwards:
        if home < 8 and white:    #back rank
            print("Error: unpromoted Pawn")
            return path   #Cannot, return home square
        x = home
        while x < 64:   #exit if off the board
            x -= 8  #forward 1
            if board[x] == ' ':
                path.append(x)
            else:
                break
            if white and x < 40:  #more than 1 step from starting position
                break
        if home not in fileH:   #connot move right from file h
            x = home - 7    #forward right
            if board[x] in xblack:
                path.append(x)
        if home not in fileA:   #cannot move left from file A
            x = home - 9    #forward left
            if board[x] in xblack:
                path.append(x)
    else:   #backwards
        if not white and home > 56:    #back rank
            print("Error: unpromoted Pawn")
            return path   #Cannot move, return home square
        x = home
        while x < 64:   #exit if off the board
            x += 8
            if board[x] == ' ':
                path.append(x)
            else:
                break
            if not white and x > 23:  #more than 1 step from starting position
                break
        if home not in fileA:   #connot move left from file A
            x = home + 7    #back left
            if board[x] in xwhite:
                path.append(x)
        if home not in fileH:  #connot move right from file H
            x = home + 9    #back right
            if board[x] in xwhite:
                path.append(x)
    return path

#Promote Pawn On Back Rank
def PromotePawn():
    if white:
        p = 'Q' #Default promotion
        options = xwhite
        options.remove('P')    #Possible promotions
        if b > 7:
            return 'P'  #Pawn cannot be promoted
        print("The Pawn on", square, "is ready to be promoted!")
        p = input("Enter new piece: ")
        if p in options:
            return p
        elif p == 'r':  #Chose Rook, wrong case
            return 'R'
        elif p == 'b':  #Chose Bishop, wrong case
            return 'B'
        elif p == 'n':  #Chose Night, wrong case
            return 'N'
        else:   #defaults to Queen (also catches 'q')
            print("Promoted", square, "to Queen")
            return 'Q'
    else:   #black
        p = 'q' #Default promotion
        options = xblack
        options.remove('p')    #Possible promotions
        if b < 56:
            return 'p'  #Pawn cannot be promoted
        print("The Pawn on", square, "is ready to be promoted!")
        p = input("Enter new piece: ")
        if p in options:
            return p
        elif p == 'R':  #Chose Rook, wrong case
            return 'r'
        elif p == 'B':  #Chose Bishop, wrong case
            return 'b'
        elif p == 'N':  #Chose Night, wrong case
            return 'n'
        else:   #defaults to Queen (also catches 'Q')
            print("Promoted", square, "to Queen")
            return 'q'

#Returns the squares a Knight can move to
def KnightMoves(home, forwards):
    path = [home]
    if home < 48:   #ranks 3-8
        if home not in fileA:
            x = home + 15  #down 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home + 17  #down 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    if home > 15:   #ranks 1-6
        if home not in fileA:
            x = home - 17  #up 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home - 15  #up 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    if home not in fileA and home not in fileB:
        print("Not A nor B")
        if home > 7:
            x = home - 10   #left 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 6   #left 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    if home not in fileG and home not in fileH:
        print("Not G nor H")
        if home > 7:
            x = home - 6   #right 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 10   #right 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    return path

#Returns the squares a Bishop can move to
def BishopMoves(home, forwards):
    path = [home]
    x = home
    while x not in fileA and x > 7: #move up and left until reaching file A or rank 8
        x -= 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x > 7: #move up and right until reaching file H or rank 8
        x -= 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileA and x < 56: #move down and left until reaching file A or rank 1
        x += 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x < 56: #move down and right until reaching file H or rank 1
        x += 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not white and board[x] in xwhite:
                path.append(x)
            break
    return path

#Returns the squares a Rook can move to
def RookMoves(home, forwards):
    path = [home]
    x = home
    while x not in fileA: #move left until reaching file A
        x -= 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH: #move right until reaching file H
        x += 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x > 7: #move up until reaching rank 8
        x -= 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x < 56: #move down until reaching rank 1
        x += 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
            break
    return path

#Returns the squares a Queen can move to
def QueenMoves(home, fwd):
    pathR = RookMoves(home, fwd)
    pathR.remove(home, fwd)
    pathB = BishopMoves(home, fwd)
    path = pathR + pathB
    return path

#Returns the squares a King can move to
def KingMoves(home, forwards):
    path = [home]
    if home > 7:    #not in rank 8
        if home not in fileA:
            x = home - 9    #up 1 left 1
            if board[x] == ' ':
                path.append(x)
            else:
                if forwards and board[x] in xblack:
                    path.append(x)
                elif not forwards and board[x] in xwhite:
                    path.append(x)
        x = home - 8    #up 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home - 7    #up 1 right 1
            if board[x] == ' ':
                path.append(x)
            else:
                if forwards and board[x] in xblack:
                    path.append(x)
                elif not forwards and board[x] in xwhite:
                    path.append(x)
    if home not in fileA:
        x = home - 1    #left 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    if home not in fileH:
        x = home + 1    #right 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
    if home < 56:   #not in rank 1
        if home not in fileA:
            x = home + 7    #down  left 1
            if board[x] == ' ':
                path.append(x)
            else:
                if forwards and board[x] in xblack:
                    path.append(x)
                elif not forwards and board[x] in xwhite:
                    path.append(x)
        x = home + 8    #down 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards and board[x] in xblack:
                path.append(x)
            elif not forwards and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home + 9    #down 1 right 1
            if board[x] == ' ':
                path.append(x)
            else:
                if forwards and board[x] in xblack:
                    path.append(x)
                elif not forwards and board[x] in xwhite:
                    path.append(x)
    #Add castling:
    #if not in check
    #if nothing kingside
        #if rook kingside
        #if nothing in the way
        #if destination isn't in check
        #if path not in check
            #add new square for king
    return path

#Checks if a square can be attacked by an opponents piece
def CheckCheck(throne, color):
    if color:
        for x in xblack:
            threat = BackTrack(throne, x)
            if threat != []:
                return True
    else:
        for x in xwhite:
            threat = BackTrack(throne, x)
            if threat != []:
                return True
    return False

#Determins if the King can Castle Kingside or Queenside
def CastleCheck(color):
    options = [False,False]
    if color: #white
        if home != 59: #White King is not on starting square
            return [False,False]
        if board[56] != 'R':
            options[0] = False
        #check Kingside rook
        #check queenside rook
        #check squares in between
        #check in check
        #check destination in check
        #check pass through check
    else: #black
        if home != 3: #Black King is not on starting square
            return [False,False]

#MAIN BODY
#Get Board Configuration
board = GetBoard()
good = ValidBoard(board)
while not good:
    print("Sorry, that board configuration is not recognised. Please Try again.")
    board = GetBoard()
    good = ValidBoard(board)
ShowBoard(board)
#Get Color Being Played
q = input ("Are you playing White (W) or Black (B)? ")
if q == 'B' or q == 'b':    #Black selected
    white = False
    move = input("Black to move (enter algebraic notation): ")
else:    #Defaults to white
    move = input("White to move (enter algebraic notation): ")
#Parse Move
if move[-1] == '+' or move [-1] == '#':
    check = True
    square = move[-3:-2]
elif move[-1] == '0' or move[-1] == 'o' or move[-1] == 'O':    #Castle
    if len(move) < 5:    #King side
        if white:
            square = 'g1'
        else:
            square = 'g8'
    else:    #Queen side
        if white:
            square = 'd1'
        else:
            square = 'd8'
else:
    square = move[-2:]
if move[1] == 'x' or move[1] == 'X':
    capture = True
if move[0] == 'K' or move[0] == 'k' or move[0] == '0' or move[0] == 'O' or move[0] == 'o':
    if white:
        piece = 'K'
    else: piece = 'k'
elif move[0] == 'Q' or move[0] == 'q':
    if white:
        piece = 'Q'
    else:
        piece = 'q'
elif move[0] == 'R' or move[0] == 'r':
    if white:
        piece = 'R'
    else:
        piece = 'r'
elif move[0] == 'N' or move[0] == 'n':
    if white:
        piece = 'N'
    else:
        piece = 'n'
elif move[0] == 'B' and move[1].isdigit() == False:
    if white:
        piece = 'B'
    else:
        piece = 'b'
elif move[0] == 'a' or move[0] == 'b' or move[0] == 'c' or move[0] == 'd' or move[0] == 'e' or move[0] == 'f' or move[0] == 'g' or move[0] == 'h' or move[0] == 'P' or move[0] == 'p':
    if white:
        piece ='P'
    else:
        piece = 'p'
else:
    print("Error: could not parse move notation: ", move)
#Validate Selected Square
b = int(BoardIndex(square))
if b == 64:    #Indicates error
    print("Error: ", square, " not found on board")
#Validate Capture
if board[b] != ' ': #A piece already occupies that square
    move = ValidCapture(board[b])
    if move == False:
        print("Error: invalid capture")
options = BackTrack(b, piece)
if len(options) == 1:
    a = options[0]
elif len(options) > 1:
    start = input("Multiple pieces can make that move. Please enter the location of the intended piece: ")
    a = BoardIndex(start)
    good = ValidPath(piece,a,b)
    if not good:
        print("Error: the", piece, "on ", start, "cannot move to", square)
        a = 64
else:
    print("Error: could not find a", piece, "that can move to", square)
if piece == 'P' and b < 8 or piece == 'p' and b > 55:   #"and" is evaluated before "or" in a multiple conditional statement
    piece = PromotePawn()
if white:
    king = FindPieces('K')
else:
    king = FindPieces('k')
good = CheckCheck(king, white)
if not good:
    print("Invalid move: your King is in check!")
if a < 64:
    ShowBoard(board)
    print('\n')
    board_new = board    #Save previous version of board (still need to verify no check)
    board_new[a] = ' '  #Starting square is now empty
    board_new[b] = piece    #Piece is now in the new location
    ShowBoard(board_new) #For testing
    #if king is in check after moving, invalid move "[move] leaves your king in check"
        #Need to check every opponent piece, except the King (xblack or xwhite)
