#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-07-07
#
WinWidth=80	#Banner display width
Size=5	#High and width of banner letter in characters
i=0	#Loop counter
j=0	#Loop counter
k=0	#Loop counter
n=0	#Letter number index
p=0	#Partial letter index
Spacing=2	#Number of spaces between the letters
PadSize=$(($Size+$Spacing))
FillChar='#'	#Possible options: #, @, $, &, 8, B, E, W, M, H, X
BannerText='Example text'	#Text to display
temp=''	#Temporary string variable
Remainder=()	#For filling in partial letter at the end
Output=()	#Output strings to display banner

read -p "What text do you want to display" $BannerText	#Get text to display
tput sc	#Save cursor position
$i=0
while [ $i -lt $Size ]	#Populate banner line by line
do
	$j=0
	$n=0
	while [ $j -lt $WinWidth ]	#Populate display line i accross window
	do
		if [ $(($WinWidth - $j)) -ge $PadSize ]
		then
			$temp=whats_my_line	#Get line $i of letter $BannerText[$n] as $temp
			$Output[$i]="$Output[$i]$temp"
			$j=$(($j+$Size))
			$k=0
			while [ $k -lt $Spacing ]	#Add whitespace between letters
			do
				$OutputLine[$i]+=' '
				(($k++))
				(($j++))
			done
			(($n++))
		else
			$Remainder[$i]=whats_my_line	#Get $i line of letter $bannerText[$n] as $Remainder[$i]
			while [ $k -lt $Spacing ]	#Add whitespace to Remainder
			do
				$Remainder[$i]+=' '
				(($k++))
			done
			$p=0
			while [ $j -lt $WinWidth ]	#Add characters from ramaining banner letter until full display width
			do
				$Output[$i]+=$Remainder[$p]
				(($p+))
				(($j++))
			done
		fi
	done
	echo $OutputLine[$i]+='\n'
	(($i++))
done
sleep 1
tput rc	#Return to saved cursor position (begining of the banner)
$i=0
while [ $i -lt $Size ]	#Increment banner to the left line by line
do
	if [ $p -gt $PadSize ]
	then
		if [ $i = 0 ]
		then
			(($n++))
			$p=0
		fi
		$Remainder[$i]=whats_my_line	#Get $i line of letter $BannerText[$n] as $Remainder[$i]
		while [ $k -lt $Spacing ]	#Add whitespace to Remainder
		do
			$Remainder[$i]+=' '
			(($k++))
		done
	fi
	$Output[$i]="${Output[$i]:1}"	#Remove first character of $Output[$i]
	$Output[$i]+=$Remainder[$p]	#Add next character the end of $Output[$i]
	echo $Output[$i]+='\n'
	(($i++))
done
(($p++))
sleep 0.2

whats_my_line () {
	echo "Inside the whats_my_line function"
	#Find correct letter
	#Check if size is correct
	#Get line $i of banner letter
	#return values
}
