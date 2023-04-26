from tspdb import Attraction, TSPDatabase
import numpy as np
import json


# Create database
db = TSPDatabase()

# Create a list of all distances
all_distance_values = []
first_idx = np.arange(0,40)
second_idx = np.arange(0,40)

with open('distances.json') as file:
    distances = json.load(file)
    for i in first_idx:
        for j in second_idx:
            if i == j:
                continue
            all_distance_values.append(distances[str(i) + ',' + str(j)])

# Make Numpy Array for ALL distances
all_distances = np.diag(np.zeros(40))
for y in range(0, 40):
    for x in range(0, 40):
        if x == y:
            all_distances[x][y] = 0
        else:
            all_distances[x][y] = db.get_attraction_distance(id1=x, id2=y)

# Toggle for while loop
toggle = True

while toggle:
    # User chooses starting location (works with apostrophes)
    first_attr_name = None
    name_to_add = input('Enter a part of or the entire name of the desired starting attraction: ')
    stripped_string = ''.join(name_to_add.lower().strip().split("'"))

    # Makes lists of attraction names
    attr_name_list = [attr.get_attraction_name() for attr in db.get_attractions_list()]
    attr_name_list_lower = [attr.get_attraction_name().lower() for attr in db.get_attractions_list()]

    # Counter for how many attractions include the user-entered string
    attr_counter = 0
    searched_attr_list = []

    # Check if entered name is an attraction
    for attr_name in attr_name_list_lower:
        if stripped_string in attr_name:
            first_attr_name = attr_name
            attr_counter += 1
            searched_attr_list.append(attr_name.title())

    # Check if attraction is valid
    if attr_counter == 1:
        toggle = False
    elif first_attr_name is None:
        print(f'\nERROR: Invalid attraction name. Either the entered name includes unsupported punctuation, \
is misspelled, or there is no attraction associated with the entered name.\n\nEnter a part of or the entire \
name of one of the following attraction names:\n{attr_name_list}\n')
        continue
    else:
        print(f'\nERROR: Multiple attractions found with the name "{stripped_string}".\
\n\nDid you mean one of these?:\n{searched_attr_list}\n')
        continue

# Choose next attraction purely by distance
