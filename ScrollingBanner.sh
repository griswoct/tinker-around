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
Remainder=''	#For filling in partial letter at the end
i=0	#Loop counter
j=0	#Loop counter
k=0	#Loop counter
n=0	#Letter number index
p=0	#Partial letter index

read -p "What text do you want to display" $BannerText	#Get text to display

$i=0
while [ $i -lt $Size ]	#Populate banner line by line
do
	$j=0
	$n=0
	while [ $j -lt $WinWidth ]	#Populate display line i accross window
	do
		if [ $(($WinWidth - $j)) -ge $PadSize ]
		then
			#Add line $i of letter $BannerText[$n] to OutputLine$i
			$j=$(($j+$Size))
			$k=0
			while [ $k -lt $Spacing ]	#Add whitespace between letters
			do
				#Add ' ' to OutputLine$i
				(($k++))
				(($j++))
			done
			(($n++))
		else
			#Get $i line of letter $bannerText[$n] as $Remainder$i
			while [ $k -lt $Spacing ]	#Add whitespace between letters
			do
				#Add ' ' to $Remainder$i
				(($k++))
			done
			$p=0
			while [ $j -lt $WinWidth ]
			do
				#Add $Remainder[$p] to the end of $OutputLine$i
				(($p+))
				(($j++))
			done
		fi
	done
	#Echo OutputLine$i '/n'
	(($i++))
done

#Return to begining of the banner
$i=0
while [ $i -lt $Size ]	#Increment banner to the left line by line
do
	#Remove first character of OutputLine$i
	if [ $p -gt $PadSize ]
	then
		#load in the next letter
		#Create new $Remainder$i
	else
	#Add $Remainder[$p] to $OutputLine$i
	#Echo OutputLine$i '/n'
	(($i++))
done
(($p++))
