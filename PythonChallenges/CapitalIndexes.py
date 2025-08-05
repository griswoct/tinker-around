'''
#CAPITAL INDEXES
#PURPOSE: RETURN THE INDEXES OF CAPITAL LETTERS WITHIN A STRING
#PYTHON CHALLENGES NO. 1
#LICESNSE: TH UNLICENSE
#AUTHOR: CALEB GRISWOLD
'''
string = []
indexes = []
capitals = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}
string = input('Please enter a string that includes at least one capital letter: ')
i = 0
for char in string:
    if char in capitals:
        indexes.append(i)
    i += 1
print("The capital letters are located at the indexes: ", indexes)
