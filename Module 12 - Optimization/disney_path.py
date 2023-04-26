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

# User chooses starting location (I don't think this will work if the user inputs an apostrophe or period or anything of the sorts
first_attr_name = None
name_to_add = input('Enter a part of or the entire name of the desired starting attraction: ')

# Makes lists of attraction names
attr_name_list = [attr.get_attraction_name() for attr in db.get_attractions_list()]
attr_name_list_lower = [attr.get_attraction_name().lower() for attr in db.get_attractions_list()]

# Counter for how many attractions include the user-entered string
attr_counter = 0
searched_attr_list = []

# Check if entered name is an attraction
for attr_name in attr_name_list_lower:
    if name_to_add.lower() in attr_name:
        first_attr_name = attr_name
        attr_counter += 1
        searched_attr_list.append(attr_name.title())

# Check if attraction is valid
if first_attr_name is None:
    print(f'\nERROR: Invalid attraction name. Enter one of the following attraction names:\n{attr_name_list}')
    exit(1)
elif attr_counter != 1:
    print(f'\nERROR: Multiple attractions found with the entered name.\
    Did you mean one of these attractions?:\n{searched_attr_list}')
    exit(1)

# Choose next attraction purely by distance
