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
* Parallel (all vertical or all horizontal)
'''

#Import
import random

#initialize variables
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
max_fails = 100
padded = 'Z'
edges = 'Z'

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
            #Add x guesses when padded == 'F'
            if sea[x] != 0:    #location not available
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
                if sea[i] > 1:    #location occupied
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
        #Add disallowed buffer around ship when padded == 'T'
        n = n + 1
    print(sea)
    return sea

boat1 = int(input("Choose ship placement strategy:\n1. Random\n2. Spaced\n3. Clumped\n4. Touch Edge\n5. Avoid Edge\n6.Touch Edge Spaced\n7. Touch Edge Clumped\n8.Avoid Edge Spaced\n9. Avoid Edge Clumped\n"))
while boat1 not in [1,2,3,4,5,6,7,8,9]:
    boat1 = int(input("Please enter a number 1 to 9: "))
if boat1 in [2,6,8]:
    padded = 'T'
elif boat1 in [3,7,9]:
    padded = 'F'
if boat1 in [4,6,7]:
    edges = 'T'
elif boat1 in [5,8,9]:
    edges = 'F'
sea1 = place_boats(padded, edges)

#while remaining_ships1 is not None: #while remaining_ships is not None:    

#loop while remaining_ships is not None and open_targets is not None:
    #if sinking is True:
        #find target near recent hit
    #else:
        #choose missile stratagy
        #find target for stratagy in open_targets
    #fire missile at target
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
