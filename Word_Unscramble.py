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

#Dictionary database (csv, json, or pickle):  #csv and json are portable, pickle is native
  #Word
  #Sorted word (letters arranged alphabetically)
  #Length
  #Popularity
  #Part of Speech

#Dictionary build:
  #Create *.csv file in Excel as a starting point
  #Import with pandas as working dictionary
  #Read nouns.md
  #For each noun:
    #Find in working dictionary
    #Assign part-of-speech (PoS) = noun
    #If noun[i] not in working dictionary
      #Add noun at end of working dictionary
  #For first n number of words without PoS:
    #Prompt user input for PoS
    #OR API call to dictionary?

#Solver:
  #Sort letters alphabetically
  #Count letters
  #Dictionary search:
    #If length = [length]:
      #Check nouns by popularity
      #Check Adjectives by popularity
      #Continue other parts of speech
