#!/usr/bin/env python3
'''
#MIDDLE LETTER
#PURPOSE: GET A STRING FROM THE USER AND RETURN THE MIDDLE LETTER
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#DATE CREATED: 2025-08-20
'''
string = []
string = input("Please enter some text: ")
length = len(string)
while len(string) < 1:
  string = input("No really, enter some text: ")
  length = len(string)
if length % 2 == 1:
  middle = int(length / 2)
  print("The middle letter is ", string[middle])
else:
  middle = int(length / 2)
  print("The middle letters are ", string[middle-1:middle+1])
