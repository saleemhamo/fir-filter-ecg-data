import numpy as np
import matplotlib.pyplot as plt

# Define time parameters
duration = 1.0  # Duration of the ECG signal in seconds
fs = 1000  # Sampling frequency in Hz
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Generate the P-wave
p_wave = np.sin(2 * np.pi * 5 * t)  # A simple sinusoidal wave for the P-wave

# Generate the QRS complex
qrs_complex = (
    -np.exp(-0.5 * ((t - 0.1) / 0.1) ** 2) +  # Q-wave
    np.exp(-0.5 * ((t - 0.2) / 0.05) ** 2) -  # R-wave
    np.exp(-0.5 * ((t - 0.3) / 0.1) ** 2)     # S-wave
)

# Generate the T-wave
t_wave = 0.2 * np.sin(2 * np.pi * 1.0 * t)  # A simple sinusoidal wave for the T-wave

# Combine the components to create the ideal ECG wavelet
ecg_wavelet = p_wave + qrs_complex + t_wave

# Plot the ECG wavelet
plt.figure(figsize=(10, 4))
plt.plot(t, ecg_wavelet)
plt.title("Ideal ECG Wavelet")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()