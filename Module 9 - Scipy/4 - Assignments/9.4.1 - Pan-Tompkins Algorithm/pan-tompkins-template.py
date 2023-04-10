import numpy as np
from scipy.signal import find_peaks, butter, filtfilt

from ekg_testbench import EKGTestBench

def main(filepath):
    if filepath == '':
        return list()

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    ekg_data = np.loadtxt(path, skiprows=2, delimiter=',')

    # save each vector as own variable
    time = ekg_data[:, 0]
    v5 = ekg_data[:, 1]
    v2 = ekg_data[:, 2]

    # identify one column to process. Call that column signal

    signal = v2

    # Finding sample frequency
    sample_freq = 1 / time[1]

    # Lowpass cutoff frequency (Hz)
    lcf = 11

    # Highpass cutoff frequency (Hz)
    hcf = 5

    # pass data through LOW PASS FILTER (OPTIONAL)
    b, a = butter(N=1, Wn=lcf, btype='lowpass', output='ba', fs=sample_freq)
    signal = filtfilt(b, a, signal)
    #signal = np.convolve(signal, a)

    # pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
    b2, a2 = butter(N=1, Wn=hcf, btype='highpass', output='ba', fs=sample_freq)
    signal = filtfilt(b2, a2, signal)

    # Filter again
    #signal = filtfilt(b, a, signal)
    signal = filtfilt(b2, a2, signal)

    #Multiply by scalar to make threshold easier
    signal *= 10
    #signal = np.convolve(signal, a2)

    # pass data through differentiator
    signal = np.diff(signal)

    # pass data through square function
    signal = np.square(signal)

    # Square again to amplify noise/signal delta
    #signal = np.square(signal)

    # create a moving average window of length 15% of sample rate
    window = []
    window_length = int(sample_freq * .1)

    for i in range(1, window_length + 1):
        window.append(int(i / i))

    # pass through moving average window
    signal = np.convolve(signal, window)

    # use find_peaks to identify peaks within averaged/filtered data
    # save the peaks result and return as part of testbench result

    ## your code here peaks,_ = find_peaks(....)
    # current solution: height=.0002, distance=175
    #peaks, _ = find_peaks(signal, height=.02, distance=100)

    # Finding possible peaks
    possible_peaks, _ = find_peaks(signal, distance=125)

    # Initialize signal peak, noise peak, and threshold
    spk = signal[possible_peaks[0]]
    npk = .1 * spk
    threshold1 = npk + (.25 * (spk - npk))
    threshold2 = .5 * threshold1

    # Placeholder for real peaks
    peaks = []

    # Identifying real peaks
    for i in range(len(possible_peaks)):

        if possible_peaks[i] - possible_peaks[i-1] >= 300:
            if signal[possible_peaks[i]] > threshold2:
                spk = .25 * signal[possible_peaks[i]] + .75 * spk
                peaks.append(possible_peaks[i])

        elif signal[possible_peaks[i]] > threshold1:
            spk = (.125 * signal[possible_peaks[i]]) + (.875 * spk)
            peaks.append(possible_peaks[i])

        else:
            npk = (.125 * signal[possible_peaks[i]]) + (.875 * npk)

        threshold1 = npk + (.25 * (spk - npk))
        threshold2 = .5 * threshold1

    peaks = np.asarray(peaks)

    # do not modify this line
    return signal, peaks


# when running this file directly, this will execute first
if __name__ == "__main__":

    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    database_name = 'qtdb_sel104'

    # set to true if you wish to generate a debug file
    file_debug = True

    # set to true if you wish to print overall stats to the screen
    print_debug = True

    # set to true if you wish to show a plot of each detection process
    show_plot = True

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    path_to_folder = "../../../data/ekg/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = main(signal_filepath)

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    print("Done!")
