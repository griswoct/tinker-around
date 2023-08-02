#!/bin/bash

#SCROLLING BANNER
#
#PURPOSE: DISPLAY SCROLLING BANNER IN THE TERMINAL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-08-02
#
# Ideads: infinite scroll back to back, infinite scroll clear between
#
Width=80	#Banner display width
Length=0	#Number of letters in banner message
Size=5	#High and width of banner letter in characters
i=0	#Banner display line
j=0	#Loop counter
n=0	#Working banner letter index
p=0	#Partial letter character index
Spacing=2	#Number of spaces between banner letters
PadSize=$(($Size+$Spacing))
C1='#'	#Fill character, possible options: #, @, $, &, 8, B, E, W, M, H, X
C0='.'	#Empty character, possible options: _, -, .
loop=true	#true to loop banner message
BannerText=$(date '+%A %B %d %Y')	#Text to display (Today's date default)
Remainder=()	#Working banner end letter
Output=()	#Output strings to display banner

whats_my_line () {
	local list=()	#Boolean array defining banner display letter matrix
	local h=0	#Height of display letter
	local w=0	#Width of display letter
	local a=0	#Offset
	local b=0	#Local loop counter
	case ${BannerText:$n:1} in	#Find correct letter
		' ')
			h=5
			w=5
			list=(false false false false false false false false false false false false false false false false false false false false false false false false false)	#Display a 5x5 space
			;;
		A | a)
			h=5
			w=5
			list=(false true true true false true false false false true true true true true true true false false false true true false false false true)
			;;
		B | b)
			h=5
			w=5
			list=(true true true true false true false false false true true true true true false true false false false true true true true true false)
			;;
		C | c)
			h=5
			w=5
			list=(false true true true true true false false false false true false false false false true false false false false false true true true true)
			;;
		D | d)
			h=5
			w=5
			list=(true true true true false true false false true true true false false false true true false false true true true true true true false)
			;;
		E | e)
			h=5
			w=5
			list=(true true true true true true false false false false true true true false false true false false false false true true true true true)
			;;
		F | f)
			h=5
			w=5
			list=(true true true true true true false false false false true true true false false true false false false false true false false false false)
			;;
		G | g)
			h=5
			w=5
			list=(false true true true false true false false false false true false true true true true false false false true false true true true false)
			;;
		H | h)
			h=5
			w=5
			list=(true false false false true true false false false true true true true true true true false false false true true false false false true)
			;;
		I | i)
			h=5
			w=5
			list=(false true true true false false false true false false false false true false false false false true false false false true true true false)
			;;
		J | j)
			h=5
			w=5
			list=(false false true true true false false false true false false false false true false true false false true false false true true false false)
			;;
		K | k)
			h=5
			w=5
			list=(true false false false true true false false true false true true true false false true false false true false true false false false true)
			;;
		L | l)
			h=5
			w=5
			list=(true false false false false true false false false false true false false false false true false false false false true true true true false)
			;;
		M | m)
			h=5
			w=5
			list=(true false false false true true true false true true true false true false true true false true false true true false false false true)
			;;
		N | n)
			h=5
			w=5
			list=(true false false false true true true false false true true false true false true true false false true true true false false false true)
			;;
		O | o)
			h=5
			w=5
			list=(false true true true false true false false false true true false false false true true false false false true false true true true false)
			;;
		P | p)
			h=5
			w=5
			list=(true true true true false true false false false true true true true true false true false false false false true false false false false)
			;;
		Q | q)
			h=5
			w=5
			list=(false true true true false true false false false true true false false false true true false false true false false true true false true)
			;;
		R | r)
			h=5
			w=5
			list=(true true true true false true false false false true true true true true false true false false true false true false false false true)
			;;
		S | s)
			h=5
			w=5
			list=(false true true true true true false false false false false true true true false false false false false true true true true true false)
			;;
		T | t)
			h=5
			w=5
			list=(true true true true true false false true false false false false true false false false false true false false false false true false false)
			;;
		U | u)
			h=5
			w=5
			list=(true false false false true true false false false true true false false false true true false false false true false true true true false)
			;;
		V | v)
			h=5
			w=5
			list=(true false false false true true false false false true true false false false true false true false true false false false true false false)
			;;
		W | w)
			h=5
			w=5
			list=(true false false false true true false false false true true false true false true true true false true true true false false false true)
			;;
		Z | x)
			h=5
			w=5
			list=(true false false false true false true false true false false false true false false false true false true false true false false false true)
			;;
		Y | y)
			h=5
			w=5
			list=(true false false false true true false false false true false true true true false false false true false false false false true false false)
			;;
		Z | z)
			h=5
			w=5
			list=(true true true true true false false false true false false false true false false false true false false false true true true true true)
			;;
		*)	#Character not recognized, display block
			h=5
			w=5
			list=(true true true true true true true true true true true true true true true true true true true true true true true true true )	#Display a 5x5 block
			;;
	esac
	if [ $Size -ne $h -o $Size -ne $w ]
	then
		echo 'SIZE MISMATCH ERROR'
		exit
	fi
	local a=$(($w * $i))
	local b=0
	local str=''
	while [ $b -lt $w ]	#Get line $i of banner letter
	do
		if [ ${list[$(($a+$b))]} == true ]
		then
			str+=$C1
		else
			str+=$C0
		fi
		((b++))
	done
	b=0
		while [ $b -lt $Spacing ]	#Add whitespace to Remainder
		do
			str+=$C0
			((b++))
		done
	Remainder[i]=$str
}

read -p $'What text do you want to display?\n' BannerText	#Get text to display
if [ $loop = true ]
then
	BannerText+=' ## '	#Buffer bewteen looped text
fi
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
			((n++))
		else
			Remainder[$i]=''
			whats_my_line	#Get $i line of letter $bannerText[$n]
			p=0
			while [ $j -lt $Width ]	#Add characters from ramaining banner letter until full display width
			do
				Output[$i]+=${Remainder[$i]:$p:1}
				((p++))
				((j++))
			done
		fi
	done
	echo ${Output[$i]} #$'\n'
	((i++))
done
sleep 1

while [ $n -lt $Length ]	#Increment through the banner text
do
	tput rc	#Return to saved cursor position (begining of the banner)
	if [ $p -ge $PadSize ]	#Completed banner letter, load next banner letter
	then
		((n++))	#Increment to the next banner letter
		if [ $n -eq $Length -a $loop = true ]
		then
			n=0
		fi
		i=0
		while [ $i -lt $Size ]	#Load next banner letter line by line
		do
			Remainder[$i]=''
			whats_my_line	#Get $i line of letter $BannerText[$n]
			#echo "Ramainder" $i $Remainder[$i]	#for testing
			((i++))
		done
		p=0	#Reset remainder position
		#sleep 1	#for testing
	fi
	i=0
	while [ $i -lt $Size ]	#Increment banner to the left line by line
	do
		Output[$i]=${Output[$i]:1}	#Remove first character of $Output[$i]
		Output[$i]+=${Remainder[$i]:$p:1}	#Add next character the end of $Output[$i]
		echo ${Output[$i]}
		#sleep 1	#for testing
		((i++))
	done
	((p++))
	sleep 0.2
done
