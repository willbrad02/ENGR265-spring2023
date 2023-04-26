"""Find the optimum path through Disney World's Magic Kingdom based on distance between all attractions.

Authors: Will Bradford with help from Zach Kreitzer
Version: 4-26-23

Assumptions: A .json file of all point-of-interest (POI) names and a .json file of distances between all
             POIs, as the crow flies, are given.
"""
from tspdb import Attraction, TSPDatabase
import numpy as np
import json


if __name__ == "__main__":

    # Instantiate database
    db = TSPDatabase()

    # Create a list of all distances
    first_idx = np.arange(0, 40)
    second_idx = np.arange(0, 40)

    with open('distances.json') as file:
        distances = json.load(file)
        all_distance_values = [distances[f'{i},{j}'] for i in first_idx for j in second_idx if i != j]

    # Make numpy array for all distances
    all_distances = np.diag(np.zeros(40))
    for y in range(0, 40):
        for x in range(0, 40):

            if x == y:
                all_distances[x][y] = 0

            else:
                all_distances[x][y] = db.get_attraction_distance(id1=x, id2=y)

    # Toggle variable for while loop
    toggle = True

    while toggle:

        # User chooses starting attraction (program ignores apostrophes, leading/trailing whitespace, and
        # capitalization, but end-of-line punctuation should not be passed)
        first_attr_name = None
        name_to_search = input('Enter either a part or the entire name of the desired starting attraction: ')
        stripped_string = ''.join(name_to_search.lower().strip().split("'"))

        # Make lists of attraction names
        attr_name_list = [attr.get_attraction_name() for attr in db.get_attractions_list()]
        attr_name_list_lower = [attr.get_attraction_name().lower() for attr in db.get_attractions_list()]

        # List storing all attraction names that match/include the entered string
        searched_attr_list = [attr_name.title() for attr_name in attr_name_list_lower if stripped_string in attr_name]

        # If at least one attraction is found, update the name of the first visited attraction
        if searched_attr_list:
            first_attr_name = searched_attr_list[0]

        # Check if attraction is valid
        if len(searched_attr_list) == 1:
            toggle = False

        elif first_attr_name is None:
            print(f'''
ERROR: Invalid attraction name. Either the entered name includes unsupported punctuation, is misspelled, or there is \
no attraction associated with the entered name.
    
Enter either a part or the entire name of one of the following attraction names:
{attr_name_list}
''')

        else:
            print(f'''
ERROR: Multiple attractions found that include "{stripped_string}".

Did you mean one of these?:
{searched_attr_list}
''')

    # Choose next attraction purely by distance
