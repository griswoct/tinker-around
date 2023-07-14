#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-07-13
#
# Ideads: infinite scroll back to back, infinite scroll clear between
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
C0='.'	#Empty character, possible options: ' ', _, -, .
BannerText='Example Text'	#Text to display
Remainder=()	#Working banner end letter
Output=()	#Output strings to display banner

read -p $'What text do you want to display?\n' BannerText	#Get text to display
Length=${#BannerText}
tput sc	#Save cursor position
i=0
while [ $i -lt $Size ]	#Populate banner line by line
do
	j=0
	n=0
	while [ $j -lt $Width -a $n -lt $Length ]	#Populate display line i accross window
	do
		if [ $(($Width - $j)) -ge $PadSize ]
		then
			whats_my_line	#Get line $i of letter $BannerText[$n]
			Output[$i]+=${Remainder[$i]}
			j=$(($j+$Size))
			k=0
			while [ $k -lt $Spacing ]	#Add whitespace between letters
			do
				OutputLine[$i]+=$C0
				((k++))
				((j++))
			done
			((n++))
		else
			Remainder[$i]=''
			whats_my_line	#Get $i line of letter $bannerText[$n]
			k=0
			while [ $k -lt $Spacing ]	#Add whitespace to Remainder
			do
				Remainder[$i]+=$C0
				((k++))
			done
			p=0
			while [ $j -lt $Width ]	#Add characters from ramaining banner letter until full display width
			do
				Output[$i]+=${Remainder[$i]:$p:1}
				((p++))
				((j++))
			done
		fi
	done
	echo '$OutputLine[$i]\n'
	((i++))
done
sleep 1
while [ $n -lt $Length ]
do
	tput rc	#Return to saved cursor position (begining of the banner)
	i=0
	while [ $i -lt $Size ]	#Increment banner to the left line by line
	do
		if [ $p -gt $PadSize ]
		then
			if [ $i = 0 ]
			then
				(($n++))
				$p=0
			fi
			Remainder[$i]=''
			whats_my_line	#Get $i line of letter $BannerText[$n]
			while [ $k -lt $Spacing ]	#Add whitespace to Remainder
			do
				Remainder[$i]+=' '
				((k++))
			done
		fi
		Output[$i]=${Output[$i]:1}	#Remove first character of $Output[$i]
		Output[$i]+=${Remainder[$i]:$p:1}	#Add next character the end of $Output[$i]
		echo $Output[$i]
		((i++))
	done
	((p++))
	sleep 0.2
done

whats_my_line () {
	local list=()
	local h=5
	local w=5
	case $BannerText[$n] in	#Find correct letter
		' ')
			$h=5
			$w=5
			$list=(false false false false false false false false false false false false false false false false false false false false false false false false false)	#Display a 5x5 space
		A | a)
			$h=5
			$w=5
			$list=(false true true true false true false false false true true true true true true true false false false true true false false false true)
		B | b)
			$h=5
			$w=5
			$list=(true true true true false true false false false true true true true true false true false false false true true true true true false)
		C | c)
			$h=5
			$w=5
			$list=(false true true true true true false false false false true false false false false true false false false false false true true true true)
		D | d)
			$h=5
			$w=5
			$list=(true true true true false true false false true true true false false false true true false false true true true true true true false)
		E | e)
			$h=5
			$w=5
			$list=(true true true true true true false false false false true true true false false true false false false false true true true true true)
		F | f)
			$h=5
			$w=5
			$list=(true true true true true true false false false false true true true false false true false false false false true false false false false)
		G | g)
			$h=5
			$w=5
			$list=(false true true true false true false false false false true false true true true true false false false true false true true true false)
		H | h)
			$h=5
			$w=5
			$list=(true false false false true true false false false true true true true true true true false false false true true false false false true)
		I | i)
			$h=5
			$w=5
			$list=(false true true true false false false true false false false false true false false false false true false false false true true true false)
		J | j)
			$h=5
			$w=5
			$list=(false false true true true false false false true false false false false true false true false false true false false true true false false)
		K | k)
			$h=5
			$w=5
			$list=(true false false false true true false false true false true true true false false true false false true false true false false false true)
		L | l)
			$h=5
			$w=5
			$list=(true false false false false true false false false false true false false false false true false false false false true true true true false)
		M | m)
			$h=5
			$w=5
			$list=(true false false false true true true false true true true false true false true true false true false true true false false false true)
		N | n)
			$h=0
			$w=0
			$list=(true false false false true true true false false true true false true false true true false false true true true false false false true)
		O | o)
			$h=0
			$w=0
			$list=(false true true true false true false false false true true false false false true true false false false true false true true true false)
		P | p)
			$h=0
			$w=0
			$list=(true true true true false true false false false true true true true true false true false false false false true false false false false)
		Q | q)
			$h=0
			$w=0
			$list=(false true true true false true false false false true true false false false true true false false true false false true true false true)
		R | r)
			$h=0
			$w=0
			$list=(true true true true false true false false false true true true true true false true false false true false true false false false true)
		S | s)
			$h=0
			$w=0
			$list=(false true true true true true false false false false false true true true false false false false false true true true true true false)
		T | t)
			$h=0
			$w=0
			$list=(true true true true true false false true false false false false true false false false false true false false false false true false false)
		U | u)
			$h=0
			$w=0
			$list=(true false false false true true false false false true true false false false true true false false false true false true true true false)
		V | v)
			$h=0
			$w=0
			$list=(true false false false true true false false false true true false false false true false true false true false false false true false false)
		W | w)
			$h=0
			$w=0
			$list=(true false false false true true false false false true true false true false true true true false true true true false false false true)
		Z | x)
			$h=0
			$w=0
			$list=(true false false false true false true false true false false false true false false false true false true false true false false false true)
		Y | y)
			$h=0
			$w=0
			$list=(true false false false true true false false false true false true true true false false false true false false false false true false false)
		Z | z)
			$h=0
			$w=0
			$list=(true true true true true false false false true false false false true false false false true false false false true true true true true)
		*)	#Character not recognized, display block
			$h=5
			$w=5
			$list=(true true true true true true true true true true true true true true true true true true true true true true true true true )	#Display a 5x5 block
	esac
	if [ $Size -ne $h ]
	then
		echo 'SIZE MISMATCH ERROR'
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
