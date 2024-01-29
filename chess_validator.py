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

start_pos = input("Enter D for default starting position, or FEN notation")
if start_pos = 'D':
    start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
