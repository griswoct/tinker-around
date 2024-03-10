#!/bin/bash

#LETTER DENSITY
#
#PURPOSE: FIND THE DISPLAY DENSITY OF A 5x5 LETTER (BLACK:WHITE PIXALS)
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2024-03-09
#
# Ideads:
#Find the density of each quadrant to get an idea of the density distribution (upper left, upper right, lower left, lower right, middle?)
#use these values for first attempt at ASCII Art generator

density=0
letters=['A','B','C']
read -p 'Which letters do you want to find the density of? ' letters
length=${#letters}
list=()
while [ $i < $length ]
do
	$density=0
	case ${letters:$i:1} in
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
		0)
			h=5
			w=5
			list=(false true true true false true false false true true true false true false true true true false false true false true true true false
 )
			;;
		1)
			h=5
			w=5
			list=(false true true false false false false true false false false false true false false false false true false false false true true true false)
			;;
		2)
			h=5
			w=5
			list=(false true true true false true false false false true false false false true false false true false false false true true true true true)
			;;
		3)
			h=5
			w=5
			list=(true true true true false false false false false true false true true true false false false false false true true true true true false)
			;;
		4)
			h=5
			w=5
			list=(true false false true false true false false true false true true true true true false false false true false false false false true false)
			;;
		5)
			h=5
			w=5
			list=(true true true true true true false false false false true true true true false false false false false true true true true true false)
			;;
		6)
			h=5
			w=5
			list=(false false true false false false true false false false true false true true false true false false false true false true true true false)
			;;
		7)
			h=5
			w=5
			list=(true true true true true false false false true false false false true false false false true false false false true false false false false)
			;;
		8)
			h=5
			w=5
			list=(false true true true false true false false false true false true true true false true false false false true false true true true false)
			;;
		9)
			h=5
			w=5
			list=(false true true true false true false false false true false true true true false false false true false false false true false false false)
			;;
		*)	#Character not recognized, display block
			h=5
			w=5
			list=(true true true true true true true true true true true true true true true true true true true true true true true true true )	#Display a 5x5 block
			;;
	esac
	while [ $j -lt 25 ]	#Get line $i of banner letter
	do
		if [ ${list[$j]} == true ]
		then
			density=$((density+1))
			#add check for each quadrant here
		fi
		((j++))
	done
	density=$((4*density))
 	echo "Density of " ${letters:$i:1} ": " $density
 	((i++))
done
