'''
# Battleship
1. Computer vs human
2. Computer vs Computer
## Strategy
### Missile Stratagy
* Dumb Random
* Random
* Grid
* Straif (diagonal lines)
* Padded (random, but with buffer space)
### Vessel Stratagy
* Random
* Padded (space between boats)
* Clump
* Middle (clump or padded)
* Edges (clump or padded)
* Parallel (all vertical or all horizontal)
'''
#initialize variables
#while remaining_ships is not None:
    #choose vessel stratagy
    #place vessel
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
