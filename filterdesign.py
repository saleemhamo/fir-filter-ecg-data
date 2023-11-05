from abc import abstractmethod

import numpy as np
import pylab as pl


class FilterDesign:
    """
        # sampling_rate: Input, signal frequency
        # f1: Input, highpass cutoff frequency, determine range
        # M_coefficients: taps, finite (20231031: now don't find a good way to calculate )
    """

    @abstractmethod
    def highpass_design(self, sampling_rate, f1, m_coefficients=None):
        if m_coefficients is None:
            m_coefficients = int(10 * sampling_rate / f1)

        k1 = int(f1 / sampling_rate * m_coefficients)

        frequency_response = np.ones(m_coefficients)
        frequency_response[:k1 + 1] = 0
        frequency_response[m_coefficients - k1:] = 0

        x = np.fft.ifft(frequency_response)
        x = np.real(x)

        impulse_response = np.zeros(m_coefficients)
        impulse_response[0:int(m_coefficients / 2)] = x[int(m_coefficients / 2):m_coefficients]
        impulse_response[int(m_coefficients / 2):m_coefficients] = x[0:int(m_coefficients / 2)]

        return impulse_response, m_coefficients

    """
        # sampling_rate: Input, signal frequency
        # f1: Input, the low cutoff frequency, determine range
        # f2: Input, the high cutoff frequency, determine range
        # M_coefficients: taps, finite
        
    """

    @abstractmethod
    def band_stop_design(self, sampling_rate, f1, f2, m_coefficients=None):
        if m_coefficients is None:
            m_coefficients = int(10 * sampling_rate / min(f1, sampling_rate - f2))

        k1 = int(f1 / sampling_rate * m_coefficients)
        k2 = int(f2 / sampling_rate * m_coefficients)

        frequency_response = np.ones(m_coefficients)
        frequency_response[k1:k2 + 1] = 0
        frequency_response[m_coefficients - k2: m_coefficients - k1 + 1] = 0

        x = np.fft.ifft(frequency_response)
        x = np.real(x)

        impulse_response = np.zeros(m_coefficients)
        impulse_response[0:int(m_coefficients / 2)] = x[int(m_coefficients / 2):m_coefficients]
        impulse_response[int(m_coefficients / 2):m_coefficients] = x[0:int(m_coefficients / 2)]

        return impulse_response, m_coefficients
