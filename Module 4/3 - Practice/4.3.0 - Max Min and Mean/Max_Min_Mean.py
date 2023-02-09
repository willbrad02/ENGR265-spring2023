# In this assignment you will be tasked with finding the maximum and
# minimum values of a list, as well as its average.

# Here is the list in question:
list_one = [4, 58, 55, 94, 11, 89, 69, 12, 97, 2, 38, 20, 25, 6, 95, 89, 11, 89, 19, 85, 44, 28, 6, 86, 96, 21,
            11, 84, 52, 9, 19, 11, 57, 35, 76, 74, 46, 3, 72, 99, 15, 27, 40, 98, 53, 94, 21, 44, 112, 92]

# Here are the variables to store your answers in:
list_max = -1
list_min = -1
list_average = -1

# To find each value you will need to have a new For Loop,
# and use a few If Statements as well. No max() or min() functions
# allowed though, that'd be too easy.


# First Loop Here:
temp_min = list_one[0]

for num in list_one:
    if num < temp_min:
        temp_min = num
        list_min = num
    else:
        continue
print(f'The minimum value is {list_min}')

# Second Loop Here:
temp_max = list_one[0]

for num in list_one:
    if num > temp_max:
        temp_max = num
        list_max = num
    else:
        continue
print(f'The maximum value is {list_max}')

# Third Loop Here:
temp_total = 0
for num in list_one:
    temp_total += num
    temp_avg = temp_total / len(list_one)
    list_average = temp_avg
print(f'The average value is {list_average}')















