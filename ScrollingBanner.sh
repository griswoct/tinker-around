#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-07-01
#
WinWidth=80	#Terminal window width
CharSize=5	#High and width of display letter (square)
Spacing=2
PadSize=$(($CharSize+$Spacing))
BannerText='Example'	#Text to display
n=$(($WinWidth/$PadSize))	#Number of whole letters in each display line

read -p "What text do you want to display" $BannerText	#Get text to display

#For $i < CharSize
	#For $j < $n	#Get the $i line of the first n letters
		#Add line $i of letter $BannerText[$j] to OutputLine$i
		#For $k < $Spacing
			#Add ' ' to OutputLine$i
			#k++
		#$j++
	#Add partial letter n+1 to OutputLine$i
	#Echo OutputLine$i '/n'
	#$i++
#Return to begining of the banner
#For $i < CharSize
	#Remove first character of OutputLine$i
	#Add next character or letter n+1
	#Echo OutputLine$i '/n'
	#$i++