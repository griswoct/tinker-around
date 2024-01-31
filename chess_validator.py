#get board arrangement or start with fresh starting position
#accepts algebraic notation to move pieces
#validates of a piece can:
    #move in that way
    #no piece is in the way
    #not capturing your own piece or opponents King
    #dosen't put your King in check
#Additional ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers and defenders are there on each piece
    #Identify checkmate

StartPos = input("Enter D for default starting position, or board configuration in FEN notation")
if fen = 'D':
    StartPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
i = 0    #Position in StartPos array
j = 0    #Board position
pieces = [K,k,Q,q,R,r,N,n,B,b,P,p]    #Valid pieces list
board = []
while j < 64:    #Populate board array from FEN string
    if fen[i] == '/':    #Next rank
        i += 1    #Ignore and go to to next character
        if i mod 8 != 0:    # '/' character encountered midway through a rank
            print("Unexpected / in the board configuration")
            break
    elif fen[i].isdigit() == True:
        if fen[i] > 8:    #More than 8 empty squares in a rank isn't posible in normal chess
            print("Unexpected extra empty squares in the board configuration")
            break
        else:
            k = 0
            while k < fen[i]:
                board[j] = ' '
                k += 1
                j += 1
    elif fen[i] in pieces:
        board[j] = fen[i]
        i += 1
        j += 1
#Validate board setup
    #if not 1 king each, throw an error (each color should have exactly 1 King)
    #if not 64 squares accounted for, throw an error (invalid configuration)
    #if more than 8 pawns on either side, throw error (too many pawns)
q = input ("Are you playing White (W) or Black (B)?")
if q == 'W' or q == 'w':
    TeamWhite = True
elif q == 'B' or q == 'b':
    TeamWhite == False
move = input("Enter desired move in algebraic notation")
#validate algebraic notation
    #parse here...
#get first character of move, and validate piece exists:
    #if first character is K or o, skip counting pieces
        #count = 1
    #if first character is a, b, c, d, e, f, or g:
        #count number of pawns of that color in that file
    #if first character is R, N, B, or Q:
        #count number of that piece and color are on the board
#if count < 1, throuw error (piece does not exist)
#if count = 1, save start location
#get last two characters of move, validate that end square is on the board(a1 to h8)
#if the third to last character of the move is 'x', verify an oponents piece is sitting on that square
#validate move path against piece type
#if not a Knight, validate clear path (no pieces in the way)
