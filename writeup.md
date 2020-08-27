# Prefix Sums

## Problem Statement
![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem%20Description.png)

Attached to the problem is a pdf of the problem statement. The pdf can be viewed and downloaded [here](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem_Statement.pdf).

For convenience, here is a screenshot of the problem statement as well.
![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Problem_Statement.png)

## Problem Breakdown
Our first step is to read the problem and fully understand the meaningful information.

Let's break down the problem. The first sentence explains that we have some sequence of *N* elements consisting of 0's and 1's. Then, the definition of a prefix sum is defined where S<sub>k</sub> is the sum of the first *k* elements within the sequence. Since the sequence only contains 0's and 1's, S<sub>k</sub> is pretty much the number of 1's in the first *k* characters of the sequence. Next, we are told that there are *p* 0's within the sequence. The variables *N* and *p* are now defined within the context of this problem.

Next, we are given the important property which helps us determine the probability. We are trying to test if the sequence passes the condition that "2S<sub>k</sub> - *k* > 0 ∀*k* between 1 and *N*" (Note ∀ means "for all"). Let's simplify this. We can move *k* and the coefficient factor of 2 to the other side to get the equivalent inequality of "S<sub>k</sub> > *k*/2". At the end, we are told that *p* < (*N*-*p*). This is necessary because if *p* >= (*N*-*p*), then when *k* = *N*, the condition is not satisfied and the total probability is 0.

In the second section, we are told how to get the flag. We must simplify the fraction to its simplest terms. We take the numerator and denominator and append the two together as strings. Then, we convert this value to hex and put it into the flag format. We are given a hash to confirm our solution.

**TL;DR: We are tasked to find the probability that a binary sequence of length *N* containing *p* 0's meets a given condition. We must find the simplest fractional representation of the probability and manipulate it to form the flag.**

It is important to note that *N* > 10<sup>18</sup> and *p* > 10<sup>14</sup>. Therefore, a solution that runs within a reasonable time must have a runtime of O(1), O(lg *p*), or O(lg *N*). Worst case if we can't find an efficient solution, we will have to find an O(*p*) solution which would run for over 36 hours but less 60 hours (may fall within the bounds of the contest, a 72 hour event).

## Determining Relationships
Now that we understand the problem, our next step is to start writing out some cases and recognizing any relationships or patterns between the variables and valid sequences.

### Relationship between *N* and No. of Valid Sequences
<sup>Note: Because of the rapidly growing sizes of the number of possible binary sequences, the writeup will feature images which only show the cases with *N* going up to size 5. Check out [this pdf](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Conditions_Analysis.pdf) for cases where *N* goes up to size 7.</sup>

Let's start out by creating a table of all the possible binary sequences given different values of *N*. Here is the table of cases when *N* is size 1 to 5.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/List%20of%20Sequences.png)

Let's highlight in yellow the cases which satisfy the condition "2S<sub>k</sub> - *k* > 0" when *k* = *N*. We know that this is equivalent to "S<sub>k</sub> > *k*/2" and S<sub>k</sub> is the number of 1's. So, we will highlight a sequence if there are more than *N*/2 1's.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Satsify%20Condition%20for%20Size%20k.png)

Of course, the problem is asking for sequences which satisfy "2S<sub>k</sub> - *k* > 0" for all *k* values, not just when *k* = *N*. We have marked all the conditions which work when *k* = *N* so we can ignore the other cases. To confirm whether a sequence matches the full conditions without the restriction on *k*, we will check if all of its "prefixes" are marked as yellow from the previous step. We will highlight the sequence green if it satisfies the full condition and is a valid sequence.

![](https://github.com/csn3rd/ByteCTFAlgoWriteup/blob/master/Brute_Force_Conditions_Analysis.png)

Now, we can count up the number of yellow and green cases for each N. We have calculated the number of yellow and green cases up to *N* = 5 (7 in the pdf). Our findings now create 2 sequences of numbers which we can look up on the On-Line Encyclopedia of Integer Sequences (OEIS) and help us extrapolate the values for future steps when needed. The sequence id's are attached to the end of their corresponding rows.

### Relationship between *N*, *V*, and No. of Valid Sequences

**To be continued...**
