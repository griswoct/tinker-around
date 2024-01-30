#get board arrangement or start with fresh starting position
#accepts algebraic notation to move pieces
#validates of a piece can:
    #move in that way
    #no piece is in the way
    #not capturing your own piece or opponents King
    #dosen't put your King in check
#Additional ideas:
    #Heat map of which squares on the boad are controlled by which player
    #How many attackers a d defenders are there on each piece

StartPos = input("Enter D for default starting position, or board configuration in FEN notation")
if StartPos = 'D':
    StartPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
#define 64 character array board
#loop through StartPos and decipher FEN notation into board array
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
