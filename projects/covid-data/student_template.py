class CovidRecord:
    """
    A simple class to hold record data from NYT database
    """

    def __init__(self, _date='', _county='', _state='', _fips=0, _cases=0, _death=0):
        """
        Default constructor for transforming each line of the file into data point

        :param _date: Date covid case was recorded
        :param _county: County in which data was recorded
        :param _state: State in which data was recorded
        :param _fips: Federal Information Processing Standards code
        :param _cases: Number of total cases recorded
        :param _death: Number of total deaths recorded
        """
        self.date = _date
        self.county = _county
        self.state = _state

        if _fips == '':
            self.fips = 0
        else:
            self.fips = int(_fips)
        self.cases = int(_cases)

        if _death == '':
            self.death = 0
        else:
            self.death = int(_death)


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of points
    :param file_path: Path to data file
    :return: List of CovidRecord points
    """
    # data point list
    covid_data = list()

    # open the NYT file path
    fin = open(file_path)

    # get rid of the headers
    fin.readline()

    done = False

    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        elements = line.strip().split(",")

        new_point = CovidRecord((elements[0]), (elements[1]), (elements[2]),
                                (elements[3]), (elements[4]), (elements[5]))

        # to reduce file sizes, only grab Virginia points
        if new_point.state == 'Virginia':
            covid_data.append(new_point)

    return covid_data


if __name__ == "__main__":
    # load covid data as list of CovidRecord objects
    data = parse_nyt_data('us-counties.csv')

    # each element in list data is a CovidRecord object. Each of which contains
    # date, county, state, fips, cases, and deaths

    # for example, we can print out the data for the first point in the US counties file
    #point = data[0]

    #print("Data: ", point.date, " County: ", point.county, " State: ", point.state,
     #     " FIPS: ", point.fips, " Cases: ", point.cases, " Deaths: ", point.death)

    # write code to address the following question:
    # When was the first positive COVID case in Rockingham County? When was the first in Harrisonburg?

# Placeholder lists for the dates corresponding to each Rockingham and Harrisonburg data point
rham_dates = []
hburg_dates = []

# Iterating through entire length of list "data" and temporarily storing each index
for i in range(len(data)):
    point1 = data[i]

    # Finding the first occurrence of "Rockingham" and storing the date
    if point1.county == 'Rockingham':
        rham_dates.append(point1.date)
        break

# Iterating through entire length of list "data" and temporarily storing each index
for i in range(len(data)):
    point1 = data[i]

    # Finding the first occurrence of "Harrisonburg city" and storing the date
    if point1.county == 'Harrisonburg city':
        hburg_dates.append(point1.date)
        break

    # Printing out the entry in the Rockingham and Harrisonburg data lists, which will inherently be the data on
    # which the first case was recorded
print(f'The first positive COVID case in Rockingham County was on {rham_dates[0]}.')
print(f'The first positive COVID case in Harrisonburg City was on {hburg_dates[0]}.')

    # write code to address the following question:
    # What day was the greatest number of new daily cases recorded in Harrisonburg? When was the greatest day in Rockingham County?

    # write code to address the following question:
    # What was the worst seven day period in either the city and county for new COVID cases? This is the 7-day period where the number of new cases was maximal.


