"""
Line up the captives
====================

As you ponder sneaky strategies for assisting with the great rabbit escape,
you realize that you have an opportunity to fool Professor Booleans guards
into thinking there are fewer rabbits total than there actually are.

By cleverly lining up the rabbits of different heights, you can obscure the
sudden departure of some of the captives.

Beta Rabbits statisticians have asked you for some numerical analysis of how
this could be done so that they can explore the best options.

Luckily, every rabbit has a slightly different height, and the guards are lazy
and few in number. Only one guard is stationed at each end of the rabbit
line-up as they survey their captive population.

With a bit of misinformation added to the facility roster, you can make the
guards think there are different numbers of rabbits in holding.

To help plan this caper you need to calculate how many ways the rabbits can be
lined up such that a viewer on one end sees x rabbits, and a viewer on the other
end sees y rabbits, because some taller rabbits block the view of the shorter
ones.

For example, if the rabbits were arranged in line with heights 30 cm, 10 cm,
50 cm, 40 cm, and then 20 cm,a guard looking from the left would see 2 rabbits
while a guard looking from the right side would see 3 rabbits.

Write a method answer(x,y,n) which returns the number of possible ways to
arrange n rabbits of unique heights along an east to west line, so that only x
are visible from the west, and only y are visible from the east. The return
value must be a string representing the number in base 10.

If there is no possible arrangement, return "0".

The number of rabbits (n) will be as small as 3 or as large as 40
The viewable rabbits from either side (x and y) will be as small as 1 and as
large as the total number of rabbits (n).
"""

import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r) if n > 0 else 1

def answer(x,y,n):
    #try:
        x,y = (max(x,y), min(x,y))
        
        if y < -1: return 0
        
        # special case 1: If both guards see only one bunny even though there is more than one bunny
        if x == 1 and y == 1: return 1 if n == 1 else 0
        # special case 2: If one guards sees all bunnies and the other sees more than one
        if x == n and y > 1: return 0
        # special case 3: If one guard sees all bunnies and the other guard sees one bunny
        if x == n and y == 1: return 1
        if y == 1: return answer(x-1,0,n-1)
        # special case 4: Hit 0 bunnies on one side, bunnies can be in any permutation
        if x == 1 and y == 0: return math.factorial(n-1)
        if x == 0 and y == 0: return 1

        solutions = 0

        for i in range(x, n-y+2 if y > 0 else n - y + 1):
            nr_left = (i - 1)
            nr_right = (n - i)
            solutions += nCr(nr_left+nr_right, nr_left) * answer(x-1,0,nr_left) * answer(0,max(0,y-1),nr_right)
            #print(nr_left * "." + "|" + nr_right * "." + "calling answer({},{},{})".format(0,max(y-1,0),nr_right))
            
        return solutions
        
def views(x,n):
    #print"Called views({},{})".format(x,n),
    # Given n bunnies, how many arrangements can we make such that only x bunnies are seen from the front?
    
    if x == n:
        #print"Returning views({},{})={}".format(x,n, 1)
        return 1
    elif x == 1:
        return math.factorial(n-1)
    elif x == 0:
        #print"Returning views({},{})={}".format(x,n, 1)
        return 1

    solutions = 0
    limit = x
    for i in range(limit, n + 1):
        #print "views({},{})={}".format(x,n, solutions)
        nr_left = (i - 1)
        nr_right = (n - i)
        print(nr_left * "." + "|" + nr_right * ".")
        #solutions += views(x-1, nr_left) * math.factorial(nr_right)
    print("Returning views({},{})={}".format(x,n, solutions))
    return solutions
