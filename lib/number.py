#!/usr/bin/python 

""" README 
Author: Ken Wu

This is a library file regarding to all number operations

"""


"""	
	ensure_front_leading_zeros
		n:			Input number
		min_width:	Min width of the output from the input number

		E.g. if input is 9 as n and 2 as min_width, then the output is 09 (with zero appened in front to make it width 2)
"""
def ensure_front_leading_zeros(n, min_width):
	w = 10 ** (min_width - 1)
	r = n / w
	if r < 1:
		return "0" + str(n)
	else:
		return "" + str(n)	

