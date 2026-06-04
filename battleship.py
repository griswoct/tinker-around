# Battleship
'''
1. Computer vs human
2. Computer vs Computer
'''
## Strategy
'''
### Missile Stratagy
* Dumb Random
* Random
* Grid
* Straif (diagonal lines)
* Padded (random, but with buffer space)
### Vessel Stratagy
* Random
* Padded (space between boats)
* Clump (no space between boats)
* Middle (clump or padded)
* Edges (clump or padded)
'''

#Import
import random

#Initialize variables
board_width = 10
board_area = board_width * board_width
sea1 = [None] * board_area
screen1 = [None] * board_area
sea2 = [None] * board_area
screen2 = [None] * board_area
ships = [5,4,3,3,2] #easier to place largest ships first
remaining_ships1 = ships
remaining_ships2 = ships
boat_strategy1 = 0
dart_strategy1 = 0
boat_strategy2 = 0
dart_strategy2 = 0
hard_block = 1  #set to 0 to block bow or stern from touching edge, 1 to allow
max_fails = 100
padded = 'Z'
edges = 'Z'

def boat_strategy(strategy):
    """Convert boat strategy number to padded and edges parameters."""
    padded = 'T' if strategy in [2, 6, 8] else 'F' if strategy in [3, 7, 9] else 'Z'
    edges = 'T' if strategy in [4, 6, 7] else 'F' if strategy in [5, 8, 9] else 'Z'
    return padded, edges

def place_boats(padded, edges):
    #Set up sea and allowed placement zones
    sea = [0] * board_area
    for i in range(board_area): #iterate through sea
        if i < board_width or i > board_area - board_width - 1 or i % board_width == 0 or i % board_width == board_width - 1:  #true for the edges of the sea
            if edges == 'F':
                sea[i] = 1  #set edges of sea to 1 (block)
            else:
                sea[i] = 0  #set edges of sea to 0 (allow)
        else:   #middle of sea
            if edges == 'T':
                sea[i] = 1  #set middle of sea to 1 (block)
            else:
                sea[i] = 0  #set middle of sea to 0 (allow)
    #Place ships in the sea
    n = 0
    while n < len(ships):   #Iterate through fleet
        boat = ships[n]
        direction = ["up", "down", "left", "right"]
        rejected = True
        fails = 0
        #Place a ship
        while rejected and fails < max_fails:  #continue while placement is rejected, up to max_fails attempts
            x = random.randint(0, board_area - 1)    #choose a random number x from board indexes
            if padded == 'F' and n > 0: #first ship placed, ramaining ships must touch
                while sea[x] != 9:  #initial location must be in the padding around other ships
                    x = random.randint(0, board_area - 1)
            elif sea[x] != 0:    #location not available
                fails = fails + 1
                continue
           #Check if too close to the edge of the board
            y = random.choice(direction)    #choose random number direction from 1 to 4
            if y == "up" and x - board_width * (boat - 1) < 0:
                fails = fails + 1
                continue    #off the top of the board, try again
            elif y == "down" and x + board_width * (boat - 1) > board_area - 1:
                fails = fails + 1
                continue    #off the bottom of the board, try again
            elif y == "left" and x % board_width < boat - 1:
                fails = fails + 1
                continue    #off the left side of the board, try again
            elif y == "right" and x % board_width > board_width - boat:
                fails = fails + 1
                continue    #off the left side of the board, try again
            #Get proposed locations to be occupied by ship
            z = 1
            proposed = [x]
            while z < boat: #loop over length of boat
                if y == "up":
                    x = x - board_width
                elif y == "down":
                    x = x + board_width
                elif y == "left":
                    x = x - 1
                elif y == "right":
                    x = x + 1
                proposed.append(x)
                z = z + 1
            conflict = False
            for i in proposed: #Check for conflicts in proposed locations
                if padded != 'T' and sea[i] == 9:   #if not padded, allow ships placed in buffer area around ships
                    conflict = False
                elif sea[i] > 0 + hard_block: #location occupied
                    fails = fails + 1
                    conflict = True
                    break  #location conflict, try again
            if not conflict:    #no conflicts, place boat
                print("Location for boat ", n + 1, " is ", proposed)   #for testing
                rejected = False
        if rejected:   #too many failures
            print("ERROR: Failed to place boat ", n - 1)
            return None    #failed to set up sea, return None
        for i in proposed:  #update sea
            sea[i] = boat
        #Add buffer around ship with value 9
        if padded == 'T' or padded == 'F':
            for i in proposed:
                if i - board_width >= 0:    #not top of board
                    if sea[i-board_width] in [0,1,9]:   #not occupied by a ship
                        sea[i-board_width] = 9  #buffer area
                if i + board_width < board_area:   #not bottom of board
                    if sea[i+board_width] in [0,1,9]:   #not occupied by a ship
                        sea[i+board_width] = 9  #buffer area
                if i % board_width != 0:    #not left edge
                    if sea[i-1] in [0,1,9]: #not occupied by a ship
                        sea[i-1] = 9    #buffer area
                if i % board_width != board_width - 1:  #not right edge
                    if sea[i+1] in [0,1,9]: #not occupied by a ship
                        sea[i+1] = 9    #buffer area
        n = n + 1
    j = 0
    while j < board_width:
        print(sea[j*board_width:(j+1)*board_width])
        j = j + 1
    return sea

def select_target():
    x = 0
    return x

def fire_dart(x: int, screen):
    return screen

def sink_ship():
    x = 0
    return x

def main():
    boat_strategy1 = int(input("Choose ship placement strategy:\n1. Random\n2. Spaced\n3. Clumped\n4. Touch Edge\n5. Avoid Edge\n6. Touch Edge Spaced\n7. Touch Edge Clumped\n8. Avoid Edge Spaced\n9. Avoid Edge Clumped\n"))
    while boat_strategy1 not in range(1, 10):
        boat_strategy1 = int(input("Please enter a number 1 to 9: "))
    padded, edges = boat_strategy(boat_strategy1)
    sea1 = place_boats(padded, edges)
    boat_strategy2 = random.randint(1, 9)    #randomly select computer boat strategy
    padded, edges = boat_strategy(boat_strategy2)
    sea2 = place_boats(padded, edges)
    #loop while remaining_ships is not None and open_targets is not None:
        #if sinking is True:
            #find target near recent hit
        #else:
            #choose dart stratagy
            #find target for stratagy in open_targets
        #fire dart at target
        #remove target from open_targets
        #if target is a hit:
            #mark hit on both boards
            #add hit to game log
            #if not sunk:
                #sinking = True
            #else:
                #sinking = False
                #announce ship was sunk
                #remove ship from remainin_ships
                #add sunk ship to game log
                #if hits is 17  #all ships sunk
                    #declare winner
                    #add to game history
                    #return winner
        #else:
            #mark as miss on both boards
            #add miss to game log
        #switch player
    #something went wrong...
    return
