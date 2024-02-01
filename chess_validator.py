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

#IMPORT STATEMENTS

#VARIABLES (GLOBAL)
TeamWhite = True    #Playing as white? (Boolean)
i = 0    #Integer index
j = 0    #Integer index
k = 0    #Integer index
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Board configuration in FEN
move = 'e4'    #Chess move in algebraic notation
q = 'Y'    #User input string
board = []    #Chess board configuration
pieces = ['K','k','Q','q','R','r','N','n','B','b','P','p']    #Valid chess pieces list

#FUNCTIONS
#Display Chess Board on Terminal Screen
def ShowBoard():
    while i < 64:    #Display board
        print(board[i:i+8])
        i += 8

fen = input("Enter D for default starting position, or board configuration in FEN notation")
if fen == 'D' or fen == 'd':
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Chess starting position
i = 0    #Position in fen array
j = 0    #Board position
while j < 64:    #Populate board array from FEN string
    if fen[i] == '/':    #Next rank
        if j % 8 != 0:    # '/' character encountered midway through a rank
            print("Error: unexpected / in the board configuration: ")
            break
        else:
            i += 1    #Ignore and go to to next character
    elif fen[i].isdigit() == True:
        if int(fen[i]) > 8:    #More than 8 empty squares in a rank isn't posible in normal chess
            print("Error: extra empty squares in the board configuration")
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
#Validate board setup
    #if not 1 king each, throw an error (each color should have exactly 1 King)
    #if not 64 squares accounted for, throw an error (invalid configuration)
    #if more than 8 pawns on either side, throw error (too many pawns)
i = 0   #Board position
ShowBoard()
q = input ("Are you playing White (W) or Black (B)? ")
if q == 'W' or q == 'w':
    TeamWhite = True
    move = input("White to move (in algebraic notation): ")
elif q == 'B' or q == 'b':
    TeamWhite = False
    move = input("Black to move (in algebraic notation): ")
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
