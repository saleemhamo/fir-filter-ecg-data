# hpbsfilter.py is the main program which uses firfilter to remove DC and 50Hz (1-3)
import numpy as np

import helper
from filterdesign import FilterDesign
from firfilter import FIRFilter


def main():
    """ 1. Original ECG Signal """
    sampling_rate = 1000
    ecg_data = helper.read_ecg_data()
    time = helper.convert_to_time(len(ecg_data), sampling_rate)
    fft_result_original, frequency_values_original = helper.convert_to_frequency(ecg_data, sampling_rate)

    # Plot the original data
    helper.plot(ecg_data, time, 'ECG Data (Original)', 'ecg_original')
    helper.plot_in_frequency(
        frequency_values_original, np.real(fft_result_original), 'ECG Data (Original)'
    )

    """ 2. Create FIR filter coefficients """
    filter_design = FilterDesign()

    """ 2.a Band-stop Filter """

    # Set needed cutoff frequencies
    cutoff_freq_band_stop_low = 45  # Lower frequency for band-stop
    cutoff_freq_band_stop_high = 55  # Higher frequency for band-stop
    coefficients_band_stop, m = filter_design.band_stop_design(
        sampling_rate, cutoff_freq_band_stop_low, cutoff_freq_band_stop_high
    )
    # TODO: Apply different windows
    coefficients_band_stop = coefficients_band_stop * np.hamming(m)
    # coefficients_band_stop = coefficients_band_stop * np.hanning(m)
    # coefficients_band_stop = coefficients_band_stop * np.tri(m)

    # Impulse Response (Band-stop)
    impulse_response_time = np.linspace(0, len(coefficients_band_stop), len(coefficients_band_stop))
    helper.plot(coefficients_band_stop, impulse_response_time, 'Impulse Response (Band-stop)')

    """ 2.b Highpass Filter """
    # Set needed cutoff frequencies
    cutoff_freq_hp = 0.5  # Cutoff frequency for high-pass
    coefficients_hp, m = filter_design.highpass_design(sampling_rate, cutoff_freq_hp)
    # TODO: Apply different windows
    coefficients_hp = coefficients_hp * np.hamming(m)

    # Impulse Response (Highpass)
    impulse_response_time = np.linspace(0, len(coefficients_hp), len(coefficients_hp))
    helper.plot(coefficients_hp, impulse_response_time, 'Impulse Response (Highpass)')

    """ 3. Process ECG signal """

    # Create FIR Filters
    fir_filter_band_stop = FIRFilter(coefficients_band_stop)
    fir_filter_highpass = FIRFilter(coefficients_hp)

    # Band-stop filtration
    filtered_band_stop_ecg = [fir_filter_band_stop.dofilter(value) for value in ecg_data]
    helper.plot(
        filtered_band_stop_ecg, time, 'ECG Data (Filtered - 50Hz removed)',
        'ecg_filtered_bs'
    )
    fft_result_band_stop, frequency_values_band_stop = helper.convert_to_frequency(filtered_band_stop_ecg, 1000)

    helper.plot_in_frequency(
        frequency_values_band_stop, np.real(fft_result_band_stop), 'ECG Data (Filtered - 50Hz removed)'

    )

    # Highpass filtration
    filtered_highpass_ecg = [fir_filter_highpass.dofilter(value) for value in filtered_band_stop_ecg]
    helper.plot(filtered_highpass_ecg, time, 'ECG Data (Filtered - 50Hz & DC removed)',
                'ecg_filtered_hb')
    fft_result_highpass, frequency_values_highpass = helper.convert_to_frequency(filtered_highpass_ecg, 1000)

    helper.plot_in_frequency(
        frequency_values_highpass, np.real(fft_result_highpass),
        'ECG Data (Filtered - 50Hz & DC removed)'
    )


if __name__ == '__main__':
    main()
