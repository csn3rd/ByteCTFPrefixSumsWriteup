# Prefix Sums

## Problem Statement
![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem%20Description.png)

Attached to the problem is a pdf of the problem statement. The pdf can be viewed and downloaded [here](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem_Statement.pdf).

For convenience, here is a screenshot of the problem statement as well.
![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem_Statement.png)

## Problem Breakdown
Our first step is to read the problem and fully understand the meaningful information.

Let's break down the problem. The first sentence explains that we have some sequence of *N* elements consisting of 0's and 1's. Then, the definition of a prefix sum is defined where S<sub>k</sub> is the sum of the first *k* elements within the sequence. Since the sequence only contains 0's and 1's, S<sub>k</sub> is pretty much the number of 1's in the first *k* characters of the sequence. Next, we are told that there are *p* 0's within the sequence. The variables *N* and *p* are now defined within the context of this problem.

Next, we are given the important property which helps us determine the probability. We are trying to test if the sequence passes the condition that "2S<sub>k</sub> - *k* > 0 ∀*k* between 1 and *N*" (Note ∀ means "for all"). Let's simplify this. We can move *k* and the coefficient factor of 2 to the other side to get the equivalent inequality of "S<sub>k</sub> > *k*/2". So, the numerator will be the number of sequences which fulfill the conditions and the denominator will be the total number of possible sequences of length *N* and *p* 0's.

The last sentence in this section indicates that *p* < (*N*-*p*). This is necessary because if *p* >= (*N*-*p*), then when *k* = *N*, the condition is not satisfied and the total probability is 0.

In the second section, we are told how to get the flag. We must simplify the fraction to its simplest terms. We take the numerator and denominator and append the two together as strings. Then, we convert this value to hex and put it into the flag format. We are given a hash to confirm our solution.

(**TL;DR**: We are tasked to find the probability that a binary sequence of length *N* containing *p* 0's meets a given condition. We must find the simplest fractional representation of the probability and manipulate it to form the flag.)

It is important to note that *N* > 10<sup>18</sup> and *p* > 10<sup>14</sup>. Therefore, a solution that runs within a reasonable time must have a runtime of O(1), O(lg *p*), or O(lg *N*). Worst case if we can't find an efficient solution, we will have to find an O(*p*) solution which would run for over 36 hours but less 60 hours (may fall within the bounds of the contest, a 72 hour event).

## Determining Relationships
Now that we understand the problem, our next step is to start writing out some cases and recognizing any relationships or patterns between the variables and valid sequences.

### Relationship between *N* and No. of Valid Sequences
<sup>Note: Because of the rapidly growing sizes of the number of possible binary sequences, the writeup will feature images which only show the cases with *N* going up to size 5. Check out [this pdf](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Conditions_Analysis.pdf) for cases where *N* goes up to size 7.</sup>

Let's start out by creating a table of all the possible binary sequences given different values of *N*. Here is the table of cases when *N* is size 1 to 5.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/List%20of%20Sequences.png)

Let's highlight in yellow the cases which satisfy the condition "2S<sub>k</sub> - *k* > 0" when *k* = *N*. We know that this is equivalent to "S<sub>k</sub> > *k*/2" and S<sub>k</sub> is the number of 1's. So, we will highlight a sequence if it contains more than *N*/2 1's.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Satsify%20Condition%20for%20Size%20k.png)

Of course, the problem is asking for sequences which satisfy "2S<sub>k</sub> - *k* > 0" for all *k* values, not just when *k* = *N*. We have marked all the conditions which work when *k* = *N* so we can ignore the uncolored cases. To confirm whether a sequence matches the condition for all *k* < *N*, we will check if all of its "prefixes" are marked as yellow from the previous step. We will highlight the sequence green if it is a valid sequence for all *k*.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Conditions_Analysis.png)

Now, we can count up the number of valid sequences for each N up to *N* = 5 (7 in the pdf). We  have now created 2 sequences of numbers which we can look up on the On-Line Encyclopedia of Integer Sequences (OEIS) and help us extrapolate the values for future steps when needed. The sequence id's are attached to the end of their corresponding rows. The sequence which matters to us is the green one, id: A001405, as that describes the number of valid sequences for a given size. According to OEIS, the number of valid sequences for a size *N* can be defined by a function, f(*N*) = binomial(*N*, floor(*N*/2)).

### Relationship between *N*, *p*, and No. of Valid Sequences
In the last step, we found the function which describes the number of valid sequences for any given size *N*. Let's break it down further and calculate the number of valid sequences for any given size *N* containing *p* zeroes (this is going to be the numerator of the probability).

From the previous table of all possible binary sequences, we can go through each green sequence and count up how many zeroes the string contains. This counts as one valid sequence for its corresponding size and its corresponding number of 0s'. We will do this for each of the green sequences and this will help us create a table where the value at the *j*th column and *i*th row denotes the number of valid sequences of size *j* containing *i* 0's.

Here is the table (highlighted in purple) containing the number of valid sequences for the first 12 possible sizes *N* and the first 6 possibilities of *p*. The table can be also be found in [this pdf](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Probabilities_Table.pdf) if the image is too small or unclear.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Probabilities_Table.png)

From this table, we can notice several patterns. The simplest pattern to recognize is the fact for some random cell in row *i* and column *j*, the value in the cell is equivalent to the sum of its adjacent cell to the left and the cell above that one (the up-left cell). While this does find the correct numerator for the probability, it is implausible to implement this as a solution for the given inputs as it would require O(*Np*) memory and runtime. Since we are looking for a more efficient solution, we should look for patterns which define a row or column. If some function or equation could be determined for each row or column, we may be looking at an O(*N*) or O(*p*) solution which may guide us closer to an efficient solution.

Another simple pattern we recognize is the fact that when *p* = 0, there is only one valid sequence regardless of *N*. When *p* = 1, the number of valid sequences seems to be counting up by 1. It is harder to recognize patterns for the next few rows. We can look up each of he sequences on OEIS and determine if there are any functions which define each row. We will denote these functions as a(n) as used by OEIS. So, when *p* = 0, we have sequence A000012 and a(n) = 1. When *p* = 1, we have sequence A000027 and a(n) = n. However, in the table, the sequence is shifted to the right by 2 so n = size-2. For *p* = 2, we have sequence A000096 and a(n) = n(n+3)/2. In the table, the sequence is shifted to the right by 4 so n = size-4. For *p* = 3, we have sequence A005586, a(n) = n(n+4)(n+5)/6, and n = size-6. We have sequence A005587, a(n) = n(n+5)(n+6)(n+7)/24, and n = size-8 for *p* = 4. And finally, for *p* = 5, we have sequence A005557 and a(n) = n(n+6)(n+7)(n+8)(n+9)/120. This is shifted to the right by 10 in the table so n = size-10.

Let's substitue in n for the size to make them easier to work with. For *p* = 0, we have a(size) = 1. For *p* = 1, we have a(size) = size-2. For *p* = 2, we have a(size) = (size-4)(size-1)/2. For *p* = 3, we have a(size) = (size-6)(size-2)(size-1)/6. For *p* = 4, we have a(size) = (size-8)(size-3)(size-2)(size-1)/24. For *p* = 5, we have (size-10)(size-4)(size-3)(size-2)(size-1)/120. From here, we start to notice some patterns. In the numerator, we seem to have a first term of size-2*p*. Then, we have (size-*p*), (size-(*p*-1)), (size-(*p*-2)), and so on until (size-1). This is equivalent to (size-1)!/(size-*p*)!. In the denominator, we have *p*!. By putting this all together, we get (size-2*p*)(size-1)! in the numerator and (size-*p*)!(*p*)! in the denominator. 

In this function, the largest factorial is (size-1)! and the runtime to calculate this would be O(*N*-1). In addition, *N* goes up to 10<sup>18</sup> so it would require large amounts of memory to store the factorial values. Thus, if we were to implement this function to calculate the number of valid cases for some given size *N* containing *p* 0's, this function may still be too slow and the numbers may get too large.

Going back to the table, there does not seem to be any patterns for each individual column so we seem to have found the most efficient way to calculate the numerator of the probability. Of course, we still have to calculate the denominator of the probability and that may help us find a better solution or find some simplifications.

### Relationship between *N*, *p*, and Total No. of Sequences
The denominator of the probability is the total number of sequences given size *N* and *p* 0's. Let's go back to the first table with the exhaustive list of all binary sequences. We will go through each of the sequences and count up how many zeroes the string contains. This will help us create a table where the value at the *j*th column and *i*th row denotes the number of sequences of size *j* containing *i* 0's.

Here is the table (highlighted in orange) containing the number of sequences for the first 12 possible sizes *N* and the first 6 possibilities of *p*. The table can be also be found in [this pdf](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Probabilities_Table.pdf) if the image is too small or unclear.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Probabilities_Table.png)

Entering each row into OEIS, we discover that the function which describes each row is binomial(n, row). In this case n = size and row = *p*. Thus, the function which describes the total number of sequences is binomial(size, *p*).

According to the binomial theorem, binomial(n, r) = n! / r!(n-r)!. 

So, the denominator of the probability is size! / (*p*)!(size-*p*)!.

### Combining and Simplifying the Probability

In the numerator, we have (size-2*p*)(size-1)! / (size-*p*)!(*p*)!. In the denominator, we have size! / (*p*)!(size-*p*)!. Dividing fractions is equivalent to multiplying the first fraction by the reciprocal of the second. So, the probability is (size-2*p*)(size-1)!(*p*)!(size-*p*)! / (size-*p*)!(*p*)!(size)!. We can see that (*p*)! and (size-*p*)! are found in both the numerator and the denominator and cancel out. We now have (size-2*p*)(size-1)! / (size)!. We know that (size)! is equivalent to size \* (size-1)! and so we can rewrite the probability as (size-2*p*)(size-1)! / (size)(size-1)!. The two (size-1)! terms cancel out and we are left with (size-2*p*) / (size).

Taking a look at what we have, the probability which we are trying to find can be found in O(1) time! This is very fast and will clearly find our answer within seconds.

### Writing Code to Get the Flag

We now have an O(1) solution to getting the probability. Since the numbers are very large, we will use python for our solution. As denoted in the problem statement, we'll name the numerator *a* and the denominator *b*. Let's start writing our *get_flag()* function. We'll create a file called *prefix_sums.py*. 

```
def get_flag(n, p):
	a = n-2*p
	b = n
```

Next, the problem statment tells us that we need to simplify our fraction to the simplest terms, such that the GCD of *a* and *b* is 1.

```
from math import gcd

def get_flag(n, p):
	a = n-2*p
	b = n

	factor = gcd(a, b)

	a = a//factor
	b = b//factor

	print("simplified fraction:\t\t" + str(a) + "/" + str(b))
```

We can use the gcd function in the math library to help us simplify our fraction by fiding the common divisor then dividing both *a* and *b* by that common divisor. We can print it out to confirm that the fraction looks correct.

Next, we need to concatenate *a* and *b* together as strings. We need to convert that string to decimal and then convert it to hex. Last, we need to enclose the hex value by the flag format.

```
from math import gcd

def get_flag(n, p):
	a = n-2*p
	b = n

	factor = gcd(a, b)

	a = a//factor
	b = b//factor

	print("simplified fraction:\t\t" + str(a) + "/" + str(b))

	dec = int(str(a) + str(b))
	flag = "flag{" + hex(dec) + "}"

	print("flag:\t\t\t\t" + flag)
```

This is the code to form the flag string.

In the problem statement, we were also given the md5 hash of the flag. We can use the md5 encoding function in the hashlib function to help us confirm that we have found the correct flag.

```
from math import gcd
import hashlib

def get_flag(n, p):
	a = n-2*p
	b = n

	factor = gcd(a, b)

	a = a//factor
	b = b//factor

	print("simplified fraction:\t\t" + str(a) + "/" + str(b))

	dec = int(str(a) + str(b))
	flag = "flag{" + hex(dec) + "}"

	print("flag:\t\t\t\t" + flag)

	hash = hashlib.md5(flag.encode()).hexdigest()

	if hash == "6046f30cf9e942ed47c88621a69ed0b2":
		print("flag is correct. hash:\t\t" + hash)
	else:
		print("flag is incorrect. hash:\t" + hash)
```

Our *get_flag()* function is now complete.

We can set *N* and *p* to the values we are given and call the *get_flag* function() to get our final result. Append the following lines and our code is complete.

```
n = 3141592653589793238
p = 101124131231734
get_flag(n, p)
```

We can run our code by traversing to the directory of our code in terminal / command prompt. Type in the command `python3 prefix_sums.py` and we receive our flag.

Flag: `flag{0xbd10c864dce5299aadd5b7aac2124eb}`
