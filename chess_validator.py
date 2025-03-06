'''
#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#   EXPANDED PURPOSE:
#       VERIFY OR GENERATE LEGAL MOVES
#       LIST ATTACKERS AND DEFENDERS
#       FACILITATE GAME BETWEEN TWO PLAYERS
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
'''
#Need to add:
    #Identify checkmate
        #Identify all possible moves
        #Try each one and check for check
        #If list of options is [], then checkmate or stalemate
        #Declare winner and end game
    #[ ] Read PGN
    #[X] Generate PGN
    #Game Over:
        #[ ] Checkmate (winner)
        #[x] Resignation (winner)
        #[ ] Draw (no winner)
            #[ ] Stalemate (no leagal moves)
            #[x] 50 moves no Pawn moves or captures
            #[ ] Position repeated 3 times (including castling and en passant)
                #Need to record the FEN after each half move
                #If the same FEN occurs 3 times (not counting ply, fmn, active color), declare "DRAW by REPITITION"
            #[ ] insufficient material:
                #King
                #King + Bishop
                #King + Knight
                #King + 2 Knights vs King
                #summary: you need a major piece/Pawn or two minor pieces (except K vs K and 2N)
                #If there is a Pawn, Rook, or Queen on the board, there is sufficient material
                #Elif there is a Bishop and one other minor piece of the same color, there is sufficient material
                #Else:
                    #insuffucient material
#More Ideas:
    #Heat map of which squares on the boad are controlled by which player
        #Number of squares controlled (squares with more defenders than opponent attackers)
        #Weighted board control (sum of defenders minus attackers for all squares)
    #How many attackers and defenders are there on each piece
        #Number of hanging pieces (no defenders)
        #Number of vulnerable pieces (equal or fewer defenders than attackers)
        #Weighted vulnerability (loss or gain of material if all attacks played out)
    #[X] Identifies all valid move for selected piece
    #Read PGN
        #[X] Add to PGN as game continues
        #Generate FEN from PGN
        #Recognize openings

#VARIABLES (GLOBAL)
capture = False #Indicates a piece is being captured
check = False   #King is in Check
good = False    #Boolean to control loops
white = None    #Playing as white? (Boolean)
a = 64    #Board index starting location
b = 64    #Board index ending location
ep = '' #En passant target square
promotion = ''
fmn = 1  #Full move number, defaults to start of game
ply = 0 #Number of half moves since last capture or Pawn movement
board = []    #Chess board configuration
castle = [True,True,True,True]  #Tracks castle availibility (KQkq)
fileA = [0,8,16,24,32,40,48,56] #Board indexes for A-file (edge of board)
fileB = [1,9,17,25,33,41,49,57] #Board indexes for B-file
fileC = [2,10,18,26,34,42,50,58] #Board indexes for C-file
fileD = [3,11,19,27,35,43,51,59] #Board indexes for D-file
fileE = [4,12,20,28,36,44,52,60] #Board indexes for E-file
fileF = [5,13,21,29,37,45,53,61] #Board indexes for F-file
fileG = [6,14,22,30,38,46,54,62]    #Board indexes for G-file
fileH = [7,15,23,31,39,47,55,63]    #Board indexes for H-file (edge of board)
history = []    #List of positions in Forsyth-Edwards Notation
pgn = []    #Portable Game Notation array
ranks = ['a','b','c','d','e','f','g','h']
xblack = ['q','r','b','n','p']    #Capturable black pieces list (no King)
xwhite = ['Q','R','N','B','P']    #Capturable white pieces list (no King)
pieces = ['K', *xwhite, 'k', *xblack]    #Valid chess pieces list

#FUNCTIONS
def get_board():
    '''Get Chess Board Setup'''
    global white
    global ep
    global fmn
    global ply
    global castle
    build = []
    #Add option to select FEN or PGN
    #if pgn:
        #call function to read pgn and build fen
    #if fen:
        #break read fen into seperate function
    fen = input("Enter D for default starting position, or board configuration in FEN notation: ")
    if fen in ['D','d']:
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"    #Chess starting position
        #fen = "rnb1k2N/pp1p2pp/1b3n2/4p3/1pB1P3/P7/2PPNqPP/R1BQK2R w KQq - 0 11"    #for testing
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
    i += 1    #Skip space before active color
    if i < len(fen):
        if fen[i] == 'w':   #White is active
            white = True
        elif fen[i] == 'b': #Black is active
            white = False
        else:
            white = True    #Defaults to white
            q = input ("Is White (W) or Black (B) active? ")
            if q == 'B' or q == 'b':    #Black selected
                white = False
        if fen[i+1] == ' ': #Skip space befre castling ability
            i += 2  #Move to castling ability
    while fen[i] != ' ' and i < len(fen):   #Read castling from fen
        if fen[i] == 'K':
            castle[0] = True
        elif fen[i] == 'Q':
            castle[1] = True
        elif fen[i] == 'k':
            castle[2] = True
        elif fen[i] == 'q':
            castle[3] = True
        elif fen[i] == '-':
            castle = [False,False,False,False]
        else:
            print("Error reading castle ability")
        i += 1
    i += 1  #Skip space before en passant target
    if i < len(fen):
        if fen[i] == '-':   #Determine En Passant Target
            ep = ''
            i += 2  #Move to halfmove clock
        else:
            ep = board_index(fen[i:i+1])
            i += 3  #Move to halfmove clock
    if i < len(fen):
        if fen[i] == '-':   #No halfmoves since last capture or Pawn movement
            ply = 0
            i += 2  #Move to full move numner
        elif fen[i+1] == ' ':   #1 digit halfmove clock
            ply = int(fen[i])
            i += 2  #Move to full move number
        else:  #2 digit halfmove clock
            ply = int(fen[i:i+1])
            i += 3  #Move to full move number
    if i < len(fen):
        fmn = int(fen[i:])   #Remaining fen string indicates full move number
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
    if move == "resign":    #resign game (exit)
        return "resign"
    if move[-1] == '+' or move [-1] == '#':    #remove '+' or '#'
        move.pop()    #Removes last character
    if move[0] in ['0','o','O']:    #castling
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
    if 'x' in move: #remove 'x' or 'X' (will determine capturing later)
        move = move.replace('x','')
    elif 'X' in move:
        move = move.replace('X','')
    if move[0] in ['K','k','0','O','o']:    #king
        if white:
            piece = 'K'
        else: piece = 'k'
    elif move[0] in {'Q','q'}:
        if white:
            piece = 'Q'
        else:
            piece = 'q'
    elif move[0] in {'R','r'}:
        if white:
            piece = 'R'
        else:
            piece = 'r'
    elif move[0] in {'N','n'}:
        if white:
            piece = 'N'
        else:
            piece = 'n'
    elif move[0] in {'B','b'} and move[1].isdigit() is False: #Bishop not b pawn
        if white:
            piece = 'B'
        else:
            piece = 'b'
    elif move[0] in ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','P','p']: #pawn
        if '=' in move:
            promo = move.pop()
            move.remove('=')
        else:
            promo = ''
        col = move[-2]
        if white:
            piece = 'P'
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
    sq = move[-2:]  #Determine square
    #Validate square
    try:
        row = int(move[-1])
        sq = col + str(row)
    except ValueError:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
    if move[-2] not in ranks:
        print("Error -- couldn't parse move: [", move, "] -- couldn't find square")
    #col = move[-2]
    destination = board_index(sq)   #convert square to number
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
    if not isinstance(i, int):
        try:
            i = int(i)
        except ValueError:
            return 'z0'
    if i % 8 == 0:  #MODULUS/INGETER ISSUE
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
    global chessman
    global board
    square = board_algebraic(b)
    if white:
        if b == ep and chessman == 'P':
            return True
        if p in xblack:
            return True
        if p == 'k':
            print("You cannot capture the King")
        elif p in xwhite or p == 'K':
            print("Your ", p, " is already on ", square)
        else:
            print("Something went wrong. ", p, " is on ", square)
    else:   #black
        if b == ep and chessman == 'p':
            return True
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
    if cm in {'P','p'}:
        reach = pawn_moves(destination, False, color)
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
        reach = bishop_moves(destination, False, color)
    elif cm in {'N','n'}:
        reach = knight_moves(destination, False, color)
    elif cm in {'R','r'}:
        reach = rook_moves(destination, False, color)
    elif cm in {'Q','q'}:
        reach = queen_moves(destination, False, color)
    elif cm in {'K','k'}:
        reach = king_moves(destination, False)
    i = 0
    while i < len(reach):   #itterate through piece's range
        if board[reach[i]] == cm:
            if cm in {'P','p'}:    #pawn
                if capture or reach[i] in col:    #only pawns in destination file (unless capturing)
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

def pawn_moves(home: int, forwards: bool, color: bool):
    '''Returns the squares a Pawn can move to from starting square home'''
    path = [home]
    if home < 8 or home > 55:
        return []   #not a valid Pawn rank, return null array
    if capture:
        if forwards == color:  #True if white forwards or black backwards
            if home not in fileH:   #can move right
                x = home - 7    #forward right
                if board[x] in xblack:
                    path.append(x)
            if home not in fileA:   #can move left
                x = home - 9   #forward left
                if board[x] in xblack:
                    path.append(x)
        elif forwards ^ color: #XOR: white and backwards or black and forwards
            if home not in fileA:  #can move left
                x = home + 7   #backward left
                if board[x] in xwhite:
                    path.append(x)
            if home not in fileH:   #can move right
                x = home + 9   #backward right
                if board[x] in xwhite:
                    path.append(x)
    else:   #straight
        x = home
        while True:
            if forwards == color:  #True if white forwards or black backwards
                x -= 8 #forwards
                if not color:  #black backwards
                    if board[x] == 'p': #found a matching color Pawn
                        path.append(x)
                        break  #Pawns can't jump eachother
            elif forwards ^ color: #XOR: white and backwards or black and forwards
                x += 8 #backwards
                if color:  #white backwards
                    if board[x] == 'P':    #found a matching color Pawn
                        path.append(x)
                        break  #Pawns can't jump eachother
            if board[x] == ' ':
                path.append(x)
            else:  #blocked, stop moving
                break
            if color:  #white
                if x < 40 or x > 47: #white can only take one more step if on rank 3
                    break
            else:  #black
                if x < 16 or x > 23: #black can only take one more step if on rank 6
                    break
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

def knight_moves(home: int, forwards: bool, color: bool):
    '''Returns the squares a Knight can move to from starting square home'''
    path = [home]
    if home < 48:   #ranks 3-8
        if home not in fileA:
            x = home + 15  #down 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack: #forwards & white or backtrack & black
                path.append(x)
            elif forwards ^ color and board[x] in xwhite: #forwards & black or backtrack & white
                path.append(x)
        if home not in fileH:
            x = home + 17  #down 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
    if home > 15:   #ranks 1-6
        if home not in fileA:
            x = home - 17  #up 2 ranks, left 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
        if home not in fileH:
            x = home - 15  #up 2 ranks, right 1 file
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
    if home not in fileA and home not in fileB:
        if home > 7:
            x = home - 10   #left 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 6   #left 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
    if home not in fileG and home not in fileH:
        if home > 7:
            x = home - 6   #right 2 files, up 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
        if home < 56:
            x = home + 10   #right 2 files, down 1 rank
            if board[x] == ' ':
                path.append(x)
            elif forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
    return path

def bishop_moves(home: int, forwards: bool, color: bool):
    '''Returns the squares a Bishop can move to from starting square home'''
    path = [home]
    x = home
    while x not in fileA and x > 7: #move up and left until reaching file A or rank 8
        x -= 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x > 7: #move up and right until reaching file H or rank 8
        x -= 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileA and x < 56: #move down and left until reaching file A or rank 1
        x += 7
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH and x < 56: #move down and right until reaching file H or rank 1
        x += 9
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    return path

def rook_moves(home: int, forwards: bool, color: bool):
    '''Returns the squares a Rook can move to'''
    path = [home]
    x = home
    while x not in fileA: #move left until reaching file A
        x -= 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x not in fileH: #move right until reaching file H
        x += 1
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x > 7: #move up until reaching rank 8
        x -= 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    x = home
    while x < 56: #move down until reaching rank 1
        x += 8
        if board[x] == ' ':
            path.append(x)
        else:
            if forwards == color and board[x] in xblack:
                path.append(x)
            elif forwards ^ color and board[x] in xwhite:
                path.append(x)
            break
    return path

def queen_moves(home: int, fwd: bool, colour):
    '''Returns the squares a Queen can move to'''
    pathR = rook_moves(home, fwd, colour)
    pathR.remove(home)
    pathB = bishop_moves(home, fwd, colour)
    path = pathR + pathB
    return path

def king_moves(home: int, forwards: bool):
    '''Returns the squares a King can move to'''
    squares = [home-9,home-8,home-7,home-1,home,home+1,home+7,home+8,home+9]
    path = []
    if home > 55:   #bottom rank
        del squares[6:]   #remove backward movement
    elif home < 8:  #top rank
        del squares[:3]   #remove forward movement
    if home in fileA:   #left edge
        for x in squares:  #itterate through remaining options
            if x in fileH:  #off the board
                squares.remove(x)  #remove leftward motion
    elif home in fileH: #right edge
        for x in squares:  #itterate through remaining options
            if x in fileA:  #off the board
                squares.remove(x)  #remove rightward motion
    for x in squares:
        if board[x] == ' ': #blank space available
            path.append(x)
        elif white:
            if not forwards and board[x] == 'K':    #backtracking, found white King
                path.append(x)
            elif board[x] in xblack:  #White King captures black piece
                path.append(x)
        else:   #black
            if not forwards and board[x] == 'k':    #backtracking, found black King
                path.append(x)
            elif board[x] in xwhite:    #Black King captures white piece
                path.append(x)
    #Castling
    if white:
        if board[60] != 'K':
            return path
        nogo = check_check(60, white)
        if nogo:    #White King in check
            return path
        if castle[0] and board[63] == 'R':  #kingside
            x = 61  #kingside of King
            while x < 63:   #path to Rook
                nogo = check_check(x, white)
                if board[x] != ' ' or nogo:
                    break
                else:
                    x += 1
            if x == 63: #cleared entire path between King and Rook
                if forwards:
                    path.append(62)
                else:
                    path.append(60)
        if castle[1] and board[56] == 'R':  #queenside
            x = 59  #queenside of King
            while x > 56:   #path to Rook
                nogo = check_check(x, white)
                if board[x] != ' ' or nogo and x > 57: #and evaluated before or
                    break
                else:
                    x -= 1
            if x == 56: #checked entire path between King and Rook
                if forwards:
                    path.append(58)
                else:
                    path.append(60)
    else:  #black
        if board[4] != 'k':
            return path
        nogo = check_check(4, white)
        if nogo:
            return path
        if castle[2] and board[7] == 'r':  #kingside
            x = 5  #kingside of King
            while x < 7:   #path to Rook
                nogo = check_check(x, white)
                if board[x] != ' ' or nogo:
                    break
                else:
                    x += 1
            if x == 7: #cleared entire path between King and Rook
                if forwards:
                    path.append(6)
                else:
                    path.append(4)
        if castle[3] and board[0] == 'r':  #queenside
            x = 3  #queenside of King
            while x > 0:   #path to Rook
                nogo = check_check(x, white)
                if board[x] != ' ' or nogo and x > 1: #and evaluated before or
                    break
                else:
                    x -= 1
            if x == 0: #checked entire path between King and Rook
                if forwards:
                    path.append(2)
                else:
                    path.append(4)
    path = list(set(path))
    return path

def check_check(throne: int, color: bool):
    '''Checks if a square can be attacked by an opponents piece'''
    threats = attackers(throne, color)
    for i in threats:
        if i != []:
            return True
    return False

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

def make_move(original: str, type, start: int, end: int, castling: bool):
    '''Updates board array and adds specified move to PGN'''
    updated = original
    global capture
    global castle
    global check
    global ep
    global pgn
    global white
    #Pawn Handling
    if type in {'P','p'}:
        if white and end < 8 or not white and end > 55: #Promote pawn
            if promotion not in ['P','p','']:
                type = promotion
            else:
                type = promote_pawn()
        elif end == ep: #en passant capture
            if white:
                updated[end+8] = ' '    #remove pawn from previous rank
            else:
                updated[end-8] = ' '    #remove pawn from next rank
            ep = '' #clear en passant target
        elif abs(end - start) == 16:    #pawn moves 2 squares
            if white:
                ep = start - 8  #en passant target
            else:
                ep = start + 8    #en passant target
    else:
        ep = '' #clear en passant target
    #Update Board
    updated[start] = ' '
    updated[end] = type
    #Castle Handling
    if castling:
        if end == 62:   #white kingside
            updated[61] = 'R'
            updated[63] = ' '
            castle[0] = False
            castle[1] = False
            move = "O-O"
        elif end == 58: #white queenside
            updated[59] = 'R'
            updated[56] = ' '
            castle[0] = False
            castle[1] = False
            move = "O-O-O"
        elif end == 6:  #black kingside
            updated[5] = 'r'
            updated[7] = ' '
            castle[2] = False
            castle[3] = False
            move = "O-O"
        elif end == 2:  #black queenside
            updated[3] = 'r'
            updated[0] = ' '
            castle[2] = False
            castle[3] = False
            move = "O-O-O"
    else:   #generate move in portable game notation
        end = board_algebraic(end)
        if type in ('P','p'):
            if capture:
                startA = board_algebraic(start)
                move = startA[0]+'x'+end
            else:
                move = end
        elif capture:
            move = type+'x'+end
        else:
            move = type+end
    if check:  #need to get check
        move = move+'+'
    if type == 'R': #update castling ability
        if start == 63: #kingside
            castle[0] = False
        elif start == 56:   #queenside
            castle[1] = False
    elif type == 'r':
        if start == 7:  #kingside
            castle[2] = False
        elif start == 0:   #queenside
            castle[3] = False
    elif type == 'K':
        castle[0] = False
        castle[1] = False
    elif type == 'k':
        castle[2] = False
        castle[3] = False
    pgn.append(move)
    return updated

def get_moves(target: int):
    '''Get available moves for piece on target square'''
    chessman = board[a]
    if chessman == 'P':
        moves = pawn_moves(a, True, True)
    elif chessman == 'p':
        moves = pawn_moves(a, True, False)
    elif chessman in ('B','b'):
        moves = bishop_moves(a, True, True)
    elif chessman in ('N','n'):
        moves = knight_moves(a, True, True)
    elif chessman in ('R','r'):
        moves = rook_moves(a, True, True)
    elif chessman in ('Q','q'):
        moves = queen_moves(a, True, True)
    elif chessman in ('K','k'):
        moves = king_moves(a, True, True)
    else:
        print("Error: could not identify piece (blank)?")
        return []
    #Check for check for each option?
    return moves

def validate_move():
    '''Checks if a move is valid'''
    global a
    global b
    global board
    global capture
    global check
    global chessman
    global promotion
    capture = False #reset capture
    check = False   #reset check
    a = 64
    b = 64
    q = get_move()
    if q == "resign": #resign game (exit)
        print("Resigning game...")
        if white:
            pgn.append("0-1")   #black wins by resignation
        else:
            pgn.append("1-0")   #white wins by resignation
        return True
    else:
        chessman = q[0]
        b = q[1]
        promotion = q[2]
        castling = q[3]
        file = q[4]
    square = board_algebraic(b)  #get algebratic notation for user feedback (error messages)
    #Validate Selected Square
    if b >= len(board):    #off the board
        print("Error: ", square, " not found on board")
        return False    #Invalid move due to invalid square
    #Validate Capture
    if b == ep or board[b] != ' ': #Move attempts to capture
        good = valid_capture(board[b])
        if good:
            capture = True
        else:
            print("Error: connot capture", board[b], "on square", square)
            return False    #Invalid move due to invalid capture
    options = back_track(b, chessman, white, file)
    if len(options) == 1:
        if castling and white and not castle[0] and not castle[1]:  #invalid castle white
            print("Invalid Castle Option/n",castle)
            return False    #Invalid move due to invalid castle
        elif castling and white and not castle[2] and not castle[3]:  #invalid castle black
            print("Invalid Castle Option/n",castle)
            return False    #Invalid move due to invalid castle
        a = options[0]
    elif len(options) > 1:
        start = input("Multiple pieces found. Please enter the location of the intended piece: ")
        a = board_index(start)
        good = valid_path(chessman, a, b)
        if not good:
            print("Error: the", chessman, "on ", start, "cannot move to", square)
            return False    #Invalid move due to invalid path for piece
    else:
        print("Error: could not find a", chessman, "that can move to", square)
        return False    #Invalid move due to invalid path for piece
    if chessman == 'P' and b < 8 or chessman == 'p' and b > 55:   #"and" is evaluated before "or"
        if promotion != 'p' and promotion != 'P':
            chessman = promotion
        else:
            chessman = promote_pawn()
    OldBoard = board
    board = make_move(board, chessman, a, b, castling)
    if white:
        king = find_pieces('K')
    else:
        king = find_pieces('k')
    check = check_check(king[0], white)
    if check:
        print("Invalid move: your King is in check!")
        board = OldBoard
        pgn.pop()   #remove last move from pgn array
        return False
    return True

def read_pgn(pgnS):
    '''Read PGN string and return board arrangement'''
    global board
    tempBoard = ['r','n','b','q','k','b','n','r','p','p','p','p','p','p','p','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','P','P','P','P','P','P','P','P','R','N','B','Q','K','B','N','R']
    #Loop through pgn string
    i = 0
    while i < len(pgnS):
        if pgnS[i] is '.':  #Use '.' to find next full move
            j = i - 1 #first digit left of '.'
            if j == 0:    #No space before move 1. (so don't look for one)
                fmn = int(pgnS[0:1])    #Set Full Move Number to initial "1"
            else:
                while pgnS[j] is not ' ':   #look for space before FMN
                    j = j - 1
                fmn = int(pgnS[j+1:i-1])    #Set Full Move Number
            j = i + 2 #Skip space after '.'
            while pgnS[j] is not ' ':   #Use ' ' to find next ply
                j = j + 1
            wMove = pgnS[i+2:j-1]   #White move
            i = j + 1   #Skip space between ply
            while pgnS[i] is not ' ':   #Use ' ' to find next ply
                i = i + 1
            bMove = pgnS[j+1:i-1]
            #NEED TO GET MOVE PARAMETERS, validate_board()?
            pgn.append(wMove)   #Update PGN array with White move
            pgn.append(bMove)   #Update PGN array with Black move
            tempBoard = make_move(board, type, start: int, end: int, castling: bool)    #Update board
        i = i + 1
    board = tempBoard
    #Update FEN
    return

#Main Menu Selection
print(" \
    1. VALIDATE MOVE\n \
    2. TWO PLAYER GAME\n \
    3. AVAILABLE MOVES FOR PIECE\n \
    4. AVAILABLE MOVES FOR COLOR\n \
    5. PIECE ATTACKERS AND DEFENDERS\n \
    6. BOARD CONTROL HEATMAP\n \
    7. IS THE GAME OVER?\n \
    ")  #Remove 7 once automatic check is implemented
selection = 0
while selection not in {1,2,3,4,5,6}:
    selection = int(input("Please select an option: ")) #loop for valid input
good = False
while not good:
    board = get_board()
    good = valid_board(board)
show_board(board)
#Add check if board arrangement is game over?
if selection == 1:  #VALIDATE MOVE
    good = validate_move()
    if good:
        print("VALID MOVE")
    else:
        print("NOT A VALID MOVE")
elif selection == 2:    #TWO PLAYER GAME
    while ply < 100:   #counts ply (half moves) since last capture or Pawn movement
        good = validate_move()
        if not good:
            #if check:
                #is the game over?
            print("Not valid, please try again")
            continue    #loop without switching (try again)
        if white:
            print(fmn,'. ',pgn[-1])
            if pgn[-1] == "0-1":    #resigned
                print("BLACK WINS by RESIGNATION!")
                break
        else:
            print(fmn,'. ',pgn[-2],' ',pgn[-1])
            if pgn[-1] == "1-0":    #resigned
                print("WHITE WINS by RESIGNATION!")
                break
        #fmn. , chessman (column if Pawn), x if capture, end square (algebraic), =promotion, +/# if check/checkmate
        show_board(board)
        white = not white   #switch colors for next player
        ply += 1
        if capture or chessman == 'p' or chessman == 'P':
            ply = 0 #reset moves since capture or Pawn movement
        if ply > 100:
            print("DRAW by FIFTY-MOVE RULE")
            break
        if white:
            fmn += 1    #increment full move number
elif selection == 3:    #AVAILABLE MOVES FOR PIECE
    square = input("Enter piece location (square): ")
    a = board_index(square)
    options = get_moves(a)
    moves = []
    for i in options:
        if i == a:
            continue    #do not include not moving
        else:
            moves.append(board[a] + board_algebraic(i)) #selected chessman + destination square
    print("Available moves for are", moves)
elif selection == 4:    #AVAILABLE MOVES FOR COLOR
    options = []
    if white:
        print("Showing all possible moves for WHITE")
        for i in board:
            if board[i] in xwhite:
                result = get_moves(i)
                if result is not []:
                    options.append(result)
    else:
        print("Showing all possible moves for BLACK")
        for i in board:
            if board[i] in xblack:
                result = get_moves(i)
                if result is not []:
                    options.append(result)
elif selection == 5:    #PIECE ATTACKERS AND DEFENDERS
    square = input("Enter piece location (square): ")
    a = board_index(square)
    chessman = board[a]
    #determin which color
    threats = attackers(a, white)
    print("Attackers:", threats)
    threats = attackers(a, not white)
    print("Defenders for this", chessman, ":", threats)
elif selection == 6:    #BOARD CONTROL HEATMAP
    bcontrol = []
    wcontrol = []
    for i in board:
        wcontrol.append(attackers(i, white))
        bcontrol.append(attackers(i, not white))
else:
    print("Error: did not recognize selection")
