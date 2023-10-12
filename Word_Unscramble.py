#scramble words to provide material
#Word Attributes:
  #Length
  #First letter
  #Type (noun, verb, adjective, adverb, etc.)
  #Common or uncommon
  #Repeated letters
  #Subject (common: animals, seasonal, wedding, baby, sports, religion, geography, literature, food)

#Dictionary database (csv file):
  #Rank (popularity)
  #Length
  #Sorted word (letters arranged alphabetically)
  #Word
  #Part of Speech

#Dictionary build:
  #Import word list from textfile in order of popularity
  #Assign rank sequentially through the list
  #Add length of word
  #Add sorted (alphabetical) form
  #Read nouns.md
  #For each noun:
    #Find in working dictionary
    #Assign part-of-speech (PoS) = noun
    #If noun[i] not in working dictionary
      #Add noun at end of working dictionary
      #Include rank, length, sorted
  #For first n number of words without PoS:
    #Prompt user input for PoS
    #OR API call to dictionary?
  #Save dictionary in csv form with pandas

import pandas
#if dictionary.csv exists:
  #read dixtionary.csv as df
df = pandas.read_csv("words.csv")
#n = int(input('Pick a number: '))
#print("Word ", n, " is: ", df.loc[n].at['Word'])  #for testing
i = 0
sort = []
while i < 9884:
	sort.append(''.join(sorted(str(df.loc[i].at['Word']))))
	i += 1
#print('Sorted word ', n, ' is ', sort[n])  #for testing
df['Sort'] = sort
#df['Sort'] = ''.join(sorted(str(df.Word)))
#print('Sorted word ', n, ' is ', df.loc[n].at['Sort'])  #for testing

#Solver:
  #Sort letters alphabetically
  #Count letters
  #Dictionary search:
    #If length = [length]:
      #Check nouns by popularity
      #Check Adjectives by popularity
      #Continue other parts of speech
  #If no word is found:
    #Prompt user for answer
    #Add to dictionary

letters = input("Please enter the scrambled letters:")
letters = ''.join(sorted(letters))
print("Sorted letters: ", letters)
match = False
j = 0
while j < 9884:
  if letters == sort[j]:
    print('Found match: ', df.loc[j].at['Word'])
    match = True
  j += 1
if match == False:
  print('No match found')
