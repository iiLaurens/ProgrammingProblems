"""
Undercover underground
======================

As you help the rabbits establish more and more resistance groups to fight
against Professor Boolean, you need a way to pass messages back and forth.

Luckily there are abandoned tunnels between the warrens of the rabbits,
and you need to find the best way to use them.

In some cases, Beta Rabbit wants a high level of interconnectedness,
especially when the groups show their loyalty and worthiness.

In other scenarios the groups should be less intertwined,
in case any are compromised by enemy agents or zombits.

Every warren must be connected to every other warren somehow,
and no two warrens should ever have more than one tunnel between them.
Your assignment: count the number of ways to connect the resistance warrens.

For example, with 3 warrens (denoted A, B, C) and 2 tunnels, there are three
distinct ways to connect them:

A-B-C
A-C-B
C-A-B

With 4 warrens and 6 tunnels, the only way to connect them is to connect
each warren to every other warren.

Write a function answer(N, K) which returns the number of ways to connect
N distinctly labelled warrens with exactly K tunnels, so that there is a
path between any two warrens.

The return value must be a string representation of the total number of
ways to do so, in base 10. N will be at least 2 and at most 20.
K will be at least one less than N and at most (N * (N - 1)) / 2
"""

import math

def memoize(f):
    """ Memoization decorator for a function taking one or more arguments. """
    class memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return memodict().__getitem__


def nCr(n, r):
    f = math.factorial
    return f(n) / (f(r) * f(n - r)) if n > 0 else 1


def min_edges(n):
    return n - 1


def max_edges(n):
    return n * (n - 1) / 2

@memoize
def answer(n, k):
    n, k = (int(n), int(k))

    if k < min_edges(n) or k > max_edges(n): return str(0)

    # The number of spanning trees in a labeled graph (Cayley's formula)
    if k == min_edges(n): return str(n**(n - 2))

    # We have a complete graph, of which only one is possible
    if k == max_edges(n): return str(1)

    # If you take a complete graph and remove all n-1 adjacent edges from a
    # single vertex, then the vertex is disconnected from the rest of the graph.
    # So if you remove less than n-1 edges from a complete graph then it is
    # impossible to have disjoint subgraphs. Hence any choice of edges is a
    # valid solution. There is (max_edges choose k) such graphs.
    if k > max_edges(n) - (n - 1): return str(int(nCr(max_edges(n), k)))

    # If none of the above works, we resort to counting techniques. Without
    # restrictions, it is possible to have (max_edges choose k) different graphs.
    # However, some of those graphs are invalid and need to be subtracted. A graph
    # in this problem is invalid if it is possible to divide the vertices in two
    # mutually exlusive subsets such that no edge in the graph connects the two
    # subsets. To be able to count the possibilities systematically without double
    # counting, I will assume that one subset is already a valid solution to a
    # smaller undercover_underground problem. This has the nice property that this
    # subset itself cannot be divided again in two subsubsets due to it being a
    # connected graph and thus provides a convenient way to define how to divide all
    # vertices into two subsets given any random graph.
    solutions = nCr(max_edges(n), k)

    # To count all invalid graphs, first divide the n vertices into two subsets, one
    # will contain i vertices and the other will contain the remaining n-i. Let i
    # loop from 1 up to and including floor(n/2) to prevent double counting.
    for i in xrange(1, n / 2 + 1):
        # Next, divide the k edges over either subset. Exhausting all edges within
        # both groups prevents any remaining edge from being able bridge the two
        # groups of vertices.
        for j in xrange(0, k + 1):
            # Now make sure that not too few or too many edges are assigned to either
            # group. Remember that one group must be a solution to the problem itself
            # and thus has a minimum and maximum number of edges it can take. The other
            # unconnected subset has no such restriction except for the maximum edges
            # it can receive.
            if j <= max_edges(n - i) and j >= min_edges(n - i) and k - j <= max_edges(i):
                # Substract the invalid solutions.
                solutions -= nCr(n, i) * int(answer(n - i, j)) * nCr(max_edges(i), k - j)
    return str(int(solutions))
