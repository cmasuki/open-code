# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:06:35 2019

This program has been written to run the fizzbuzz game.
It is designed for learning Python and for experimenting with Github.
CMAS-open-code project

@author: StewartC
"""

# This loop finds all the numbers which divide by 3 or 5

for a in range (1, 100):
    if ((a%3 > 0) and (a%5 > 0)):    
        print a

    if ((a%3 == 0) and (a%5 > 0)):
        print "Fizz"

    if ((a%3 > 0) and (a%5 == 0)):
        print "Buzz"
    
    if ((a%3 == 0) and (a%5 == 0)):
        print "Fizz Buzz"    
        

