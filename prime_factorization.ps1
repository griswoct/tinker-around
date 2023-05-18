#PRIME FACTORIZATION
#
#PURPOSE: FIND THE PRIME FACTORIZATION OF AN INTEGER USING POWERSHELL
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 2023-05-18
#
$n = 2
[int]$n = Read-Host "What number would you like to factor?"
If ($n -lt 2) {
	for (; $n -lt 2;)
	{
		Write-Host "The number to be factored must be greater than 1"
		[int]$n = Read-Host "What number would you like to factor?"
	}
}
if ($n -eq 4) {
	Write-Host "Prime factors for" $n ": 2 2"
	Start-Sleep -Seconds 3
	exit
}
elseif ($n -le 5) {
	Write-Host "Prime factors for" $n ":" $n
	Start-Sleep -Seconds 3
	exit
}
$primes = @(2)
for ($i = 2; $i -le $n; $i++)
{
	for ($j = 0; $j -lt $primes.Length;)	#itterate through primes
	{
		if ($i % $primes[$j] -eq 0) {	#Not a new prime
			$j = $primes.Length	#Exit for j
		}
		elseif ($j -eq ($primes.Length - 1)) {	#New prime
			$primes += $i	#Add i to list of primes
			$j += 2	#Exit for j
			#Write-Host $i "is prime!"
		}
		else {
			$j++	#Itterate through primes list
		}
	}
}
Write-Host "Primes up to:" $n ":" $primes
$m = $n
$factors = @()
for ($k = 0; $k -lt $primes.Length;)	#Check divisibility by primes up to n
{
	if (($m % $primes[$k]) -eq 0) {	#Is primes[k] a factor?
		$factors += $primes[$k]	#add p to list of factors
		$m = ($m / $primes[$k])	#New factor to evaluate
		#$k = 0	#<-- is this necessary?
	}
	elseif ($primes[$k] -gt $n) {
		$k = $primes.Length		#exit for k
	}
	else {
		$k++	#Next prime
	}
}
Write-Host "Prime factors for" $n ":" $factors
Start-Sleep -Seconds 3
