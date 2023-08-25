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

#Dictionary database (json?)
  #Word
  #Sorted word (letters arranged alphabetically)
  #Length
  #Popularity
  #Part of Speech

#Solver:
  #Sort letters alphabetically
  #Count letters
  #Dictionary search:
    #If length = [length]:
      #Check nouns by popularity
      #Check Adjectives by popularity
      #Continue other parts of speech