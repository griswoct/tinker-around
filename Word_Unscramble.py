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

#For each noun in nouns.md:
  #Find in working dictionary
  #Assign part-of-speech (PoS) = noun
#Part of Speech:
    #Prompt user input for PoS
    #OR API call to dictionary?
  #Save dictionary in csv form with pandas

import pandas
import os.path
if os.path.exists('dictionary.csv') == True:
	df = pandas.read_csv('dictionary.csv')
else:
	df = pandas.read_csv('words.csv')
i = 0
sort = []
while i < len(df):
	sort.append(''.join(sorted(str(df.loc[i].at['Word']))))
	i += 1
df['Sort'] = sort
#df['Sort'] = ''.join(sorted(str(df.Word)))
#print('Sorted word ', n, ' is ', df.loc[n].at['Sort'])  #for testing
if os.path.exists('dictionary.csv') == False:
	df.to_csv('dictionary.csv', sep=',', index=False)

letters = input('Please enter the scrambled letters: ')
letters = ''.join(sorted(letters))
#print("Sorted letters: ", letters)	#for testing
match = False
j = 0
while j < len(df):
	if letters == sort[j]:
		print('Found match: ', df.loc[j].at['Word'])
		match = True
	j += 1
if match == False:
	print('No match found')
	prompt = input('Add to dictionary? (Y/N)')
	if prompt == 'Y' or 'yes' or 'YES' or 'Yes':
		print('What word do the letters', letters, 'make?')
		word = input('>:')
		df.loc[len(df)] = [len(df)+1, word, len(letters), letters]  #Add line to dataframe
		df.to_csv('dictionary.csv', sep=',', index=False)
print('Exiting Word_Unscramble.py')
