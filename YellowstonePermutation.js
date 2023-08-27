//Yellowstone Permutation
//
//PURPOSE: Output a series of numbers following the yellowstone purmutation
//LICENSE: THE UNLICENSE
//AUTHOR: CALEB GRISWOLD
//UPDATED: 2023-08-27
//
//YELLOWSTONE PERMUTATION:
//No terms are repeated
//Use the smallest valid number
//New term must be relatively prime to the previous term
//New term must have a common factor with the term before last

const n = [1, 2, 3];	//Solution array
const u = [1, 2, 3];	//Already used numbers
const p = [2, 3];	//List of prime numbers
var pf0 = [1];	//Prime factorization of current term option
var pf1 = [1];	//Prime factorization of previous term (back 1)
var pf2 = [1];	//Prime factorization of term before last (back 2)
const numTerms = 24;	//number of terms to calculate
let min = u[u.length - 1] + 1;	//Smallest unused integer
let x = 4;	//Guess for next term
let i = 3;	//Array index

i = n.length;
min = smallestUnused(3)
x = min;
pf1 = primeFactors(n[i-1]);
while (i < numTerms) {	//Find the first numTerms terms
	pf0 = primeFactors(x);
	while (commonFactor(pf0, pf1) == true) {	//Find an unused integer that does not have a common factor with the previous term
		x = smallestUnused(x);
		pf0 = primeFactors(x);
	}
	pf2 = primeFactors(n[i-2])
	if (commonFactor(pf0, pf2) == true) {	//x has a common term with the term before last
		n[i] = x;	//Next term found!
		add2u(x);	//added x to the array u, in sorted order
		i++;
		pf2 = pf1;	//Prime factors term shift: term n-1 becomes term n-2
		pf1 = pf0;	////Prime factors term shift: term n becomes term n-1
		if (x == min) {	//Smallest available integer was the next term
			min = smallestUnused(3);		//New smallest unused integer
		}
		x = min;
	} else {
		x = smallestUnused(x);	//x does not have a common factor with the term before last, try the next unused integer
	}
}
alert(n);

function smallestUnused(m){ //finds the smallest unused integer greater than m
	let j = m;
	let y = 0;
	let l = u.length;
	if (j >= l) {
		j = l - 1;	//Index last used number
		
	}
	while (u[j] > m) {
		if (u[j] != j + 1) {	//previous integers still missing
			j--;	//work backwards
		} else {
			break;
		}
	}
	y = u[j] + 1;
	while (y <= m) {	//y must be at least m
		y++;
	}
	while (y == u[j+1]) {	//m is in a block of used numbers
		y++;
		j++;
	}
	return y;	//smallest unused integer greater than m
}

function primeFactors(m) {	//Find the prime factors of p
	const factors = [];	//Prime factors
	let j = 0;	//Primes index
	let k = 0; 	//Factors index
	if (m < 4) {	//Integers less than four are primes
		factors[k] = m;
		return factors;
	} else {
		if (p[p.length - 1] < m) {	//Largest prime in array p is less than m
			generatePrimes(m);	//Get all primes through m
		}
		while (m > 1) {	//Itterate through primes
			if (m % p[j] == 0) {	//p[j] is a prime factor
				factors[k] = (p[j]);	//Add p[j] to factors
				k++;	//Next factor
				m /= p[j];
			} else {	//p[j] is not a factor
				if (m / p[j] < p[j]) {	//No more primes, exceeded square root
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

function generatePrimes(limit) {	//Generate additional prime numbers up to limit
	let m = p[p.length - 1] + 2;	//Start checking at next odd after last prime
	let j = 0;
	while (m <= limit + 1) {	//Find primes up through limit
		if (m % p[j] == 0) {	//m is not prime
			m += 2;	//Next odd m (2 is the only even prime)
			j = 0;
		} else {	//m might be prime
			j++;	//Next prime
			if (j == p.length) {	//New Prime
				p.push(m);
				m += 2;
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