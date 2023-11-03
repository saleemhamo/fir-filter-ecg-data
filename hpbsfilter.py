# hpbsfilter.py is the main program which uses firfilter to remove DC and 50Hz (1-3

import helper
from firfilter import FIRFilter
from filterdesign import FilterDesign

# def main():
ecg_data = helper.read_ecg_data()
time = helper.convert_to_time(len(ecg_data), 1000)
fft_result_ori, frequency_values_ori = helper.convert_to_frequency(ecg_data, 1000)

# Plot the original data
helper.plot(ecg_data, time, 'ECG Data (Original)', 'Time (s)', 'Amplitude')
helper.plot_in_frequency(frequency_values_ori, fft_result_ori, 'ECG Data(Original)', 'Frequency(HZ)', 'Amplitude')

# Set needed cutoff frequencies
sampling_rate = 1000
cutoff_freq_hp = 0.5  # Adjust this cutoff frequency as needed
cutoff_freq_bs_low = 45  # Lower frequency for bandstop
cutoff_freq_bs_high = 55  # Higher frequency for bandstop

# Create FIR filter coefficients
filter_design = FilterDesign()
coeff_hp = filter_design.highpass_design(sampling_rate, cutoff_freq_hp)
coeff_bs = filter_design.band_stop_design(sampling_rate, cutoff_freq_bs_low, cutoff_freq_bs_high)
firfilter_hp = FIRFilter(coeff_hp)
firfilter_bs = FIRFilter(coeff_bs)

# Process ECG signal
filtered_hp_ecg = [firfilter_hp.dofilter(value) for value in ecg_data]
filtered_ecg = [firfilter_bs.dofilter(value) for value in filtered_hp_ecg]

# Plot filtered ECG signals
fft_result_fil, frequency_values_fil = helper.convert_to_frequency(filtered_ecg, 1000)
helper.plot(filtered_ecg, time, 'ECG Data (Filtered)', 'Time (s)', 'Amplitude')
helper.plot_in_frequency(frequency_values_fil, fft_result_fil, 'ECG Data(Filtered)', 'Frequency(HZ)', 'Amplitude')

# main()