//Yellowstone Permutation
//
//PURPOSE: Output a series of numbers following the yellowstone purmutation
//LICENSE: THE UNLICENSE
//AUTHOR: CALEB GRISWOLD
//UPDATED: 2023-08-26
//
//YELLOWSTONE PERMUTATION:
//No terms are repeated
//Use the smallest valid number
//New term must be relatively prime to the previous term
//New term must have a common factor with the term before last

const n = [1, 2, 3];	//Solution array
const u = n;	//Already used numbers
const p = [2];	//List of prime numbers
const pf0 = [1];	//Prime factorization of current term option
const pf1 = [1];	//Prime factorization of previous term (back 1)
const pf2 = [1];	//Prime factorization of term before last (back 2)
const numTerms = 10;	//number of terms to calculate
let min = u[u.length - 1] + 1;	//Smallest unused integer
let x = 4;	//Guess for next term
let i = 3;	//Array index

i = n.length;
min = smallestUnused(1)
x = min;
for (let h = 0; h < numTerms; h++) {
	pf1 = primeFactors(n[i-1]);
	pf0 = primeFactors(x);
	while (commonFactor(pf0, pf1) == true) {	//Find an unused integer that does not have a common factor with the previous term
		x = smallestUnused(x);
		pf0 = primeFactors(x);
	}
	pf2 = primeFactor(n[i-2])
	If (commonFactor(pf0, pf2) == true) {	//x has a common term with the term before last
		n[i] = x;
		add2u(x);	//added x to the array u, in sorted order
		If (x == min) {	//Smallest available integer was the next term
			min = smallestUnused(min);		//New smallest unused integer
		x = min;
		i++;
		} else {
		x = smallestUnused(x);
		}
	}
}
alert(n);

function smallestUnused(m){ //finds the smallest unused integer greater than m
	let j = m - 1;
	if (u[j] != m) {	//there are missing integers before m, work backwards to m
		while (u[j] > m) {
			if (u[j] != j + 1) {	//previous integers still missing
				j--;	//work backwards
			} else {
				break;
			}
		}
	}
	let l = u.length;
	let y = u[j];
	while (j < l) {	//index j must stay within array u
		if (u[j+1] == y + 1) {	//all intergers through j+1 used
			j++;
			y++;
		} else {	//found unused integer
			y++;	//y is the first option
			break;
		}
	}
	retrun y;	//smallest unused integer greater than m
}

function primeFactors(m) {	//Find the prime factors of p
	const factors = [];	//Prime factors
	let j = 0;	//Index
	if (m == 1) {
		factors[0] = 1;
		return factors;
	} else if (m == 2) {
		factors[0] = 2;
		return factors;
	} else {
		//need to check largest prime number in array p
			//If the lasrgest prime is too small, find another prime
		while (m > 1) {	//Itterate through primes
			if (m % p[j] == 0) {	//p[j] is a prime factor
				factors.push(p[j]);
				m /= p[j];
				if (m == 1) {	//All prime factors found
					return factors;
				}
			} else {	//p[j] is not a factor
				if (m / p[j] < p[j])) {	//No more primes, exceeded square root
					factors.push(m);	//Last prime factor is m
					return factors;
				} else {
					j++;	//Next prime
				}
			}
		}
	}
	return factors;
}

function generatePrimes(limit) {	//Generate additional prime numbers up to m
	let m = p[p.length - 1] + 1;	//Start at last prime + 1
	let j = 0;
	while (m < limit) {	//Find primes up to limit
		if (m % p[j] == 0) {	//m is not prime
			m++;	//Next m
			j = 0;
		} else {	//m might be prime
			j++;	//Next prime
			if (j == p.length) {	//New Prime
				p.push(m);
				m++;
				j = 0;
			}
		}
	}
}

function add2u(m) {	//Adds n to the list of used integers (array u)
	u.push(m);	//add m to array u
	u.sort(function(a, b){return a - b});	//sort array u by numberic value
}

function commonFactor(factors1, factors2) {	//return true if two arrays share a common term
	let j = 0;
	let k = 0;
	while ((j < factors1.length) && (k < factors2.length)) {	//array indexes must be within the lengths of the arrays
		if (factors1[j] == factors2[k]) {	//found a common factor
			return true;
		} else {	//adjust j or k
			if (factors1[j] < factors2[k]) {	//pf1 and pf2 must but in numerical order
				j++;
			} else {
				k++;
			}
		}
	}
	return false;
}
