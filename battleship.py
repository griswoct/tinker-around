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
sea1 = [None] * 100
screen1 = [None] * 100
sea2 = [None] * 100
screen2 = [None] * 100
ships = ['P','S','M','B','C']
remaining_ships1 = ships
remaining_ships2 = ships
boat_strategy1 = 0
dart_strategy1 = 0
boat_strategy2 = 0
dart_strategy2 = 0
padded = 'Z'
edges = 'Z'

def place_boats(padded, edges):
    sea = [0] * 100
    #if edges is 'T':   #block middle of board
        #set middle of sea to 1
    #elif edges is 'F': #block edges of board
        #set edges of board to 1
    x = random.randint(0,99)    #NEED TO CHOOSE STRATAGY HERE
    n = 0
    while n < len(ships):
        boat = ships[n]
        while sea[x] is not 0:  #find an available part of the sea
            x = random.randint(0,99)    #choose a random number x from 0-99
        y = random.randint(1,4)    #choose random number direction from 1 to 4
        z = 0
        #choose size based on ship type
        #check if the boat will go off the end of the board
            #if up, x - 10 * (size - 1) >= 0
            #if down, x + 10 * (size - 1) <= 99
            #if left, x - (size - 1) >= 0
            #if right, x + (size - 1) <= 99
        #while less than the length of the boat:
            #choose y
                #if up, z = z - 10
                #if down, z = z + 10
                #if left, z = z - 1
                #if right, z = z + 1
            #record locations
            #if occupied spot (sea[z] is not 0 or 1):
                #reset locations, boat length progress, direction, and starting point x
                #try placing again
        #record value of ramaining_ships1[-1] to sea1[locations]
        #remove last element of remaining ship
    return sea

boat1 = input("Choose ship placement strategy:\n1. Random\n2. Spaced\n3. Clumped\n4. Touch Edge\n5. Avoid Edge\n6.Touch Edge Spaced\n7. Touch Edge Clumped\n8.Avoid Edge Spaced\n9. Avoid Edge Clumped\n")
while boat1 not in [1,2,3,4,5,6,7,8,9]:
    boat1 = input("Please enter a number 1 to 9: ")
if boat1 in [2,6,8]:
    padded = 'T'
elif boat1 in [3,7,9]:
    padded = 'F'
if boat1 in [4,6,7]:
    edges = 'T'
elif boat1 in [5,8,9]:
    edges = 'F'
sea1 = place_boats(padded, edges)

while remaining_ships1 is not None: #while remaining_ships is not None:    

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
