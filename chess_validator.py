'''
#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-06-09
'''
#Need to fix:
    #can't find King (backtracking)
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
        #Declare winner and end game
    #game over:
        #checkmate
        #[x] resignation
        #stalemate (no leagal moves)
        #[x] draw) no Pawn moves or captures in 50 moves, 3 move repetition)
        #insufficient material:
            #King
            #King + Bishop
            #King + Knight
            #King + 2 Knights vs King
            #summary: you need a major piece (or Pawn) or two minor pieces (except K vs K and 2N)
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
ep = '' #En passant target square
fileA = [0,8,16,24,32,40,48,56] #Board indexes for A-file (edge of board)
fileB = [1,9,17,25,33,41,49,57] #Board indexes for B-file
fileC = [2,10,18,26,34,42,50,58] #Board indexes for C-file
fileD = [3,11,19,27,35,43,51,59] #Board indexes for D-file
fileE = [4,12,20,28,36,44,52,60] #Board indexes for E-file
fileF = [5,13,21,29,37,45,53,61] #Board indexes for F-file
fileG = [6,14,22,30,38,46,54,62]    #Board indexes for G-file
fileH = [7,15,23,31,39,47,55,63]    #Board indexes for H-file (edge of board)
ranks = ['a','b','c','d','e','f','g','h']
board = []    #Chess board configuration
board_old = []
xblack = ['q','r','b','n','p']    #Capturable black pieces list (no King)
xwhite = ['Q','R','N','B','P']    #Capturable white pieces list (no King)
pieces = ['K', *xwhite, 'k', *xblack]    #Valid chess pieces list

#FUNCTIONS
def get_board():
    '''Get Chess Board Setup'''
    build = []
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Default starting position
    fen = input("Enter D for default starting position, or board configuration in FEN notation: ")
    if fen in ['D','d']:
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Chess starting position
    i = 0    #Position in fen array
    j = 0    #Board position
    while j < 64 and i < len(fen):    #Populate board array from FEN string
        if fen[i] == '/':    #Next rank
            if j % 8 != 0:    # '/' character encountered midway through a rank
                print("Error: unexpected / in the board configuration:")
                print(fen)
                break
            i += 1    #Ignore and go to to next character
        elif fen[i].isdigit():
            if int(fen[i]) > 8:    #More than 8 empty squares in a rank
                print("Error: extra empty squares in the board configuration:")
                print(fen)
                break
            k = 0    #Number of empty squares added to rank
            while k < int(fen[i]):    #Add specified number of empty squares to board array
                build.append(' ')
                k += 1
                j += 1
            i += 1    #Go to next character after adding empty squares
        elif fen[i] in pieces:    #Checks if character indicates valid chess piece
            build.append(fen[i])
            i += 1
            j += 1
        else:
            print("Error: ", fen[i], " is not a recognized piece.")
            break
    return build

def valid_board(brd: str):
    '''Validate Chess Board Configuration'''
    if len(brd) != 64:
        print("Error: incomplete board")    #Board array should have 64 elements
        return False
    for i in pieces:
        k = 0
        for j in brd:
            if i == j:
                k += 1
        if k > 9:
            print("Error: excessive number of ", i)
            return False
        if i in ['P', 'p'] and k > 8:
            print("Error: more than 8 Pawns")
            return False
        if i == 'k' and k != 1:
            print("Error: there should be exactly 1 black King. Found ", k)
            return False
        if i == 'K' and k != 1:
            print("Error: there should be exactly 1 white King. Found ", k)
        else:
            return True

def show_board(brd: str):
    '''Display Chess Board on Terminal Screen'''
    i = 0    #Board position
    while i < 64:    #Display board
        print(brd[i:i+8])
        i += 8

def get_move():
    '''Get Chess Move in Algebraic Notation'''
    move = ''
    col = ''
    while move == '':   #keep prompting for a move if nothing is entered
        if white:
            move = input("White to move (enter algebraic notation): ")
        else:    #black
            move = input("Black to move (enter algebraic notation): ")
    #Check for resignation
    if move == "resign":    #resign game (exit)
        return "resign" #exit module?
    #Remove '+' or '#'
    if move[-1] == '+' or move [-1] == '#':
        move.pop()    #Removes last character
    #Handle castling
    if move[0] == '0' or move[0] == 'o' or move[0] == 'O':
        print("Castling...")
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
    elif move[0] == 'B' and move[1].isdigit() is False:
        if white:
            piece = 'B'
        else:
            piece = 'b'
    elif move[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'P', 'p']:
        if '=' in move:
            promo = move.pop()
            move.remove('=')
        else:
            promo = ''
        col = move[-2]
        if white:
            piece ='P'
            if promo not in xwhite:
                promo = 'P' #invalid promotion, default to pawn
        else:
            piece = 'p'
            if promo not in xblack:
                #Add case change? (e.g. Q --> q)
                promo = 'p'  #invalid promotion, default to pawn
    else:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find piece")
        #continue    #try again
    if piece not in ['P', 'p']:   #if  not a pawn
        promo = piece   #set promotion piece to itself (failsafe)
        col = move[1]
    #Determine square
    sq = move[-2:]
    print("move is: ", move)
    #Validate square
    try:
        row = int(move[-1])
        sq = col + str(row)
    except ValueError:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
        #continue   #try again
    if move[-2] not in ranks:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
        #continue   #try again
    #col = move[-2]
    #Convert square to number
    destination = board_index(sq)
    return [piece, destination, promo, False, col]  #capture, check, checkmate can be calculated

def board_index(sq: str):
    '''Convert Algebraic Notated Square to Board Index Number'''
    if len(sq) != 2:    #Board location should be 2 characters in algebraic notation
        return 64    #Invalid index indicating error
    if not sq[1].isdigit: #Second digit in location should be a number
        return 64
    if int(sq[1]) != 0 and int(sq[1]) != 9: #Rank 1-8
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
        return i

def board_algebraic(i: int):
    '''Convert Board Index to Algebraic Notation'''
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

def valid_capture(p):
    '''Verify Piece Can Be Captured'''
    global ep
    global b
    if b == ep:
        return True
    if white:
        if p in xblack:
            return True
        if p == 'k':
            print("You cannot capture the King")
        elif p in xwhite or p == 'K':
            print("Your ", p, " is already on ", square)
        else:
            print("Something went wrong. ", p, " is on ", square)
            return False
    else:   #black
        if p in xwhite:
            return True
        if p == 'K':
            print("You cannot capture the King")
        elif p in xblack or p == 'k':
            print("Your ", p, " is already on ", square)
        else:
            print("Something went wrong. ", p, " is on ", square)
            return False

def find_pieces(p):
    '''Find the Number and Locations of Pieces "p"'''
    loc = []   #Count and up to 9 locations, 64 is off the board
    i = 0
    while i < 64:
        if board[i] == p:
            loc.append(i)
        i += 1
    return loc

def back_track(destination: int, cm, color: bool, col):
    '''Backtracks path for that type of piece, and returns the locations of those pieces'''
    origins = []
    color = not color   #include your own pieces, not your opponents
    if cm in {'P','p'}:
        reach = pawn_moves(destination, False)
        print("Pawn reach:", reach) #for testing
        if col == 'a':   #find file if the piece is a Pawn
            col = fileA
        elif col == 'b':
            col = fileB
        elif col == 'c':
            col = fileC
        elif col == 'd':
            col = fileD
        elif col == 'e':
            col = fileE
        elif col == 'f':
            col = fileF
        elif col == 'g':
            col = fileG
        elif col == 'h':
            col = fileH
        else:
            col = list(range(64))  #if col isn't recognized, file includes whole board
    elif cm in {'B','b'}:
        reach = bishop_moves(destination, False)
    elif cm in {'N','n'}:
        reach = knight_moves(destination, False)
    elif cm in {'R','r'}:
        reach = rook_moves(destination, False)
    elif cm in {'Q','q'}:
        reach = queen_moves(destination, False)
    elif cm in {'K','k'}:
        reach = king_moves(destination, False)
    i = 0
    while i < len(reach):   #itterate through piece's range
        if board[reach[i]] == cm:
            if cm in {'P','p'}:    # and col in file:   #check valid file, piece is a Pawn
                if reach[i] in col:    #only include Pawn in file indicated in entered move
                    origins.append(reach[i])
            else:
                origins.append(reach[i])
        i += 1
    return origins

def valid_path(cm, origin: int, destination: int):
    '''Checks if a piece can move from origin to destination in a single move'''
    reach = [origin]
    if cm in {'P','p'}:
        reach = pawn_moves(origin, True)
    elif cm in {'B','b'}:
        reach = bishop_moves(origin, True)
    elif cm in {'N','n'}:
        reach = knight_moves(origin, True)
    elif cm in {'R','r'}:
        reach = rook_moves(origin, True)
    elif cm in 'Q' or cm == 'q':
        reach = queen_moves(origin, True)
    elif cm in {'K','k'}:
        reach = king_moves(origin, True)
    else:
        print("Error: couldn't determine possible moves for", cm, "on", origin)
    return bool(destination in reach)

def pawn_moves(home: int, forwards: bool):
    '''Returns the squares a Pawn can move to from starting square home'''
    path = [home]
    if home < 8 or home > 55:
        return []   #not a valid Pawn rank, return null array
    if capture:
        if forwards == white:  #True if white forwards or black backwards
            if home not in fileH:   #can move right
                x = home - 7    #forward right
                if board[x] in xblack:
                    path.append(x)
            if home not in fileA:   #can move left
                x = home - 9   #forward left
                if board[x] in xblack:
                    path.append(x)
        elif forwards ^ white: #XOR: white and backwards or black and forwards
            if home not in fileA:  #can move left
                x = home + 7   #backward left
                if board[x] in xwhite:
                    path.append(x)
            if home not in fileH:   #can move right
                x = home + 9   #backward right
                if board[x] in xwhite:
                    path.append(x)
    else:   #straight
        #global ep
        x = home
        while True:
            if forwards == white:  #True if white forwards or black backwards
                x -= 8 #forwards
                if not white:  #black backwards
                    if board[x] == 'p': #found a matching color Pawn
                        path.append(x)
                        break  #Pawns can't jump eachother
            elif forwards ^ white: #XOR: white and backwards or black and forwards
                x += 8 #backwards
                if white:  #white backwards
                    if board[x] == 'P':    #found a matching color Pawn
                        path.append(x)
                        break  #Pawns can't jump eachother
            if board[x] == ' ':
                path.append(x)
            else:  #blocked, stop moving
                break
            if white:  #white
                if x < 40 or x > 47: #white can only take one more step if on rank 3
                    break
                #ep = x #set en passant target
            else:  #black
                if x < 16 or x > 23: #black can only take one more step if on rank 6
                    break
                #ep = x #set en passant target
    return path

def promote_pawn():
    '''Promote pawn on the back rank'''
    if white:
        p = 'Q' #Default promotion
        promotions = xwhite
        promotions.remove('P')    #Possible promotion
        if b > 7:
            return 'P'  #Pawn cannot be promoted
        print("The Pawn on", square, "is ready to be promoted!")
        p = input("Enter new piece: ")
        if p in promotions:
            return p
        if p == 'r':  #Chose Rook, wrong case
            return 'R'
        if p == 'b':  #Chose Bishop, wrong case
            return 'B'
        if p == 'n':  #Chose Night, wrong case
            return 'N'
        print("Promoted", square, "to Queen")   #defaults to Queen (also catches 'q')
        return 'Q'
    else:   #black
        p = 'q' #Default promotion
        promotions = xblack
        promotions.remove('p')    #Possible promotions
        if b < 56:
            return 'p'  #Pawn cannot be promoted
        print("The Pawn on", square, "is ready to be promoted!")
        p = input("Enter new piece: ")
        if p in promotions:
            return p
        if p == 'R':  #Chose Rook, wrong case
            return 'r'
        if p == 'B':  #Chose Bishop, wrong case
            return 'b'
        if p == 'N':  #Chose Night, wrong case
            return 'n'
        print("Promoted", square, "to Queen")   #defaults to Queen (also catches 'Q')
        return 'q'

def knight_moves(home: int, forwards: bool):
    '''Returns the squares a Knight can move to from starting square home'''
    path = [home]
    if home < 48:   #ranks 3-8
        if home not in fileA:
            x = home + 15  #down 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack: #forwards & white or backtrack & black
                path.append(x)
            elif forwards ^ white and board[x] in xwhite: #forwards & black or backtrack & white
                path.append(x)
        if home not in fileH:
            x = home + 17  #down 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
    if home > 15:   #ranks 1-6
        if home not in fileA:
            x = home - 17  #up 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home - 15  #up 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
    if home not in fileA and home not in fileB:
        if home > 7:
            x = home - 10   #left 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 6   #left 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
    if home not in fileG and home not in fileH:
        if home > 7:
            x = home - 6   #right 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 10   #right 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
    return path

def bishop_moves(home: int, forwards: bool):
    '''Returns the squares a Bishop can move to from starting square home'''
    path = [home]
    x = home
    while x not in fileA and x > 7: #move up and left until reaching file A or rank 8
        x -= 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x > 7: #move up and right until reaching file H or rank 8
        x -= 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileA and x < 56: #move down and left until reaching file A or rank 1
        x += 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x < 56: #move down and right until reaching file H or rank 1
        x += 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    return path

def rook_moves(home: int, forwards: bool):
    '''Returns the squares a Rook can move to'''
    path = [home]
    x = home
    while x not in fileA: #move left until reaching file A
        x -= 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH: #move right until reaching file H
        x += 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x > 7: #move up until reaching rank 8
        x -= 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x < 56: #move down until reaching rank 1
        x += 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == white and board[x] in xblack:
                path.append(x)
            elif forwards ^ white and board[x] in xwhite:
                path.append(x)
            break
    return path

def queen_moves(home: int, fwd: bool):
    '''Returns the squares a Queen can move to'''
    pathR = rook_moves(home, fwd)
    pathR.remove(home)
    pathB = bishop_moves(home, fwd)
    path = pathR + pathB
    return path

def king_moves(home: int, forwards: bool):
    '''Returns the squares a King can move to'''
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
    castles = castle_check(white)
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

def check_check(throne: int, color: bool):
    '''Checks if a square can be attacked by an opponents piece'''
    threats = attackers(throne,color)
    return bool(not threats)

def attackers(target: int, color: bool):
    '''Checks for opponent pieces which can attack the target square'''
    threat = []
    if color:
        for x in xblack:
            threat.append(back_track(target, x, not white, ''))
    else:
        for x in xwhite:
            threat.append(back_track(target, x, not white, ''))
    return threat

def castle_check(color: bool):
    '''Determins if the King can Castle Kingside or Queenside'''
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
                bad = check_check(c, color)
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
                bad = check_check(c, color)
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
                bad = check_check(c, color)
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
                bad = check_check(c, color)
                print("Check for",c,"is",bad)   #for testing
                if bad and c > 1:
                    options[1] = False #No castling Kingside
                    break
                c -= 1
        else:
            options[1] = False
    return options

#Updates the board with requested move
def MakeMove(original: str, type: bool, start: int, end: int, castling: bool):
    updated = original
    global ep
    global white
    #Promote Pawn
    if type == 'P' and end < 8 or type == 'p' and end > 55:   #"and" is evaluated before "or"
        if promotion != 'p' and promotion != 'P':
            type = promotion
        else:
            type = promote_pawn()
    #Update Board
    updated[start] = ' '
    updated[end] = type
    #En Passant
    if end == ep:
        if white:
            updated[end+8] = ' '    #remove pawn from previous rank
        else:
            updated[end-8] = ' '    #remove pawn from next rank
        ep = '' #clear ep target square
    #Castle
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
board = get_board()
good = valid_board(board)
while not good:
    print("Sorry, that board configuration is not recognised. Please Try again.")
    board = get_board()
    good = valid_board(board)
show_board(board)
#Get Color Being Played
white - True    #defaults to white
q = input ("Are you playing White (W) or Black (B)? ")
if q == 'B' or q == 'b':    #Black selected
    white = False
fmn = 0
ply = 0
while ply < 50:   #counts ply since last capture or Pawn movement
    capture = False #reset capture
    check = False   #reset check
    a = 52  #
    q = get_move()
    if q == "resign": #resign game (exit)
        print("Resigning game...")
        break
    else:
        chessman = q[0]
        b = q[1]
        promotion = q[2]
        castle = q[3]
        file = q[4]
    square = board_algebraic(b)  #get algebratic notation for user feedback (error messages)
    #Validate Selected Square
    if b >= len(board):    #off the board
        print("Error: ", square, " not found on board")
        continue    #loop without switching (try again)
    #Validate Capture
    if b == ep or board[b] != ' ': #Move attempts to capture
        good = valid_capture(board[b])
        if good:
            capture = True
        else:
            print("Error: connot capture", board[b], "on square", square)
            continue    #loop without switching (try again)
    options = back_track(b, chessman, white, file)
    if len(options) == 1:
        a = options[0]
    elif len(options) > 1:
        start = input("Multiple pieces found. Please enter the location of the intended piece: ")
        a = board_index(start)
        good = valid_path(chessman, a, b)
        if not good:
            print("Error: the", chessman, "on ", start, "cannot move to", square)
            continue    #loop without switching (try again)
    else:
        print("Error: could not find a", chessman, "that can move to", square)
        continue    #loop without switching (try again)
    if chessman == 'P' and b < 8 or chessman == 'p' and b > 55:   #"and" is evaluated before "or"
        if promotion != 'p' and promotion != 'P':
            chessman = promotion
        else:
            chessman = promote_pawn()
    OldBoard = board
    board = MakeMove(board, chessman, a, b, castle)
    if white:
        king = find_pieces('K')
    else:
        king = find_pieces('k')
    check = check_check(king[0], white)
    if check:
        print("Invalid move: your King is in check!")
        board = OldBoard
        continue    #loop without switching (try again)
    #show corrected move (including check, checkmate, castling, pawn promotion)
    show_board(board)
    white = not white   #switch colors for next player
    ply += 1
    if capture or chessman == 'p' or chessman == 'P':
        ply = 0 #reset moves since capture or Pawn movement
    if ply > 50:
        print("No capture or Pawn move in 50 moves. Game is a DRAW")
        break
    if not white:
        fmn += 1    #increment full move number
