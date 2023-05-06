import itertools
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit
from pytsp.utils import minimal_spanning_tree
import numpy as np
from tspdb import TSPDatabase
from colorama import Fore


def run_christofides_algorithm(graph, starting_node=0):
    """
    Christofides TSP algorithm
    http://www.dtic.mil/dtic/tr/fulltext/u2/a025602.pdf
    Args:
        graph: 2d numpy array matrix
        starting_node: of the TSP
    Returns:
        tour given by christofides TSP algorithm

    Examples:
        #>>> import numpy as np
        #>>> graph = np.array([[  0, 300, 250, 190, 230],
        #>>>                   [300,   0, 230, 330, 150],
        #>>>                   [250, 230,   0, 240, 120],
        #>>>                   [190, 330, 240,   0, 220],
        #>>>                   [230, 150, 120, 220,   0]])
        #>>> christofides_tsp(graph)
    """

    # Minimal spanning tree (Connect all nodes to at least one other, based on distance)
    mst = minimal_spanning_tree(graph, 'Prim', starting_node=0)

    # Save nodes that have an odd number of connections
    odd_degree_nodes = list(_get_odd_degree_vertices(mst))
    odd_degree_nodes_ix = np.ix_(odd_degree_nodes, odd_degree_nodes)
    nx_graph = nx.from_numpy_array(-1 * graph[odd_degree_nodes_ix])

    # Minimal-weight perfect matching
    # (Create edges by matching all nodes to each other; edges have no common nodes)
    matching = max_weight_matching(nx_graph, maxcardinality=True)

    # Unite minimal-weight perfect matching and minimal spanning tree to create a graph where all nodes have an even
    # number of connections (graph does not loop back on itself)
    euler_multigraph = nx.MultiGraph(mst)
    for edge in matching:
        euler_multigraph.add_edge(odd_degree_nodes[edge[0]], odd_degree_nodes[edge[1]],
                                  weight=graph[odd_degree_nodes[edge[0]]][odd_degree_nodes[edge[1]]])

    # Create an initial path along the previously created shape; nodes may appear more than once
    euler_tour = list(eulerian_circuit(euler_multigraph, source=starting_node))
    path = list(itertools.chain.from_iterable(euler_tour))

    # Eliminate duplicate nodes in the path
    final_path = _remove_repeated_vertices(path, starting_node)[:-1]

    return final_path


def _get_odd_degree_vertices(graph):
    """
    Finds all the odd degree vertices in graph

    :param graph: 2D numpy array as adj. matrix
    :return: Set of vertices that have odd degree
    """
    odd_degree_vertices = {index for index, row in enumerate(graph) if len(np.nonzero(row)[0]) % 2 != 0}

    return odd_degree_vertices


def _remove_repeated_vertices(path, starting_node):
    path = list(dict.fromkeys(path).keys())
    path.append(starting_node)
    return path


if __name__ == "__main__":

    # Instantiate database
    db = TSPDatabase()

    # Make lists of attraction names
    attr_name_list = [attr.get_attraction_name() for attr in db.get_attractions_list()]
    attr_name_list_lower = [attr.get_attraction_name().lower() for attr in db.get_attractions_list()]

    # Toggle variable for while loop
    toggle = True
    print_counter = 0

    while toggle:

        first_attr_name = None

        # Print IDs and names for user to choose from
        if print_counter == 0:

            print(Fore.LIGHTBLUE_EX + 'ID: Name' + Fore.RESET)
            for attr in db.get_attractions_list():
                print(f'{attr.id:02d}: {attr.get_attraction_name()}')

            # Only print on first loop
            print_counter +=1

        # User chooses starting attraction (program ignores apostrophes, leading/trailing whitespace, and
        # capitalization, but end-of-line punctuation should not be passed)
        name_to_search = input(Fore.RESET + '\nEnter one of the above attraction IDs or at least a portion '
                               'of the attraction\'s name that you would like to start at. '
                               'Press ENTER to start at the front of the park.:\n')
        stripped_input = ''.join(name_to_search.lower().strip().split("'"))

        # List storing all attraction names that match/include the entered string
        searched_attr_list = [attr_name.title() for attr_name in attr_name_list_lower if stripped_input in attr_name]

        # Choose starting location from inputted id, must be valid id
        if stripped_input.isdigit() and 0 <= int(stripped_input) <= 39:
            first_attr_name = db.get_attraction_name_by_id(int(stripped_input))
            toggle = False

        # Start at front of park
        elif stripped_input == '':
            first_attr_name = db.get_attraction_name_by_id(36)
            toggle = False

        # Check number of attractions associated with input
        elif len(searched_attr_list) == 1:
            first_attr_name = searched_attr_list[0]
            toggle = False

        # Multiple attractions associated with input
        elif len(searched_attr_list) > 1:
            print(Fore.LIGHTRED_EX + f'\nERROR: Multiple attractions found that include "{stripped_input}".'
                                     f'\n{Fore.RESET}Did you mean one of these?:\n{searched_attr_list}\n')

        # Input is invalid
        else:
            # If input is an id
            if stripped_input.strip('-.').isnumeric() or \
                    (''.join(stripped_input.lower().strip('-').split(".")).isnumeric() and '.' in stripped_input):
                print(Fore.LIGHTRED_EX + '\nERROR: Invalid attraction ID. Valid IDs are integers from 0-39.\n')

            # If input is a name
            else:
                print(Fore.LIGHTRED_EX + '\nERROR: Invalid attraction name. Either the entered name includes '
                                         'unsupported punctuation, is misspelled, or there is no '
                                         'attraction associated with the entered name.\n')

    # Get first attraction and id
    first_attr = db.get_attraction_by_name(first_attr_name)
    first_attr_id = first_attr.id

    # Pixel coordinates of each attraction: (x, y)
    attraction_coordinates = [80.43, 667.25,
                              1001.09, 656.34,
                              120.65, 415.39,
                              927.18, 680.33,
                              1033.70, 221.32,
                              252.17, 593.106,
                              988.05, 288.9,
                              706.52, 234.4,
                              766.3, 430.7,
                              379.35, 344.53,
                              508.69, 288.9,
                              297.83, 739.2,
                              395.65, 451.37,
                              859.79, 373.96,
                              881.52, 207.15,
                              603.26, 379.41,
                              865.22, 648.7,
                              532.61, 331.44,
                              976.1, 139.55,
                              176.09, 717.40,
                              663.698, 361.97,
                              690.22, 375.05,
                              770.65, 305.28,
                              1133.699, 587.66,
                              58.695, 482.99,
                              384.78, 654.16,
                              1075, 243.13,
                              469.57, 476.45,
                              291.31, 672.697,
                              781.52, 359.79,
                              159.78, 466.64,
                              936.96, 481.899,
                              977.177, 666.15,
                              701.09, 955.08,
                              1084.79, 165.72,
                              27.174, 443.74,
                              641.31, 1011.77,
                              843.481, 189.71,
                              989.13, 722.85,
                              254.35,  698.86]

    # Split pixel coordinates into x and y
    x_coordinates, y_coordinates = [], []

    for i in attraction_coordinates:
        if len(x_coordinates) <= len(y_coordinates):
            x_coordinates.append(i)
        else:
            y_coordinates.append(i)

    # Create symmetric array of attraction pixel distances
    all_pixel_distances = np.diag(np.zeros(40))

    for y in range(0, 40):
        for x in range(0, 40):

            if x == y:
                all_pixel_distances[x][y] = 0

            else:
                all_pixel_distances[x][y] = (
                    np.sqrt((x_coordinates[x] - x_coordinates[y]) ** 2 + (y_coordinates[x] - y_coordinates[y]) ** 2))

    # Run christofides algorithm (guaranteed to be no longer than 3/2 of the optimal path)
    recommended_path = run_christofides_algorithm(all_pixel_distances, first_attr_id)

    print(f'\nIt is recommended that you visit attractions in the following order:\n{recommended_path}')
