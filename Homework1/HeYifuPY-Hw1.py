#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:26:02 2020

@author: yifuhe
"""

from math import *
import numpy as np

# question 1
def dayOfWeek(m, d, y):
    N = d + 2*m + floor(3*(m+1)/5) + y + floor(y/4) - floor(y/100) + floor(y/400) + 2
    return N % 7

# question 2
def kthDigit(x, k):
    if not (isinstance(x,int) and isinstance(k,int)):
        return "unknown"
    if k < 0:
        return "unknown"
    if k >= len(str(x)):
        return 0
    else:
        return int(str(x)[::-1][k])
        
# question 3
def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False

# quesstion 4
def isEvenPositiveInt(num):
    if num > 0:
        if num % 2 == 0:
            return True
    return False
# question 5
def isPerfectCube(num):
    temp = abs(num)
    if int(np.cbrt(temp)) ** 3 == temp:
        return True
    return False

# question 6
def f(num):
    return num**2 - num

# question 7
def g(num):
    return 3* num**2 - 4.5*num

# question 8
def h(num):
    return sin(num)+cos(num)

# question 9
def bisection(f,low,hi,tol):
    while(hi - low >= tol):
        temp = (hi + low)/2
        if f(temp)*f(hi) < 0:
            low = temp
        else:
            hi = temp
    return temp

    
# question 10
def harmonicNumber(n):
    if n == 0:
        return 0
    else:
        res = 0
        for i in range(1,n+1):
            res += 1/i
    return res



print("Test hw 1...")
assert (isEven(246810) == True)
assert (isEven(19) == False)

assert (isEvenPositiveInt(231) == False) 
assert (isEvenPositiveInt(400) == True)

assert (dayOfWeek(4,1,2020) == 4)
assert (dayOfWeek(3,26,2015) == 5)

assert (kthDigit (1234,3) == 1) 
assert (kthDigit (-1234, 3) == 1) 
assert (kthDigit (12, 0) == 2)
assert (kthDigit (123456, 10) == 0)
assert (kthDigit (123456, 8.5) == 'unknown')
assert (kthDigit (123456, -8) == 'unknown')
assert (kthDigit (123.456, 10) == 'unknown')
assert (kthDigit ('hello', 10) == 'unknown')

assert (isPerfectCube(27) == True)
assert (isPerfectCube(16) == False)
assert (isPerfectCube(-729) == True)

assert (f(3) == 6)
assert (f(4.5) == 15.75)
assert (f(-21) == 462)
assert (f(3) == 6)
assert (f(1) == 0.)

assert (g(1) == -1.5)
assert(g(3) == 13.5)
assert(g(1.5) == 0)



assert (isclose(g(3.2), 16.32, abs_tol=1e-6))
assert (isclose(h(0), 1.0, abs_tol=1e-6))


assert (isclose(bisection (f, 0.1, 10.0, 0.00000001), 1.0, abs_tol=1e-6))
assert (isclose(bisection (g, 0.01, 10.0, 0.00000001), 1.5, abs_tol=1e-6)) 
assert(isclose(bisection (h, 1.01, 3.02, 0.00000001), (3 * pi/4), abs_tol=0.00000001)) 
assert(isclose (bisection (h, 6.0, 10.0, 0.00000001), (11 * pi/4), abs_tol=1e-6)) 

assert(isclose (harmonicNumber (0),0.0, abs_tol=1e-6))
assert(isclose (harmonicNumber (1),1/1.0,abs_tol=1e-6 ))
assert(isclose (harmonicNumber (2),1/1.0 + 1/2.0, abs_tol=1e-6 ))
assert(isclose (harmonicNumber (3),1/1.0 + 1/2.0 + 1/3.0, abs_tol=1e-6))

print ("Pass all tests")