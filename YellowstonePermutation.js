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
const u = [1, 2, 3];	//Already used numbers
const pf1 = [1];	//Prime factorization 1
const pf2 = [1];	//Prime factorization 2
const numTerms = 10;	//number of terms to calculate
let min = 4;	//Smallest unused integer
let x = 4;	//Guess for next term
let i = 3;	//Array index

i = n.length;
min = smallestUnused(1)
x = min
for (let h = 0; h < numTerms; h++) {
	pf1 = primeFactors(n[i-1])
	pf2 = primeFactors(x)
	while (commonFactor() == true) {	//Find an unused integer that does not have a common factor with the previous term
		x = smallestUnused(x)
		pf2 = primeFactors(x)
	}
	pf1 = primeFactor(n[i-2])
	If (commonFactor() == true) {	//x has a common term with the term before last
		n[i] = x
		add2u(x)		//added x to the array u, in sorted order
		If (x == min)	{	//Smallest available integer was the next term
			min = smallestUnused(min)		//New smallest unused integer
		x = min
		i++
		} else {
		x = smallestUnused(x)
		}
	}
}

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

function primeFactors(p) {	//Find the prime factors of p
	//PLACEHOLDER
}

function add2u(m) {	//Adds n to the list of used integers (array u)
	u.push(m);	//add m to array u
	u.sort(function(a, b){return a - b});	//sort array u by numberic value
}

function commonFactor() {	//return true if two arrays share a common term
	let j = 0;
	let k = 0;
	while ((j < pf1.length) && (k < pf2.length)) {	//array indexes must be within the lengths of the arrays
		if (pf1[j] == pf2[k]) {	//found a common factor
			return true;
		} else {	//adjust j or k
			if (pf1[j] < pf2[k]) {	//pf1 and pf2 must but in numerical order
				j++;
			} else {
				k++;
			}
		}
	}
	return false;
}
