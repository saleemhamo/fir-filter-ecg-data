# hpbsfilter.py is the main program which uses firfilter to remove DC and 50Hz (1-3

import helper


def main():
    ecg_data = helper.read_ecg_data()
    time = helper.convert_to_time(len(ecg_data), 1000)

    # Plot the original data
    helper.plot(ecg_data, time, 'ECG Data (Original)', 'Time (s)', 'Amplitude')

    # data
    # highpass_cofficients = highpass_design(....)
    # band_stop_cofficients = band_stop_design(....)
    # fir_filter(highpass, data)
    # fir_filter(band_stop_cofficients, data)

main()
