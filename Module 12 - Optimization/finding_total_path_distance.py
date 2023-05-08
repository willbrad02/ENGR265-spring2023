from disney_tsp_final import attr_pixel_distances, plot_fastest_route

def find_total_distance(path_list,distance_array):
    '''
    Function which takes a list of points and a symmetrical distance array between points and
    finds total distance of the path taken

    :param path_list: list of integers which is the series of destinations through the park
    :param distance_array: symmetrical array of distances between each point and every other point
    :return: single total distance value between all points
    '''

    #create list to hold each distance
    distance_list = []

    #create variable to store previous point
    point = -1

    for i in path_list:
        if point != -1:

            #find distance between points
            distance = attr_pixel_distances[i,point]

            #multiplied by factor which converts pixel distance to feet
            distance_list.append(distance * 2.272)

        #update previous point
        point = i

    #find total distance
    total_distance = sum(distance_list)



    print('The total distance walked would be',int(total_distance),'feet')


path = [36, 33, 3, 1, 16, 32, 23, 38, 13, 2, 5, 6, 7, 8, 9, 10, 11, 0, 19, 39, 12, 14, 17, 20, 22, 25, 27, 28, 29, 31, 37, 4, 26, 34, 18, 24, 30, 35, 15, 21]
find_total_distance(path, attr_pixel_distances)




