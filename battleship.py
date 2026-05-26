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
ships = [5,4,3,3,2] #easier to place largest ships first
remaining_ships1 = ships
remaining_ships2 = ships
boat_strategy1 = 0
dart_strategy1 = 0
boat_strategy2 = 0
dart_strategy2 = 0
padded = 'Z'
edges = 'Z'

def place_boats(padded, edges):
    #Set up sea and allowed placement zones
    sea = [0] * 100
    for i in range(100): #iterate through sea
        if i < 10 or i > 89 or i % 10 == 0 or i % 10 == 9:  #true for the edges of the sea
            if edges == 'F':
                sea[i] = 1  #set edges of sea to 1 (block)
            else:
                sea[i] = 0  #set edges of sea to 0 (allow)
        else:   #middle of sea
            if edges == 'T':
                sea[i] = 1  #set middle of sea to 1 (block)
            else:
                sea[i] = 0  #set middle of sea to 0 (allow)
    
    #AI GENERATED VERSION
    '''
    if edges == 'T':
        sea = [1 if (i // 10 in (0, 9) or i % 10 in (0, 9)) else 0 for i in range(100)]
    elif edges == 'F':
        sea = [1 if not (i // 10 in (0, 9) or i % 10 in (0, 9)) else 0 for i in range(100)]
    else:
        sea = [0] * 100
    '''
    #END AI GENERATED VERSION
    
    #Place ships in the sea
    n = 0
    while n < len(ships):   #Iterate through fleet
        boat = ships[n]
        direction = ["up", "down", "left", "right"]
        rejected = True
        fails = 0
        #Place a ship
        while rejected and fails < 100:  #continue while placement is rejected, up to 100 attempts
            x = random.randint(0,99)    #choose a random number x from 0-99
            if sea[x] is not 0:    #location not available
                fails = fails + 1
                continue
            y = random.choice(direction)    #choose random number direction from 1 to 4
            z = 0
            #Check if too close to the edge of the board
            if y == "up" and x - 10 * (boat - 1) < 0:
                fails = fails + 1
                continue    #off the top of the board, try again
            elif y == "down" and x + 10 * (boat - 1) > 99:
                fails = fails + 1
                continue    #off the bottom of the board, try again
            elif y == "left" and x % 10 < boat - 1:
                fails = fails + 1
                continue    #off the left side of the board, try again
            elif y == "right" and x % 10 + boat > 10:
                fails = fails + 1
                continue    #off the left side of the board, try again
            proposed = []
            #loop over length of boat
                #choose y
                #if up, x = x - 10
                #if down, x = x + 10
                #if left, x = x - 1
                #if right, x = x + 1
                #if sea[x] > 1:    #location occupied
                    #fails = fails + 1
                    #break   #exit loop, ship collision
                #check padding
                #if not enought space
                    #fails = fails + 1
                    #break  #insufficient spacing
                #else:
                    #add x to proposed
                    #if len(proposed) = boat:
                        #rejected = False
                        #fails = 0
        #if rejected:   #too many failures
            #print error message
            #return None    #failed to set up sea, return None
        #update sea with sea[proposed] = boat
        n = n + 1
    print(sea)
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
