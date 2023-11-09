# hrdetect.py is the R peak and heartrate detector and must show a graph of the momentary heartrate against time (5).
import numpy as np

import helper
from firfilter import FIRFilter
from hpbsfilter import main as get_filtered_ecg


def main():
    filtered_ecg, time = get_filtered_ecg(False)
    helper.plot(filtered_ecg, time, 'ECG Data (Filtered - 50Hz & DC removed)')

    wavelet, wavelet_time = extract_wavelet_from_ecg(filtered_ecg)
    detect_peeks(wavelet, wavelet_time, filtered_ecg, time, 'ECG Data Sample', 'ecg_data')

    wavelet, wavelet_time = generate_sinc_wavelet()
    detect_peeks(wavelet, wavelet_time, filtered_ecg, time, 'Sinc Pulse', 'sinc_pulse')


def detect_peeks(wavelet, wavelet_time, filtered_ecg, time, wavelet_type, plot_prefix):
    helper.plot(wavelet, wavelet_time, wavelet_type + ' (Wavelet)', plot_prefix + '_wavelet')

    # Reverse
    wavelet.reverse()
    helper.plot(wavelet, wavelet_time, wavelet_type + 'Wavelet (reversed)', plot_prefix + '_wavelet_reversed')

    # Apply Matched Filter
    matched_filter = FIRFilter(wavelet)
    peeks = [matched_filter.dofilter(value) for value in filtered_ecg]
    helper.plot(peeks, time, wavelet_type + ' Detected Peeks after Applying Matched Filter', plot_prefix + 'peeks')

    # Square signal
    peeks = [n ** 2 for n in peeks]
    helper.plot(peeks, time, wavelet_type + ' Detected Peeks (after X^2)', plot_prefix + 'peeks_squared')

    # Threshold signal
    filtered_peeks = [0 if x < 7 else x for x in peeks]
    helper.plot(filtered_peeks, time, wavelet_type + ' Detected Peeks (after thresholding)',
                plot_prefix + 'peeks_threshold')


def extract_wavelet_from_ecg(filtered_ecg):
    start_index = 10500
    end_index = 11100

    # Extract one wavelet
    filtered_ecg_sample = filtered_ecg[start_index:end_index]
    wavelet_time = helper.convert_to_time(len(filtered_ecg_sample), 1000)

    return filtered_ecg_sample, wavelet_time


def generate_sinc_wavelet():
    x = np.linspace(-4, 4, 41)
    return np.sinc(x).tolist(), x


if __name__ == '__main__':
    main()
