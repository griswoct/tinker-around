#1. Find the factors of a particular number
#2. Find a list of primes (up to a limit)
#3. Find the factors for a list of numbers (up to a limit)


#1. FIND THE FACTORS OF N:
#get number $n
#If $n -lt 4:
	#echo "1, " & $n
	#exit
#get square root of $n: $sqrtn
#generate list of $primes through $sqrtn
	#Call #2, input $sqrtn, get $primes
#$m = $n
#for (each $p in $primes; until $p > $sqrtn)
{
	#If $m mod $p = 0:
		#append $p to $factors
		#$m = $m / $p
		#set $p index to 0
	#Else:
		#next $p
}
#list $factors

#2. FIND LIST OF PRIMES LESS THAN X:
#get $x
#If x -lt 2:
	#for (; $x -lt 2;)
	{
		#echo "Number must be greater than 1"
		#get $x
	}
#$primes = [2]
#for ($i = 2; $i -lt $x; $i++)
{
	#for ($p in $primes)
	{
		#If $i mod $p = 0:	#Not a new prime
			#exit for loop
		#Else If last $p:	#No factor in primes, new prime
			#Append $i to $primes
		#Else:
			#next $p
	}
}
#return $primes

#3. FIND THE FACTORS FOR ALL NUMBERS UP TO Y:
#get y
for ($j = 2; j -lt $y; $j++)
{
	#Call #1, input $j, get $factors
	#write $j & "factors: " & $factors
}
