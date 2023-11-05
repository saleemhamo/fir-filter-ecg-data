# hrdetect.py is the R peak and heartrate detector and must show a graph of the momentary heartrate against time (5).
import numpy as np

import helper
from filterdesign import FilterDesign
from firfilter import FIRFilter


def main():
    filtered_ecg, time = get_filtered_ecg()

    start_index = 950
    end_index = 1600

    # Extract one wavelet
    filtered_ecg_sample = filtered_ecg[start_index:end_index]
    wavelet_time = helper.convert_to_time(len(filtered_ecg_sample), 1000)
    helper.plot(filtered_ecg_sample, wavelet_time, 'ECG Data Sample (Wavelet)')

    wavelet = filtered_ecg_sample
    wavelet.reverse()
    helper.plot(wavelet, wavelet_time, 'Wavelet (reversed)')

    matched_filter = FIRFilter(wavelet)
    peeks = [matched_filter.dofilter(value) for value in filtered_ecg]

    helper.plot(peeks, time, 'Detected Peeks after Applying Matched Filter')

    peeks = [n ** 2 for n in peeks]

    helper.plot(peeks, time, 'Detected Peeks (after X^2)')

    filtered_peeks = [0 if x < 7 else x for x in peeks]

    helper.plot(filtered_peeks, time, 'Detected Peeks (after thresholding)')


def get_filtered_ecg():
    """ 1. Original ECG Signal """
    sampling_rate = 1000
    ecg_data = helper.read_ecg_data()
    time = helper.convert_to_time(len(ecg_data), sampling_rate)

    # Plot the original data
    helper.plot(ecg_data, time, 'ECG Data (Original)', 'ecg_original')

    """ 2. Create FIR filter coefficients """
    filter_design = FilterDesign()

    """ 2.a Band-stop Filter """

    # Set needed cutoff frequencies
    cutoff_freq_band_stop_low = 45  # Lower frequency for band-stop
    cutoff_freq_band_stop_high = 55  # Higher frequency for band-stop
    coefficients_band_stop, m = filter_design.band_stop_design(
        sampling_rate, cutoff_freq_band_stop_low, cutoff_freq_band_stop_high
    )
    coefficients_band_stop = coefficients_band_stop * np.hamming(m)

    """ 2.b Highpass Filter """
    # Set needed cutoff frequencies
    cutoff_freq_hp = 10  # Cutoff frequency for high-pass
    coefficients_hp, m = filter_design.highpass_design(sampling_rate, cutoff_freq_hp)
    coefficients_hp = coefficients_hp * np.hamming(m)

    """ 3. Process ECG signal """

    # Create FIR Filters
    fir_filter_band_stop = FIRFilter(coefficients_band_stop)
    fir_filter_highpass = FIRFilter(coefficients_hp)

    # Band-stop filtration
    filtered_band_stop_ecg = [fir_filter_band_stop.dofilter(value) for value in ecg_data]

    # Highpass filtration
    filtered_highpass_ecg = [fir_filter_highpass.dofilter(value) for value in filtered_band_stop_ecg]

    helper.plot(filtered_highpass_ecg, time, 'ECG Data (clean)')

    return filtered_highpass_ecg, time


if __name__ == '__main__':
    main()
