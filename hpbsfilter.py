# hpbsfilter.py is the main program which uses firfilter to remove DC and 50Hz (1-3)
import numpy as np

import helper
from filterdesign import FilterDesign
from firfilter import FIRFilter
from lmsfilter import filter_signal_lms


def main(plot=True):
    """ 1. Original ECG Signal """
    print("Reading ECG Data")
    sampling_rate = 1000
    ecg_data = helper.read_ecg_data()
    time = helper.convert_to_time(len(ecg_data), sampling_rate)
    fft_result_original, frequency_values_original = helper.convert_to_frequency(ecg_data, sampling_rate)

    # Plot the original data
    if plot:
        helper.plot(ecg_data, time, 'ECG Data (Original)', 'ecg_original')
        helper.plot_in_frequency(
            frequency_values_original, np.real(fft_result_original), 'ECG Data (Original)', 'ecg_original_freq'
        )

    """ 2. Create FIR filter coefficients """
    filter_design = FilterDesign()

    """ 2.a Band-stop Filter """

    # Set needed cutoff frequencies
    cutoff_freq_band_stop_low = 45  # Lower frequency for band-stop
    cutoff_freq_band_stop_high = 55  # Higher frequency for band-stop
    coefficients_band_stop, m, frequency_response_band_stop, inverse_fft = filter_design.band_stop_design(
        sampling_rate, cutoff_freq_band_stop_low, cutoff_freq_band_stop_high
    )

    frequency_response_time = np.linspace(-1 * np.pi, np.pi, len(frequency_response_band_stop))
    if plot:
        helper.plot(
            frequency_response_band_stop, frequency_response_time, 'Frequency Response (Band-stop)', 'freq_response_bs'
        )

    impulse_response_time = np.linspace(0, len(coefficients_band_stop), len(coefficients_band_stop))

    if plot:
        helper.plot(
            inverse_fft, impulse_response_time, 'Impulse Response (Band-stop)', 'bs_impulse_response_1'
        )
        helper.plot(
            coefficients_band_stop, impulse_response_time, 'Impulse Response (Band-stop)', 'bs_impulse_response'
        )

    # Apply hamming window
    coefficients_band_stop = coefficients_band_stop * np.hamming(m)

    # Impulse Response (Band-stop)
    if plot:
        helper.plot(
            coefficients_band_stop, impulse_response_time, 'Impulse Response (Band-stop) - Hamming Window',
            'bs_impulse_response_window'
        )

    """ 2.b Highpass Filter """
    # Set needed cutoff frequencies
    cutoff_freq_hp = 0.5  # Cutoff frequency for high-pass
    coefficients_hp, m, frequency_response_highpass, inverse_fft = filter_design.highpass_design(
        sampling_rate, cutoff_freq_hp
    )

    frequency_response_time = np.linspace(-1 * np.pi, np.pi, len(frequency_response_highpass))
    if plot:
        helper.plot(
            frequency_response_highpass, frequency_response_time, 'Frequency Response (Highpass)', 'freq_response_hp'
        )

    impulse_response_time = np.linspace(0, len(coefficients_hp), len(coefficients_hp))
    if plot:
        helper.plot(
            inverse_fft, impulse_response_time, 'Impulse Response (Highpass)', 'hp_impulse_response_1'
        )
        helper.plot(
            coefficients_hp, impulse_response_time, 'Impulse Response (Highpass)', 'hp_impulse_response'
        )

    # Apply hamming window
    coefficients_hp = coefficients_hp * np.hamming(m)

    # Impulse Response (Highpass)
    if plot:
        helper.plot(
            coefficients_hp, impulse_response_time, 'Impulse Response (Highpass) - Hamming Window',
            'hp_impulse_response_window'
        )

    """ 3. Process ECG signal """

    # Create FIR Filters
    fir_filter_band_stop = FIRFilter(coefficients_band_stop)
    fir_filter_highpass = FIRFilter(coefficients_hp)

    # Band-stop filtration
    print(
        "Filtering ECG data using Band-stop FIR filter (f1: " + str(cutoff_freq_band_stop_low) + ", f2: " +
        str(cutoff_freq_band_stop_high) + ")"
    )
    filtered_band_stop_ecg = [fir_filter_band_stop.dofilter(value) for value in ecg_data]
    if plot:
        helper.plot(
            filtered_band_stop_ecg, time, 'ECG Data (Filtered - 50Hz removed)',
            'ecg_filtered_bs'
        )
    fft_result_band_stop, frequency_values_band_stop = helper.convert_to_frequency(filtered_band_stop_ecg, 1000)
    if plot:
        helper.plot_in_frequency(
            frequency_values_band_stop, np.real(fft_result_band_stop), 'ECG Data (Filtered - 50Hz removed)',
            'ecg_filtered_bs_frequency'
        )

    # Highpass filtration
    print("Filtering ECG data using Highpass FIR filter (fc: " + str(cutoff_freq_hp) + ")")
    filtered_highpass_ecg = [fir_filter_highpass.dofilter(value) for value in filtered_band_stop_ecg]
    if plot:
        helper.plot(
            filtered_highpass_ecg, time, 'ECG Data (Filtered - 50Hz & DC removed)',
            'ecg_filtered_hb'
        )
    fft_result_highpass, frequency_values_highpass = helper.convert_to_frequency(filtered_highpass_ecg, 1000)
    if plot:
        helper.plot_in_frequency(
            frequency_values_highpass, np.real(fft_result_highpass), 'ECG Data (Filtered - 50Hz & DC removed)',
            'ecg_filtered_hp_frequency'
        )

    filtered_wavelet, wavelet_time = extract_wavelet_from_ecg(filtered_highpass_ecg)
    if plot:
        helper.plot(filtered_wavelet, wavelet_time, 'ECG Wavelet (After FIR Filtration)', 'ecg_fir_wavelet')

    """ LMS Adaptive Filter """
    filtered_signal_lms = filter_signal_lms()

    # Apply Highpass filter
    fir_filter_highpass = FIRFilter(coefficients_hp)
    filtered_highpass_ecg_lms = [fir_filter_highpass.dofilter(value) for value in filtered_signal_lms]
    if plot:
        helper.plot(
            filtered_highpass_ecg_lms, time, 'ECG Data (After LMS 50Hz + Highpass Filtration)',
            'ecg_filtered_lms'
        )

    filtered_wavelet, wavelet_time = extract_wavelet_from_ecg(filtered_highpass_ecg_lms, 10450, 11050)
    if plot:
        helper.plot(filtered_wavelet, wavelet_time, 'ECG Wavelet (After LMS Filtration)', 'ecg_lms_wavelet')

    return filtered_highpass_ecg, time


def extract_wavelet_from_ecg(signal, start_index=10500, end_index=11100):
    # Extract one wavelet
    filtered_ecg_sample = signal[start_index:end_index]
    wavelet_time = helper.convert_to_time(len(filtered_ecg_sample), 1000)

    return filtered_ecg_sample, wavelet_time


if __name__ == '__main__':
    main()
