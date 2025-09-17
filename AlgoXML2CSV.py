'''
#AlgoXML2CSV
#PURPOSE: PARSE XML OUTPPUT FROM ALGOAPP BACKUP INTO HUMAN READABLE CSV FILE
#AUTHOR: CALEB GRISWOLD
#LICENSE: THE UNLICENSE
#CREATED: 09/02/2025
'''

import pandas as pd
from io import StringIO

#Open xml file
with open('Literary  Vocabulary.xml', 'r') as file:
    contents = file.read()

#Remove html tags and insert commas
a = contents.find('<cards>') + 7
contents = contents[a:] #Find '<cards> and delete it and everything before it
contents = "Front,Back,\n" + contents  #Create header row
contents = contents.replace('<card>','')   #Delete card opening tags
contents = contents.replace('</card>','\n')   #Use card closig tag to mark new lines
contents = contents.replace("<text name='Front'>", '"F:') #Replace front text opening tags
contents = contents.replace("<text name='Back'>", '"B:') #Replace back text opening tags
contents = contents.replace('</text>','",')   #Use the text closing tags to mark delimination
contents = contents.replace("</cards></deck>", "")  #Delete "</cards></deck>" from end of string

#Create csv from contents string
contents_io = StringIO(contents)
df = pd.read_csv(contents_io)
print(df.head(2))   #for testing
breakpoint()    #for testing

#Sort Front and Back text to appropriate column
for index, row in df.iterrows():
    col_a = row['Front']
    col_b = row['Back']
    if col_a.startswith("B:"):   #Back text is the Front column
        print("Need to swap", col_b)    #for testing
        df.at[index, 'Front'] = col_b[2:] #Swap and remove "F:"
        df.at[index, 'Back'] = col_a[2:] #Swap and remove "B:"
    else:
        df.at[index, 'Front'] = col_a[2:] #Swap and remove "F:"
        df.at[index, 'Back'] = col_b[2:]    #Swap and remove "B:"

tsv_file = 'Literary Vocabulary.csv'    #Output file name
df.to_csv(tsv_file, index=False)