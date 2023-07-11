#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-07-10
#
Width=80	#Banner display width
Length=0	#Number of letters in banner message
Size=5	#High and width of banner letter in characters
i=0	#Banner display line
j=0	#Loop counter
k=0	#Loop counter
n=0	#Working banner letter index
p=0	#Partial letter character index
Spacing=2	#Number of spaces between banner letters
PadSize=$(($Size+$Spacing))
C1='#'	#Fill character, possible options: #, @, $, &, 8, B, E, W, M, H, X
C0=' '	#Empty character, possible options: ' ', _, -, .
BannerText='Jed G'	#Text to display
Remainder=()	#Working banner end letter
Output=()	#Output strings to display banner

read -p "What text do you want to display" $BannerText	#Get text to display
$Length=${#BannerText}
tput sc	#Save cursor position
$i=0
while [ $i -lt $Size ]	#Populate banner line by line
do
	$j=0
	$n=0
	while [ $j -lt $Width -a $n -lt $Length ]	#Populate display line i accross window
	do
		if [ $(($Width - $j)) -ge $PadSize ]
		then
			$temp=''
			whats_my_line	#Get line $i of letter $BannerText[$n]
			$Remainder[$i]=$?
			$Output[$i]="$Output[$i]$Remainder[$i]"
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
			$Remainder[$i]=''
			whats_my_line	#Get $i line of letter $bannerText[$n]
			$Remainder[$i]=$?
			$k=0
			while [ $k -lt $Spacing ]	#Add whitespace to Remainder
			do
				$Remainder[$i]+=' '
				(($k++))
			done
			$p=0
			while [ $j -lt $Width ]	#Add characters from ramaining banner letter until full display width
			do
				$Output[$i]+=${Remainder[$i]:$p:1}
				(($p+))
				(($j++))
			done
		fi
	done
	echo $OutputLine[$i]+='\n'
	(($i++))
done
sleep 1
while [$n -lt $Length ]
do
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
			$Remainder[$i]=''
			whats_my_line	#Get $i line of letter $BannerText[$n]
			$Remainder[$i]=$?
			while [ $k -lt $Spacing ]	#Add whitespace to Remainder
			do
				$Remainder[$i]+=' '
				(($k++))
			done
		fi
		$Output[$i]="${Output[$i]:1}"	#Remove first character of $Output[$i]
		$Output[$i]+=${Remainder[$i]:$p:1}	#Add next character the end of $Output[$i]
		echo $Output[$i]+='\n'
		(($i++))
	done
	(($p++))
	sleep 0.2
done

whats_my_line () {
	local list=()
	local h=5
	local w=5
	case $BannerText[$n] in	#Find correct letter
		*)	#Character not recognized, display blank space
			$h=5
			$w=5
			$list=(false false false false false false false false false false false false false false false false false false false false false false false false false)	#Display a 5x5 space
	esac
	if [ $Size -ne $h ]
	then
		echo "ERROR: SIZE MISMATCH"
		exit
	fi
	local a=$(($w * $i))
	local b=0
	local str=''
	while [ $b -lt $Size ]	#Get line $i of banner letter
	do
		if [ $list[$(($a + $b)) ]
		then
			$str+=$C1
		else
			$str+=$C0
		fi
		(($b++))
	done
	return $str
}
