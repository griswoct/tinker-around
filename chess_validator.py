#CHESS VALIDATOR
#PURPOSE: ACCEPT BOARD CONFIGURATION AND CHESS MOVE, VERIFY IF IT IS A LEGAL MOVE
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-02-03
#
#accepts algebraic notation to move pieces
#validates of a piece can:
    #move in that way
    #no piece is in the way
    #not capturing your own piece or opponents King
    #dosen't put your King in check
#ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers and defenders are there on each piece
    #Identify checkmate

#IMPORT STATEMENTS
#import

#VARIABLES (GLOBAL)
capture = False
check = False
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
    i = 0    #Board position
    while i < 64:    #Display board
        print(board[i:i+8])
        i += 8

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
#Validate Chess Board Setup
if len.(board) != 64:
    print("Error: incomplete board configuration")    #Board array should have 64 elements
for i in pieces:
    i = 0
    for j in board:
        if i == j:
            k += 1
    if k > 8:
        print("Error: excessive number of ", i)
    elif i == 'p' and k > 8:
        print("Error: more than eight black Pawns")
    elif i == 'P' and k > 8:
        print("Error: more than eight white Pawns")
    elif i == 'k' and k != 1:
        print("Error: there should be exactly 1 black King")
    elif i == 'K' and k != 1:
        print("Error: there should be exactly 1 white King")
ShowBoard()
#Get Color Being Played
q = input ("Are you playing White (W) or Black (B)? ")
if q == 'B' or q == 'b':
    TeamWhite = False
    move = input("Black to move (enter algebraic notation): ")
else:
    move = input("White to move (enter algebraic notation): ")
#Parse Move
if move[-1] == '+' or move [-1] == '#':
    check = True
    destination = move[-3:-2]
elif move[-1] == '0' or move[-1] == 'o' or move[-1] == 'O': #Castle
    if len(move) < 5: #King side
        if TeamWhite:
            destination = 'g1'
        else:
            destination = 'g8'
    else: #Queen side
        if TeamWhite:
            destination = 'd1'
        else:
            destination = 'd8'
else:
    destination = move[-2:]
if move[1] == 'x':
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
    print("Error: could not parse move notation")
#Verify destination is on the board
#count number of that piece:
    #if first character is K or o, skip counting pieces
        #count = 1
    #if first character is a, b, c, d, e, f, or g:
        #count number of pawns of that color in that file
    #if first character is R, N, B, or Q:
        #count number of that piece and color are on the board
#if count < 1, throuw error (piece does not exist)
#if count = 1, save start location
#get last two characters of move, validate that end square is on the board(a1 to h8)
#if the third to last character of the move is 'x', verify an oponents piece is sitting on that square (but not their King)
#else verify the destination does not have a piece on it
#validate move path against piece type
#if not a Knight, validate clear path (no pieces in the way)
