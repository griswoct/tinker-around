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
//
//array n = 1, 2, 3		//Solution array
//array u = 1, 2, 3		//Already used numbers
//array pf1 = 1		//Prime factorization 1
//array pf2 = 1		//Prime factorization 2
//int min = 4		//Smallest unused integer
//int x = 4		//Guess for next term
//int i = 3		//Array index
//
//i = (size of n) - 1
//min = smallestUnused(0)
//x = min
//Loop start
	//pf1 = primeFactors(n[i-1])
	//pf2 = primeFactors(x)
	//Loop while pf1 and pf2 share a common term:	//Find an unused integer that does not have a common factor with the previous term
		//x = smallestUnused(x)
		//pf2 = primeFactors(x)
	//Loop While End
	//pf1 = primeFactor(n[i-2])
	//If pf1 and pf2 share a common term:	//x has a common term with the term before last
		//n[i] = x
		//add2U(x)		//added x to the array u, in sorted order
		//If x = min:		//Smallest available integer was the next term
			//min = smallestUnused(min)		//New smallest unused integer
		//End If
		//x = min
		//i++
	//Else:
		//x = smallestUnused(x)
	//End If
//Loop end

//Functions:
	//Prime factorization, save result?
	//Smallest unused integer (larger than invalid option)
	//Add a integer to the array u
	//Shared terms between pf1 and pf2
