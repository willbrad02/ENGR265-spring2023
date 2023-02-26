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
    '''point = data[0]

    print("Data: ", point.date, " County: ", point.county, " State: ", point.state,
          " FIPS: ", point.fips, " Cases: ", point.cases, " Deaths: ", point.death)
'''
    # write code to address the following question:
    # When was the first positive COVID case in Rockingham County? When was the first in Harrisonburg?

# Placeholder lists for all Rockingham and Harrisonburg data
rham_data = []
hburg_data = []

# Iterating through entire length of list "data" and temporarily storing each index
for i in range(len(data)):
    point1 = data[i]

    # Finding each occurrence of "Rockingham" and storing the associated data
    if point1.county == 'Rockingham':
        rham_data.append(point1)

    # Finding each occurrence of "Harrisonburg city" and storing the associated data
    elif point1.county == 'Harrisonburg city':
        hburg_data.append(point1)

# Storing the first data point of Rockingham and also the date associated
rham_first_point = rham_data[0]
rham_first_case_date = rham_first_point.date

# Storing the first data point of Harrisonburg and also the date associated
hburg_first_point = hburg_data[0]
hburg_first_case_date = hburg_first_point.date

# Printing out the date for the first recorded COVID cases in Rockingham and Harrisonburg
print(f'The first positive COVID case in Rockingham County was on {rham_first_case_date}.')
print(f'The first positive COVID case in Harrisonburg City was on {hburg_first_case_date}.\n')

    # write code to address the following question:
    # What day was the greatest number of new daily cases recorded in Harrisonburg? When was the greatest day in Rockingham County?

# Placeholder lists for the daily number of cases for Rockingham and Harrisonburg
rham_cases = []
hburg_cases = []

# Iterating through the Rockingham data list and storing all the number of cases
for i in range(len(rham_data)):
    data_point = rham_data[i]
    rham_cases.append(data_point.cases)

# Iterating through the Harrisonburg data list and storing all the number of cases
for i in range(len(hburg_data)):
    data_point = hburg_data[i]
    hburg_cases.append(data_point.cases)

# Variable holding the temporary maximum Rockingham and Harrisonburg daily case spike
rham_max = rham_cases[1] - rham_cases[0]
hburg_max = hburg_cases[1] - hburg_cases[0]

# Placeholder variables for the day of greatest increase for Rockingham and Harrisonburg
rham_max_day = 0
hburg_max_day = 0

# Iterating through the Rockingham data, finding the index of the day of greatest increase.
# Updating placeholder variables with that respective date for Harrisonburg and Rockingham
for i in range(len(rham_cases)):
    if (rham_cases[i] - rham_cases[i-1]) > rham_max:
        rham_max = rham_cases[i] - rham_cases[i-1]
        rham_max_day = rham_data[i].date
    elif (hburg_cases[i] - hburg_cases[i-1]) > hburg_max:
        hburg_max = hburg_cases[i] - hburg_cases[i-1]
        hburg_max_day = hburg_data[i].date


print(f'The day that the greatest number of new daily cases was recorded in Harrisonburg City was on {hburg_max_day}.')
print(f'The day that the greatest number of new daily cases was recorded in Rockingham County was on {rham_max_day}.\n')

    # write code to address the following question:
    # What was the worst seven day period in either the city and county for new COVID cases? This is the 7-day period where the number of new cases was maximal.

