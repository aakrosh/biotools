#!/usr/bin/env python

from collections import Counter

import numpy as np

def construct_bwt(string):
    """
    length(T) = n
    Computational cost: O(n logn)
    Storage cost: n*n
    """
    T = string + "$"
    rotations = [(T[i:] + T[:i]) for i in xrange(0, len(T))]
    rotations.sort()
    return [x[-1] for x in rotations]

def construct_bwt_via_sa(string):
    """
    length(T) = n
    Computational cost: O(n logn)
    Storage cost: n*(n-1)/2
    """
    T = string + "$"
    suffixes = [(T[i:],i) for i in xrange(0,len(T))]
    suffixes.sort()
    return [T[y-1] for x,y in suffixes]

def apply_inverse_bwt(bwl):
    array = []
    counter = Counter()
    first = sorted(bwl)

    for i in xrange(0, len(bwl)):
        row = []
        row.append(first[i])
        row.append(bwl[i])
        row.append(counter[bwl[i]])
        counter[bwl[i]] += 1
        array.append(row)

    for 

    print array

if __name__ == "__main__":
    teststring = "abaaba"
    teststring = "tomorrow and tomorrow and tomorrow"
    teststring = "banana"

    bwl = construct_bwt(teststring)
    print "".join(bwl)

    bwl = construct_bwt_via_sa(teststring)
    print "".join(bwl)

    apply_inverse_bwt(bwl)
