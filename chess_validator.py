#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-02-06
#
#accepts algebraic notation to move pieces
#validates of a piece can:
    #move in that way
    #no piece is in the way
    #dosen't put your King in check
#ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers and defenders are there on each piece
    #Identify checkmate
    #Identifies all valid move for selected piece

#IMPORT STATEMENTS
#import

#VARIABLES (GLOBAL)
capture = False
check = False
white = True    #Playing as white? (Boolean)
a = 52    #Board index starting location
b = 36    #Board index ending location
i = 0    #Integer index
j = 0    #Integer index
k = 0    #Integer index
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Board configuration in FEN
move = 'e4'    #Chess move in algebraic notation
square = 'e4'    #Selected square on the board (algebraic notation)
board = []    #Chess board configuration
pieces = ['K','k','Q','q','R','r','N','n','B','b','P','p']    #Valid chess pieces list
xblack = ['q','r','b','n','p']    #Capturable black pieces list (no King)
xwhite = ['Q','R','N','B','P']    #Capturable white pieces list (no King)

#FUNCTIONS
#Display Chess Board on Terminal Screen
def ShowBoard():
    i = 0    #Board position
    while i < 64:    #Display board
        print(board[i:i+8])
        i += 8

#Convert Algebraic Notated Square to Board Index Number
def BoardIndex(sq):
    if len(sq) != 2:    #Board location should be 2 characters in algebraic notation
        return 64    #Invalid index indicating error
    else:
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
            i = 64
        if i < 0 or i > 63:
            return 64    #Invalid index indicating error
        else:
            return i

#Verify the Piece "p" Can Be Captured
def ValidCapture(p):
    if white:
        if p in xblack:
            if not capture:
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

#MAIN BODY
#Get Chess Board Setup
fen = input("Enter D for default starting position, or board configuration in FEN notation")
if fen == 'D' or fen == 'd':
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"    #Chess starting position
i = 0    #Position in fen array
j = 0    #Board position
while j < 64:    #Populate board array from FEN string
    if fen[i] == '/':    #Next rank
        if j % 8 != 0:    # '/' character encountered midway through a rank
            print("Error: unexpected / in the board configuration")
            print(fen)
            break
        else:
            i += 1    #Ignore and go to to next character
    elif fen[i].isdigit() == True:
        if int(fen[i]) > 8:    #More than 8 empty squares in a rank isn't posible in normal chess
            print("Error: extra empty squares in the board configuration")
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
#Validate Chess Board Setup
if len(board) != 64:
    print("Error: incomplete board configuration")    #Board array should have 64 elements
    ShowBoard()
for i in pieces:
    i = 0
    for j in board:
        if i == j:
            k += 1
    if k > 8:
        print("Error: excessive number of ", i)
    elif i == 'p' and k > 8:
        print("Error: more than 8 black Pawns")
    elif i == 'P' and k > 8:
        print("Error: more than 8 white Pawns")
    elif i == 'k' and k != 1:
        print("Error: there should be exactly 1 black King. Found ", k)
    elif i == 'K' and k != 1:
        print("Error: there should be exactly 1 white King. Found ", k)
ShowBoard()
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
    piece = 'K'
elif move[0] == 'Q' or move[0] == 'q':
    piece = 'Q'
elif move[0] == 'R' or move[0] == 'r':
    piece = 'R'
elif move[0] == 'N' or move[0] == 'n':
    piece = 'N'
elif move[0] == 'B' and move[1].isdigit() == False:
    piece = 'B'
elif move[0] == 'a' or move[0] == 'b' or move[0] == 'c' or move[0] == 'd' or move[0] == 'e' or move[0] == 'f' or move[0] == 'g' or move[0] == 'h' or move[0] == 'P' or move[0] == 'p':
    piece ='P'
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

#count number of that piece:
    #if piece == 'K', skip counting
        #count = 1
    #if piece == 'P':
        #count number of pawns of that color in that file
    #if piece is R, N, B, or Q:
        #count number of that piece and color are on the board
#if count < 1, throuw error (piece does not exist)
#if count = 1, save start location
#validate move path against piece type
#if not a Knight, validate clear path (no pieces in the way)
