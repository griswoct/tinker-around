# Battleship
'''
1. Computer vs human
2. Computer vs Computer
'''
## Strategy
'''
### Missile Stratagy
1. Dumb Random
2. Random
3. Grid
4. Straif (diagonal lines)
5. Padded (random, but with buffer space)
### Vessel Stratagy
* Random
* Padded (space between boats)
* Clump (no space between boats)
* Middle (clump or padded)
* Edges (clump or padded)
'''

#Import
import random

#Initialize CONSTANTS
HARDBLOCK = 1  #set to 0 to block bow or stern from touching edge, 1 to allow
WIDTH = 10    #length of board edge
AREA = WIDTH * WIDTH  #number of spaces on the board
MAXFAILS = 100 #maximum failed iterations for setup or targeting before exiting
SHIPS= [5,4,3,3,2] #easier to place largest SHIPSfirst

#Initialize variables
player = 1  #which player's turn is it?
screen1 = [None] * AREA   #blank screen for player
screen2 = [None] * AREA   #blank screen for computer
sea1 = [None] * AREA  #blank sea for player
sea2 = [None] * AREA  #blank sea for computer
remaining_ships1 = SHIPS   #start with all ships remaining
remaining_ships2 = SHIPS   #start with all ships remaining
boat_strategy1 = 0  #player defaults to invalid boat strategy
boat_strategy2 = 1  #computer defaults to random boat strategy
dart_strategy1 = 0  #player defaults to invalid dart strategy
dart_strategy2 = 1  #computer defaults to random dart strategy
target_list2 = []    #default blank target list
padded1 = 'Z'    #not true or false (irgnored)
padded2 = 'Z'    #not true or false (irgnored)
edges1 = 'Z'   #not true or false (irgnored)
edges2 = 'Z'   #not true or false (irgnored)
sinking1 = False #player actively sinking ship
sinking2 = False #computer actively sinking ship
hit1 = None    #location of recent hit for player
hit2 = None    #location of recent hit for computer
target = None  #target space
impact = False   #dart strike defaults to miss

def get_boat_strategy():
    '''Prompt player to select a boat placement stragety'''
    strategy = input("Choose ship placement strategy:\n1. Random\n2. Spaced\n3. Clumped\n4. Touch Edge\n5. Avoid Edge\n6. Touch Edge Spaced\n7. Touch Edge Clumped\n8. Avoid Edge Spaced\n9. Avoid Edge Clumped\n")
    if not strategy or not strategy.isdigit():
        strategy = 0
    else:
        strategy = int(strategy)
    while strategy not in range(1, 10):
        strategy = input("Please enter a number 1 to 9: ")
        if strategy and bs1.isdigit():
            strategy = int(strategy)
        else:
            strategy = 0
    return strategy

def boat_strategy(strategy):
    '''Get padding and edge strategy from boat strategy selection'''
    padded = 'T' if strategy in [2, 6, 8] else 'F' if strategy in [3, 7, 9] else 'Z'
    edges = 'T' if strategy in [4, 6, 7] else 'F' if strategy in [5, 8, 9] else 'Z'
    return padded, edges

def place_boats(padded, edges):
    '''Place boats on the sea according to the selected strategy'''
    #Set up sea and allowed placement zones
    sea = [0] * AREA
    for i in range(AREA): #iterate through sea
        if i < WIDTH or i > AREA - WIDTH - 1 or i % WIDTH == 0 or i % WIDTH == WIDTH - 1:  #true for the edges of the sea
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
    while n < len(SHIPS):   #Iterate through fleet
        boat = SHIPS[n]
        direction = ["up", "down", "left", "right"]
        rejected = True
        fails = 0
        #Place a ship
        while rejected and fails < MAXFAILS:  #continue while placement is rejected, up to MAXFAILS attempts
            x = random.randint(0, AREA - 1)    #choose a random number x from board indexes
            if padded == 'F' and n > 0: #first ship placed, ramaining ships must touch
                while sea[x] != 9:  #initial location must be in the padding around other ships
                    x = random.randint(0, AREA - 1)
            elif sea[x] != 0:    #location not available
                fails = fails + 1
                continue
           #Check if too close to the edge of the board
            y = random.choice(direction)    #choose random number direction from 1 to 4
            if y == "up" and x - WIDTH * (boat - 1) < 0:
                fails = fails + 1
                continue    #off the top of the board, try again
            elif y == "down" and x + WIDTH * (boat - 1) > AREA - 1:
                fails = fails + 1
                continue    #off the bottom of the board, try again
            elif y == "left" and x % WIDTH < boat - 1:
                fails = fails + 1
                continue    #off the left side of the board, try again
            elif y == "right" and x % WIDTH > WIDTH - boat:
                fails = fails + 1
                continue    #off the left side of the board, try again
            #Get proposed locations to be occupied by ship
            z = 1
            proposed = [x]
            while z < boat: #loop over length of boat
                if y == "up":
                    x = x - WIDTH
                elif y == "down":
                    x = x + WIDTH
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
                elif sea[i] > 0 + HARDBLOCK: #location occupied
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
                if i - WIDTH >= 0:    #not top of board
                    if sea[i-WIDTH] in [0,1,9]:   #not occupied by a ship
                        sea[i-WIDTH] = 9  #buffer area
                if i + WIDTH < AREA:   #not bottom of board
                    if sea[i+WIDTH] in [0,1,9]:   #not occupied by a ship
                        sea[i+WIDTH] = 9  #buffer area
                if i % WIDTH != 0:    #not left edge
                    if sea[i-1] in [0,1,9]: #not occupied by a ship
                        sea[i-1] = 9    #buffer area
                if i % WIDTH != WIDTH - 1:  #not right edge
                    if sea[i+1] in [0,1,9]: #not occupied by a ship
                        sea[i+1] = 9    #buffer area
        n = n + 1
    j = 0
    while j < WIDTH:
        print(sea[j*WIDTH:(j+1)*WIDTH])
        j = j + 1
    return sea

def get_dart_strategy():
    '''Prompt player to select a boat placement stragety'''
    ds = input("Choose dart targeting strategy:\n1. Dumb Random\n2. Random\n3. Grid\n4. Straif (diagonal lines)\n5. Padded (spaced from previous targets)\n")
    if not ds or not ds.isdigit():
        boat_strategy = 0
    else:
        boat_strategy = int(ds)
    while boat_strategy not in range(1, 10):
        ds = input("Please enter a number 1 to 9: ")
        if ds and ds.isdigit():
            boat_strategy = int(ds)
        else:
            dart_strategy = 0
    return dart_strategy

def dart_strategy(strategy):
    '''Get dart strategy from dart strategy selection'''
    target_list = []    #default blank target list
    gap = int(sum(SHIPS) / len(SHIPS))   #average boat length rounded down
    start = random.randint(0, gap - 1)  #randomize grid alignment
    i = start
    if strategy == 3: #form a grid
        while i < AREA:
            j = i % WIDTH #j tracks the board column
            while j < WIDTH:
                target_list.append(i)
                i = i + gap
                j = j + gap
            row = int(i / WIDTH)
            i = (row + gap) * WIDTH + start  #move down gap rows and back to start column
    elif strategy == 4: #form diagonal lines
        while i < AREA:
            j = i % WIDTH #j tracks the board column
            while j < WIDTH:
                target_list.append(i)
                i = i + gap
                j = j + gap
            row = int(i / WIDTH)
            offset = start + row    #diagonal starting point
            while offset > gap - 1: #keep starting poing within gap of the left edge
                offset = offset - gap
            i = row * WIDTH + offset   #move to the beginning of the next row
    else:   #defaults to random, use entire board as target list (includes options 1 and 2)
        target_list = list(range(0, AREA))    #array from 0 to board area - 1
    return target_list

def sink_ship(hit: int):
    '''Continue attack on hit ship'''
    x = 0
    return x

def get_target(screen):
    valid_selection = False
    selection = input("Please select a target: ")    #get target from player
    while not valid_selection:
        if selection[0].upper() in "ABCDEFGHIJ" and selection[1] in "1234567890":    #validate target format
            target = (ord(selection[0].upper()) - 65) * WIDTH + int(selection[1:]) - 1    #convert target to index
            if target < AREA:    #validate target is on the board
                valid_selection = True
            else:
                print("Target is off the board, please try again.")
                selection = input("Please select a target: ")
        else:
            print("Invalid target, please try again.")
            selection = input("Please select a target: ")
        if screen[target] != ' ':   #target already used
            print("This location has already been targeted, with result: ", screen[target])
            valid_selection = False
            selection = input("Please select a target: ")
    return target

def fire_dart(x: int, screen, sea):
    '''Fire dart and report result'''
    impact = False   #default to miss
    if screen[x] is not None:    #space already targeted
        return None    #invalid target
    if sea[x] > 1:
        impact = True
    return impact

def main():
    '''Main function to run battleship game'''
    boat_strategy1 = get_boat_strategy()
    padded1, edges1 = boat_strategy(boat_strategy1)
    sea1 = place_boats(padded1, edges1)
    boat_strategy2 = random.randint(1, 9)    #randomly select computer boat strategy
    padded2, edges2 = boat_strategy(boat_strategy2)
    sea2 = place_boats(padded2, edges2)
    dart_strategy2 = random.randint(1, 5)    #randomly select computer dart strategy
    target_list2 = dart_strategy(dart_strategy2)
    while remaining_ships1 and remaining_ships2:    #while both players have ships remaining
        if player == 1:
            screen = screen1
            sea = sea2
            target = get_target(screen)
        elif player == 2:
            screen = screen2
            sea = sea1
            if sinking2 and dart_strategy != 1: #actively sinking a ship
                target = sink_ship(hit2)    #find target near recent hit
            else:   #default to choosing from target list
                target = random.choice(target_list2)    #choose random target from target list
        impact = fire_dart(target, screen, sea)    #fire dart at target space and return result
            #remove target from open_targets
                #if target list is empty
                    #populate with remaining spaces
                    #if target list is still empty
                        #error message
                        #return
            #if target is a hit:
                #mark hit on both boards
                #add hit to game log
                #if sunk:
                    #sinking = False
                    #announce ship was sunk
                    #remove ship from remainin_ships
                    #add sunk ship to game log
                    #if hits is 17  #all ships sunk
                        #declare winner
                        #add to game history
                        #return winner
                #else:
                    #sinking = True
            #else:
                #mark as miss on both boards
                #add miss to game log
            #switch player
    #something went wrong...
    return

if __name__ == "__main__":
    main()
