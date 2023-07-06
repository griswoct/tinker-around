#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-07-05
#
WinWidth=80	#Terminal window width
Size=5	#High and width of display letter in characters
FillChar='#'	#Possible options: 8, @, #, $, &, B, E, W, M, H, X
Spacing=2	#Number of spaces between the letters
PadSize=$(($Size+$Spacing))
BannerText='Example'	#Text to display
n=$(($WinWidth/$PadSize))	#Number of whole letters in each display line
i=0	#Loop counter
j=0	#Loop counter
k=0	#Loop counter

read -p "What text do you want to display" $BannerText	#Get text to display

$i=0
while [ $i -lt $Size ]
do
	$j=0
	while [ $j -lt $n ]	#Get the $i line of the first n letters
	do
		#Add line $i of letter $BannerText[$j] to OutputLine$i
		$k=0
		while [ $k -lt $Spacing ]	#Add whitespace between letters
		do
			#Add ' ' to OutputLine$i
			(($k++))
		done
		(($j++))
	done
	#Add partial letter n+1 to OutputLine$i
	#Echo OutputLine$i '/n'
	(($i++))
done
#Return to begining of the banner
$i=0
while [ $i -lt $Size ]
do
	#Remove first character of OutputLine$i
	#Add next character or letter n+1
	#Echo OutputLine$i '/n'
	(($i++))
done
