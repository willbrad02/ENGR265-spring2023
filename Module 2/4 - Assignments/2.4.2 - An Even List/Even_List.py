import random

"""
THIS SECTION IS DR. FORSYTH'S CODE. DO NOT MODIFY. BUT KEEP READING.
"""

# randomly sample a distribution between 2 and 6
random_number = int(random.uniform(2, 6))

# any number times 2 is even
an_odd_number = 2 * random_number

# generate a random list of odd length containing values up to 100
even_list = random.sample(range(100), an_odd_number)

# print out the list contents
print("Your list is: ", even_list)

"""
YOUR CODE BEGINS BELOW HERE. FILL IN THE MISSING OPERATIONS / CODE
"""
import math as m
length = len(even_list)

middle_left_index = (length // 2) - 1
middle_right_index = m.ceil(length / 2)

element1 = even_list[middle_left_index]
element2 = even_list[middle_right_index]

# this is the final result. Modify this line, and the empty lines above, to solve the assignment
middle_average = (element1 + element2) / 2

# the average of middle elements is
print("The average is: ", middle_average)
