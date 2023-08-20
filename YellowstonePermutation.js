//Yellowstone Permutation
//
//PURPOSE: Output a series of numbers following the yellowstone purmutation
//LICENSE: THE UNLICENSE
//AUTHOR: CALEB GRISWOLD
//UPDATED: 2023-08-15
//
//YELLOWSTONE PERMUTATION:
//No terms are repeated
//Use the smallest valid number
//New term must be relatively prime to the previous term
//New term must have a common factor with the term before last

//const n = [1, 2, 3];		//Solution array
//const u = [1, 2, 3];		//Already used numbers
//const pf1 = [1];		//Prime factorization 1
//const pf2 = [1	];	//Prime factorization 2
//let min = 4;		//Smallest unused integer
//let x = 4;		//Guess for next term
//let i = 3;	//Array index

//i = n.length;
//min = smallestUnused(1)
//x = min
//Loop start
	//pf1 = primeFactors(n[i-1])
	//pf2 = primeFactors(x)
	//Loop while pf1 and pf2 share a common term:	//Find an unused integer that does not have a common factor with the previous term
		//x = smallestUnused(x)
		//pf2 = primeFactors(x)
	//Loop While End
	//pf1 = primeFactor(n[i-2])
	//If pf1 and pf2 share a common term {	//x has a common term with the term before last
		//n[i] = x
		//add2u(x)		//added x to the array u, in sorted order
		//If (x = min)	 {	//Smallest available integer was the next term
			//min = smallestUnused(min)		//New smallest unused integer
		//x = min
		//i++
	//} else {
		//x = smallestUnused(x)
	//}
//}

//Functions:
	//Prime factorization, save result?
	//Smallest unused integer (larger than invalid option)
	//Add a integer to the array u
	//Shared terms between pf1 and pf2

function smallestUnused(m){ //finds the smallest unused integer greater than m
	//let j = m - 1;
//if (u[j] = m) { //all integers less than m have been used, start at m
//} else { //there are missing integers before m, work backwards to m
//loop while u[j] > m and u[j] != j+1 {
//j--;
//}
//}
//let l = u.length;
//let y = u[j];
//while j < l {
//if (u[j+1] = y + 1) {
//j++;
//y++;
//} else {
//y++, exit loop
//}
//retrun y
}