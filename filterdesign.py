from abc import abstractmethod
import numpy as np
import helper
import matplotlib.pyplot as plt
from scipy import signal


class FilterDesign:

    @abstractmethod
    def highpass_design(self, sampling_rate, f1,M_coefficients = None):
        # sampling_rate: Input, signal frequency
        # f1: Input, highpass cutoff frequency, determine range
        # M_coefficients: taps, finite (20231031: now don't find a good way to calculate ) 
        
        if M_coefficients is None:
            M_coefficients = int(10 * sampling_rate /  f1) # 20231031:find in chartgpt...
            # M_coefficients =signal.buttord() /signal.order_filter(input_signal, target_response, n)
            if M_coefficients % 2 == 0:
                M_coefficients += 1  
        # H(z) set the highpass filter of M_coefficients in frequency domain
        filter_hp_fre = np.zeros(M_coefficients, dtype=complex)
        DC = 1
        filter_hp_fre[M_coefficients // 2] = DC 
        for single_coefficient in range(1, M_coefficients // 2):
            # write the coefficient formula, need to double check 
            filter_hp_fre[(M_coefficients//2) + single_coefficient] = 2*np.sin(2*np.pi*single_coefficient*f1/sampling_rate)/(np.pi*single_coefficient) 
        
        return np.real(np.fft.ifft(filter_hp_fre))


    @abstractmethod
    def band_stop_design(self, sampling_rate, f1, f2,M_coefficients=None):
        # sampling_rate: Input, signal frequency
        # f1: Input, the low cutoff frequency, determine range
        # f2: Input, the high cutoff frequency, determine range
        # M_coefficients: taps, finite 
        if M_coefficients is None:
            M_coefficients = int(10 * sampling_rate/min(f1, sampling_rate - f2)) # 20231031:find in chartgpt...
            # M_coefficients =signal.buttord() /signal.order_filter(input_signal, target_response, n)
            if M_coefficients % 2 == 0:
                M_coefficients += 1  
        # H(z) set the band stop filter of M_coefficients in frequency domain
        filter_bs_fre = np.zeros(M_coefficients, dtype=complex)
        DC = 1
        filter_bs_fre[M_coefficients // 2] = DC
        for single_coefficient in range(1, M_coefficients// 2):
            filter_bs_fre[(M_coefficients// 2) + single_coefficient] = (np.sin(2 * np.pi * single_coefficient* f1 / sampling_rate) /(np.pi * single_coefficient))-\
                  (np.sin(2 * np.pi * single_coefficient * f2 / sampling_rate) /(np.pi * single_coefficient))
        return np.real(np.fft.ifft(filter_bs_fre))

# simple test
# sampling_rate = 1000  # 采样率为1000 Hz
# cutoff_freq_highpass = 50  # 高通滤波器的截止频率为50 Hz
# low_cutoff_freq_bandstop = 40  # 带通滤波器的低截止频率为40 Hz
# high_cutoff_freq_bandstop = 60  # 带通滤波器的高截止频率为60 Hz

# filter_test = FilterDesign()

# highpass_coefficients = filter_test.highpass_design(sampling_rate,cutoff_freq_highpass)

# bandstop_coefficients = filter_test.band_stop_design(sampling_rate,low_cutoff_freq_bandstop, high_cutoff_freq_bandstop)

# # plot
# w_highpass, h_highpass = signal.freqz(highpass_coefficients, worN=8000)
# w_bandstop, h_bandstop = signal.freqz(bandstop_coefficients, worN=8000)
# plt.figure(figsize=(10, 6))

# plt.subplot(2, 1, 1)
# plt.title("High-Pass Filter Frequency Response")
# plt.plot(w_highpass, abs(h_highpass), 'b')
# plt.xlabel('Frequency [radians / sample]')
# plt.ylabel('Amplitude')

# plt.subplot(2, 1, 2)
# plt.title("Bandstop Filter Frequency Response")
# plt.plot(w_bandstop, abs(h_bandstop), 'b')
# plt.xlabel('Frequency [radians / sample]')
# plt.ylabel('Amplitude')
# plt.tight_layout()
# plt.show()

