#scramble words to provide material
#need common english words, likely nouns
#Word Attributes:
  #Length
  #First letter
  #Type (noun, verb, adjective, adverb, etc.)
  #Common or uncommon
  #Repeated letters
  #Subject (common: animals, seasonal, wedding, baby, sports, religion, geography, literature, food)
#Sub dictionaries?
#Object or relationsl database?
#Order by popularity, try nouns first

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