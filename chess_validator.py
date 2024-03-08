#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-03-07
#
#Need to add:
    #Fully parse FEN:
        #Active color
        #Track castling (replace CheckCastle?)
        #En passant target square
        #Number of halfmoves (ply) since last capture or pawn movement
        #Fullmove number
    #Identify checkmate
        #Identify all possible moves
        #Try each one and check for checkmate
        #If list of options is [], then checkmate
        #Declare winned are end game
    #game over:
        #checkmate
        #resignation
        #stalemate (no leagal moves)
        #draw no Pawn moves or captures in 50 moves, 3 move repetition
        #insufficient material:
            #King
            #King + Bishop
            #King + Knight
            #King + 2 Knights vs King
            #in other words, you need a King and [(two or more pieces)** or (Rook or Queen or Pawn)] **except King and Knight and Knight vs King
#More Ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers and defenders are there on each piece
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
fileC = [2,10,18,26,34,42,50,58] #Board indexes for C-file
fileD = [3,11,19,27,35,43,51,59] #Board indexes for D-file
fileE = [4,12,20,28,36,44,52,60] #Board indexes for E-file
fileF = [5,13,21,29,37,45,53,61] #Board indexes for F-file
fileG = [6,14,22,30,38,46,54,62]    #Board indexes for G-file
fileH = [7,15,23,31,39,47,55,63]    #Board indexes for H-file (edge of board)
ranks = ['a','b','c','d','e','f','g','h']
locations = [0,0,0,0,0,0,0,0,0,0]   #Number and locations of pieces
#move = 'e4'    #Chess move in algebraic notation
#piece = 'P' #Letter indicating piece (capitalization indicates color)
#square = 'e4'    #Selected square on the board (algebraic notation)
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
    elif fen == 'T' or fen == 't':
        fen = "r3k2r/8/4n3/3P1P2/8/8/8/R3K2R"
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

#Get Chess Move in Algebraic Notation:
def GetMove():
    #Get move from user
    if white:
        move = input("White to move (enter algebraic notation): ")
    else:    #Defaults to white
        move = input("Black to move (enter algebraic notation): ")
    #Check for resignation
    if move == "resign":    #resign game (exit)
        return "resign"
    #Remove '+' or '#'
    if move[-1] == '+' or move [-1] == '#':
        move.pop()    #Removes last character
    #Handle castling
    if move[0] == '0' or move[0] == 'o' or move[0] == 'O':
        if white:
            piece = 'K'
            if len(move) < 5:   #kingside
                destination = 62  #g1 = 62
            else:   #queenside
                destination = 58  #c1 = 58
        else:   #black
            piece = 'k'
            if len(move) < 5:   #kingside
                destination = 6 #g8 = 6
            else:   #queenside
                destination = 2 #c8 = 2
        return [piece, destination, piece, True, '']
    #Remove 'x' or 'X' (will determine capturing later)
    if 'x' in move:
        move = move.replace('x','')
    elif 'X' in move:
        move = move.replace('X','')
    #Determine piece
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
        if '=' in move:
            promo = move.pop()
            move.remove('=')
        else:
            promo = ''
        if white:
            piece ='P'
            if promo not in xwhite:
                promo = 'P' #invalid promotion, default to pawn
        else:
            piece = 'p'
            if promo not in xblack:
                promo = 'p'  #invalid promotion, default to pawn
    else:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find piece")
        #continue    #try again
    if piece != 'P' and piece != 'p':   #if  not a pawn
        promo = piece   #set promotion piece to itself (failsafe)
    #Determine square
    sq = move[-2:]
    #Validate square
    try:
        rank = int(move[-1])
    except ValueError:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
        #continue   #try again
    if move[-2] not in ranks:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
        #continue   #try again
    col = move[-2]
    #Convert square to number
    destination = BoardIndex(sq)
    return [piece, destination, promo, False, col]  #capture, check, checkmate can be calculated

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
        spot = 'a'
    elif i % 8 == 1:
        spot = 'b'
    elif i % 8 == 2:
        spot = 'c'
    elif i % 8 == 3:
        spot = 'd'
    elif i % 8 == 4:
        spot = 'e'
    elif i % 8 == 5:
        spot = 'f'
    elif i % 8 == 6:
        spot = 'g'
    else:
        spot = 'h'
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
            return True
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
            return True
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
    loc = []   #Count and up to 9 locations, 64 is off the board
    i = 0
    while i < 64:
        if board[i] == p:
            loc.append(i)
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
def BackTrack(destination, type, color, col):
    origins = []
    color = not color   #include your own pieces, not your opponents
    if type == 'P' or type == 'p':
        reach = PawnMoves(destination, color)
        if col == 'a':   #find file if the piece is a Pawn
            file = fileA
        elif col == 'b':
            file = fileB
        elif col == 'c':
            file = fileC
        elif col == 'd':
            file = fileD
        elif col == 'e':
            file = fileE
        elif col == 'f':
            file = fileF
        elif col == 'g':
            file = fileG
        elif col == 'h':
            file = fileH
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
        #print("i:",i,"reach[i]:",reach[i])  #for testing
        if board[reach[i]] == type:
            if (type == 'P' or type == 'p') and col in ranks:   #check a valid column is selected and the piece is a Pawn
                if reach[i] in file:    #only include Pawn in list if it is in the indicated file (e.g. cxd4 only includes Pawns in the c file)
                    origins.append(reach[i])
            else:   #will include all Pawns in range if a file isn't selected
                origins.append(reach[i])
        i += 1
    #print("reach is:", reach,", origins is:", origins)  #for testing
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
    #print(type, "on", origin, "can reached:")   #for testing
    #print(reach)    #for testing
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
        #x = home
        x = home - 8
        while x > -1:   #exit if off the board
            #x -= 8  #forward 1
            if board[x] == ' ':
                path.append(x)
            else:
                break
            if white and x < 40:  #more than 1 step from starting position
                break
            x -= 8
        if home not in fileH:   #connot move right from file h
            x = home - 7    #forward right
            if x > -1 and board[x] in xblack:
                path.append(x)
        if home not in fileA:   #cannot move left from file A
            x = home - 9    #forward left
            if x > -1 and board[x] in xblack:
                path.append(x)
    else:   #backwards
        if not white and home > 56:    #back rank
            print("Error: unpromoted Pawn")
            return path   #Cannot move, return home square
        #x = home
        x = home + 8
        while x < 64:   #exit if off the board
            #x += 8
            if board[x] == ' ':
                path.append(x)
            else:
                break
            if not white and x > 23:  #more than 1 step from starting position
                break
            x += 8
        if home not in fileA:   #connot move left from file A
            x = home + 7    #back left
            if x < 64 and board[x] in xwhite:
                path.append(x)
        if x < 64 and home not in fileH:  #connot move right from file H
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
        #print("Not A nor B")   #for testing
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
        #print("Not G nor H")   #for testing
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
    #print("x =",x) #for testing
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
    pathR.remove(home)
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
    castles = CastleCheck(white)
    print("Castle:", castles)   #for testing
    if white:   #white
        if forwards:
            if castles[0]:
                path.append(62) #kingside
            if castles[1]:
                path.append(58) #queenside
        else:   #backwards
            #if castles[0] or castles[1]:
            #    path.append(60) #white king starting square
            if castles[0] and home == 62:  #backtracking, kingside
                path.append(60)
            if castles[1] and home == 58:  #backtracking, queenside
                path.append(60)
    else:   #black
        if not forwards:
            if castles[0]:
                path.append(6) #kingside
            if castles[1]:
                path.append(2) #queenside
        else:   #backwards
            #if castles[0] or castles[1]:
            #    path.append(4)  #white king starting square
            if castles[0] and home == 6:  #backtracking, kingside
                path.append(4)
            if castles[1] and home == 2:  #backtracking, queenside
                path.append(4)
    print("King moves:", path)  #for testing
    return path

#Checks if a square can be attacked by an opponents piece
def CheckCheck(throne, color):
    if color:
        for x in xblack:
            threat = BackTrack(throne, x, not white, '')
            print("Threats from",x,threat)  #for testing
            if threat != []:
                return True
    else:
        for x in xwhite:
            threat = BackTrack(throne, x, not white, '')
            print("Threats from",x,threat)  #for testing
            if threat != []:
                return True
    return False

#Checks if a square can be attacked by an opponents piece
def Attackers(target, color):
    threat = []
    if color:
        for x in xblack:
            threat.append(BackTrack(target, x, not white), '')
    else:
        for x in xwhite:
            threat.append(BackTrack(target, x, not white), '')
    return threat

#Determins if the King can Castle Kingside or Queenside
def CastleCheck(color):
    options = [True, True]
    if color:   #white
        if board[60] != 'K':    #White King is not on starting square
            return [False, False]
        if board[63] == 'R':    #Kingside Rook
            c = 60
            while c < 63:
                if c > 60 and board[c] != ' ':
                    options[0] = False   #a piece is between the king and the rook
                    break
                bad = CheckCheck(c, color)
                print("Check for",c,"is",bad)   #for testing
                if bad:
                    options[0] = False #No castling Kingside
                    break
                c += 1
        else:
            options[0] = False
        if board[56] == 'R':    #Queenside Rook
            c = 60
            while c > 56:
                if c < 60 and board[c] != ' ':
                    options[1] = False   #a piece is between the king and the rook
                    break
                bad = CheckCheck(c, color)
                print("Check for",c,"is",bad)   #for testing
                if bad and c > 57:
                    options[1] = False #No castling Kingside
                    break
                c -= 1
        else:
            options[1] = False
    else: #black
        if board[4] != 'k':    #White King is not on starting square
            return [False, False]
        if board[7] == 'r':    #Kingside Rook
            c = 4
            while c < 7:
                if c > 4 and board[c] != ' ':
                    options[0] = False   #a piece is between the king and the rook
                    break
                bad = CheckCheck(c, color)
                print("Check for",c,"is",bad)   #for testing
                if bad:
                    options[0] = False #No castling Kingside
                    break
                c += 1
        else:
            options[0] = False
        if board[0] == 'r':    #Queenside Rook
            c = 4
            while c > 0:
                if board[c] != ' ':
                    options[1] = False   #a piece is between the king and the rook
                    break
                bad = CheckCheck(c, color)
                print("Check for",c,"is",bad)   #for testing
                if bad and c > 1:
                    options[1] = False #No castling Kingside
                    break
                c -= 1
        else:
            options[1] = False
    return options

#Updates the board with requested move
def MakeMove(original, type, start, end, castling):
    updated = original
    #Promote Pawn
    if type == 'P' and end < 8 or type == 'p' and end > 55:   #"and" is evaluated before "or" in a multiple conditional statement
        if promotion != 'p' and promotion != 'P':
            type = promotion
        else:
            type = PromotePawn()
    #Update board:
    updated[start] = ' '
    updated[end] = type
    #Castle:
    if castling:    #castling
        print("Castling")   #for testing
        if end == 62:   #white kingside
            updated[61] = 'R'
            updated[63] = ' '
        elif end == 58: #white queenside
            updated[59] = 'R'
            updated[56] = ' '
        elif end == 6:  #black kingside
            updated[5] = 'r'
            updated[7] = ' '
        elif end == 2:  #black queenside
            updated[3] = 'r'
            updated[0] = ' '
    return updated

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
else:
    white = True
fmn = 0
ply = 0
while ply < 50:   #counts ply since last capture or Pawn movement
    q = GetMove()
    if q == "resign": #resign game (exit)
        print("Resigning game...")
        break
    else:
        chessman = q[0]
        b = q[1]
        promotion = q[2]
        castle = q[3]
        rank = q[4]
    square = BoardAlgebraic(b)  #get algebratic notation for user feedback (error messages)
    #Validate Selected Square
    if b >= len(board):    #off the board
        print("Error: ", square, " not found on board")
        continue    #loop without switching (try again)
    #Validate Capture
    if board[b] != ' ': #A piece already occupies that square
        good = ValidCapture(board[b])
        if good:
            capture = True
        else:
            print("Error: connot capture", board[b], "on square", square)
            continue    #loop without switching (try again)
    options = BackTrack(b, chessman, white, rank)
    if len(options) == 1:
        a = options[0]
    elif len(options) > 1:
        start = input("Multiple pieces can make that move. Please enter the location of the intended piece: ")
        a = BoardIndex(start)
        good = ValidPath(chessman, a, b)
        if not good:
            print("Error: the", chessman, "on ", start, "cannot move to", square)
            continue    #loop without switching (try again)
    else:
        print("Error: could not find a", chessman, "that can move to", square)
        continue    #loop without switching (try again)
    if chessman == 'P' and b < 8 or chessman == 'p' and b > 55:   #"and" is evaluated before "or" in a multiple conditional statement
        if promotion != 'p' and promotion != 'P':
            chessman = promotion
        else:
            chessman = PromotePawn()
    OldBoard = board
    board = MakeMove(board, chessman, a, b, castle)
    if white:
        king = FindPieces('K')
    else:
        king = FindPieces('k')
    good = not CheckCheck(king[0], white)
    if not good:
        print("Invalid move: your King is in check!")
        board = OldBoard
        continue    #loop without switching (try again)
    #show corrected move (including check, checkmate, castling, pawn promotion)
    ShowBoard(board)
    white = not white   #switch colors for next player
    ply += 1
    if capture or chessman == 'p' or chessman == 'P':
        ply = 0 #reset 
    if not white:
        fmn += 1    #increment full move number
