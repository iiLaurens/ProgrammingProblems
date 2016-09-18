"""
Zombit pandemic
===============

The nefarious Professor Boolean is up to his usual tricks. This time he is
using social engineering to achieve his twisted goal of infecting all the
rabbits and turning them into zombits! Having studied rabbits at length,
he found that rabbits have a strange quirk: when placed in a group,
each rabbit nudges exactly one rabbit other than itself.
This other rabbit is chosen with uniform probability. We consider two
rabbits to have socialized if either or both of them nudged the other.
(Thus many rabbits could have nudged the same rabbit, and two rabbits may
have socialized twice.) We consider two rabbits A and B to belong
to the same rabbit warren if they have socialized, or if A has socialized
with a rabbit belonging to the same warren as B.

For example, suppose there were 7 rabbits in Professor Boolean's nefarious lab.
We denote each rabbit using a number. The nudges may be as follows:

1 nudges 2
2 nudges 1
3 nudges 7
4 nudges 5
5 nudges 1
6 nudges 5
7 nudges 3

This results in the rabbit warrens {1, 2, 4, 5, 6} and {3, 7}.

Professor Boolean realized that by infecting one rabbit, eventually it would
infect the rest of the rabbits in the same warren! Unfortunately, due to
budget constraints he can only infect one rabbit, thus infecting only the
rabbits in one warren. He ponders, what is the expected maximum number of
rabbits he could infect?

Write a function answer(n), which returns the expected maximum number of
rabbits Professor Boolean can infect given n, the number of rabbits.

n will be an integer between 2 and 50 inclusive. Give the answer as a string
representing a fraction in lowest terms, in the form "numerator/denominator".
Note that the numbers may be large.

For example, if there were 4 rabbits, he could infect
a maximum of 2 (when they pair up) or 4 (when they're all socialized),
but the expected value is 106 / 27. Therefore the answer would be "106/27".
"""

from itertools import groupby
from math import factorial
from fractions import Fraction

def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

@memodict
def f(n):
    return factorial(n)

def nCr(n,r):
    return f(n) / f(r) / f(n-r) if n > 0 else 1

@memodict
def chunk_permutations(n):
    # Some intensive googling brought me to sequence A000435 (knowing that it must
    # start with {0, 0, 1, 8, 78}), which equates to the number of maximally directed
    # pseudoforests with n nodes that contains only one tree. We need this amount to 
    # calculate the probability of this chunk. This function is what makes this
    # particular Foobar problem so hard.
    #
    # a(n) = (n-1)! * Sum (n^k/k!, k=0..n-2)
    
    return (f(n-1) * sum([Fraction(n**k, f(k)) for k in range(n-1)])).numerator

def partitions(n, min=2): 
    # This function forms every possible way we can partition
    # n bunnies, with a lower bound on the group size.
    
    for chunk in range(min, n // 2 + 1):
        # Fix one chunk of bunnies by size and put the
        # remaining bunnies in this function to receive
        # all possible partition of the remaining bunnies.
        # Note that we want to avoid permutations of the same
        # group sizes, so adapt the lower bound to maintain
        # group partitions of increasing group size.
        
        for subchunks in partitions(n - chunk, chunk):
            yield [chunk] + subchunks
            
    # Don't forget the possibility of simply keeping all bunnies
    # in one group.
    yield [n]

def answer(n):
    # Every bunny can choose any other bunny than itself. So the total
    # number of possibilities that the bunnies can nudge is:
    denominator = (n-1)**n
    
    expectation = 0
    for partition in partitions(n):
        remainder = n
        numerator = 1
        # Use the multinomial distribution to calculate in how many
        # ways we can partition the n bunnies into the partitioned chunks
        for chunk in partition:
            numerator *= nCr(remainder, chunk) * chunk_permutations(chunk)
            remainder -= chunk
            
        # Chunks in our situation are unlabeled and the multinominal distribution
        # assumed labeled chunks. Chunks of the same size can be permuted interchangably
        # so we need to divide by the all the ways that chunks can be permuted.
        for frequency in [len(list(group)) for key, group in groupby(partition)]:
            numerator /= f(frequency)
        
        # The probability that this particular partition occurs is numerator / denominator.
        # The largest chunk of bunnies is the final chunk, by construction.
        # The expectation is simply the sum of the probability of each partition times
        # the largest chunk. So add this particular partition to the sum.
        expectation += partition[-1] * numerator
    
    #
    return str(Fraction(expectation, denominator).numerator) + "/" + str(Fraction(expectation, denominator).denominator)
