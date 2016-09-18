"""
Carrotland
==========
 
The rabbits are free at last, free from that horrible zombie science experiment.
They need a happy, safe home, where they can recover.
 
You have a dream, a dream of carrots, lots of carrots, planted in neat rows and
columns! But first, you need some land. And the only person who's selling land
is Farmer Frida. Unfortunately, not only does she have only one plot of land,
she also doesn't know how big it is - only that it is a triangle. However, she
can tell you the location of the three vertices, which lie on the 2-D plane and
have integer coordinates.
 
Of course, you want to plant as many carrots as you can. But you also want to
follow these guidelines: The carrots may only be planted at points with integer
coordinates on the 2-D plane. They must lie within the plot of land and not on
the boundaries. For example, if the vertices were (-1,-1), (1,0) and (0,1), then
you can plant only one carrot at (0,0).
 
Write a function answer(vertices), which, when given a list of three vertices,
returns the maximum number of carrots you can plant.
 
The vertices list will contain exactly three elements, and each element will be
a list of two integers representing the x and y coordinates of a vertex. All
coordinates will have absolute value no greater than 1000000000. The three
vertices will not be collinear.
"""

from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def answer(vertices):
    # The solution can be quickly found using Pick's theorem. But first we need two
    # values: the area of the triangle and the integer boundary points .

    # shoelace formula
    area = 0.5 * abs((vertices[0][0] - vertices[2][0]) * (vertices[1][1] - vertices[0][1]) - (vertices[0][0] - vertices[1][0]) * (vertices[2][1] - vertices[0][1]))

    # basic algebra to calculate integer boundary points
    bound_points = 3
    for v in range(3):
        # If we can find the first weight w > 0 such that for two coordinates we have that
        # w * x_1 + (1-w)*x_2 is integer and w * y_1 + (1-w)*y_2 is integer,
        # then it means that the linear combination of the two coordinates with that
        # weight is an integer boundary point. And since the function and the grid
        # are both linear, there could be if 2 * w < 1 and 3 * w < 1 etc.

        delta_w_x = Fraction(1,abs(vertices[v - 1][0] - vertices[v][0])) if vertices[v - 1][0] != vertices[v][0] else 0
        delta_w_y = Fraction(1,abs(vertices[v - 1][1] - vertices[v][1])) if vertices[v - 1][1] != vertices[v][1] else 0

        if min(delta_w_x, delta_w_y) == 0 and max(delta_w_x, delta_w_y) > 0:
            bound_points += max(delta_w_x, delta_w_y).denominator - 1
        else:
            lcm_denominator = lcm(delta_w_y.denominator, delta_w_x.denominator)
            lcm_numerator = int(lcm(delta_w_x.numerator * (lcm_denominator / delta_w_x.denominator), (lcm_denominator / delta_w_y.denominator) * delta_w_y.numerator))
            integer_phase = Fraction(lcm_numerator, lcm_denominator)
            bound_points += integer_phase.denominator - 1

    # Pick's theorem
    return int(area - bound_points / 2.0 + 1)
