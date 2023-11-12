# lmsfilter.py is the main program which uses an LMS filter to remove 50Hz (4)
import numpy as np

import helper


class LMSFilter:

    def __init__(self, _coefficients):
        self._coefficients = _coefficients
        self.buffer = [0] * len(_coefficients)

    def do_filter(self, value):
        self.buffer = [value] + self.buffer[:-1]
        result = 0
        for h, v in zip(self._coefficients, self.buffer):
            result = result + h * v
        return result

    def do_filter_adaptive(self, signal_sample, noise, learning_rate):
        canceller = self.do_filter(noise)
        error = signal_sample - canceller

        for j in range(len(self._coefficients)):
            self._coefficients[j] = self._coefficients[j] + error * learning_rate * self.buffer[j]

        return signal_sample - canceller


def filter_signal_lms():
    sampling_rate = 1000
    ecg_data = helper.read_ecg_data()
    time = helper.convert_to_time(len(ecg_data), sampling_rate)
    helper.plot(ecg_data, time, 'ECG Data (Original)')

    n_taps = 100
    learning_rate = 0.01
    f_noise = 50
    filtered_signal = np.empty(len(ecg_data))
    lms_coefficients = np.zeros(n_taps)
    lms_filter = LMSFilter(lms_coefficients)

    for i in range(len(ecg_data)):
        ref_noise = np.sin(2.0 * np.pi * f_noise / sampling_rate * i)
        output_signal = lms_filter.do_filter_adaptive(ecg_data[i], ref_noise, learning_rate)
        filtered_signal[i] = output_signal

    helper.plot(
        filtered_signal, time, 'ECG Data (LMS Filter - 50Hz removal)',
        'ecg_filtered_lms'
    )

    return filtered_signal


if __name__ == '__main__':
    filter_signal_lms()
