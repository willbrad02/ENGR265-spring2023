"""Find the optimum path through Disney World's Magic Kingdom based on distance between all attractions.

Authors: Will Bradford with help from Zach Kreitzer
Version: 4-30-23

Assumptions: A .json file of all point-of-interest (POI) names and a .json file of distances between all
             POIs, as the crow flies, are given.
"""
from tspdb import TSPDatabase
import numpy as np
import json


# Find the closest attraction that has not already been visited
def get_next_attraction_id(curr_attr, distances_array):

    # Only look at column of current attraction's id
    distances_array_working = distances_array[:, curr_attr.id]

    # Dictionary to store all non-visited id's and their non-zero distances to the current attraction
    distance_dict = {}

    # Iterating through distances
    for dist in distances_array_working:

        # Ignoring distances of 0, creating a list that holds the id values of the dist value
        if dist > 0:
            dist_idx = np.copy(np.where(distances_array_working == dist))
            dist_idx = [num for num in dist_idx[0]]

            # Looping if there are multiple id's that are equidistant from current attraction
            for i in range(len(dist_idx)):

                # Add distance to list if the id has not been visited
                if dist_idx[i] not in path_list_id:
                    distance_dict[dist_idx[i]] = dist

    # Return None if no ID's left
    if not distance_dict:
        return None

    # Store the minimum distance
    min_dist = min(distance_dict.values())
    min_distance_id = [key for key, val in distance_dict.items() if val == min_dist]

    # If multiple, choose the smallest ID
    next_id = min_distance_id[0]

    return next_id


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

    # Get first attraction
    current_attr = db.get_attraction_by_name(first_attr_name)

    # Create path to follow
    path_list_id = [current_attr.id]

    # Loop through, accounting for the fact that 1 attraction has already been chosen
    for i in range(len(db.attractions) - 1):
        next_attr_id = get_next_attraction_id(current_attr, all_distances)

        # Just in case function is called when no ID's remain
        if next_attr_id is None:
            print('ERROR: Function "get_next_attraction_id()" was called after all IDs have been accounted for')
            quit()

        # Track attraction ID's
        path_list_id.append(next_attr_id)

        # Update current attraction
        current_attr = db.get_attraction_by_id(next_attr_id)

    # Multiple versions of the path for better readability
    path_list_names = [db.get_attraction_name_by_id(num) for num in path_list_id]
    path_list_attractions = [db.get_attraction_by_id(num) for num in path_list_id]

    print(f'It is recommended that you visit attractions in the following order:\n{path_list_id}')
