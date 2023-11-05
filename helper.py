import matplotlib.pyplot as plt
import os
import numpy as np


def read_ecg_data():
    ecg_data_path = "ecg.dat"

    # Initialize an empty list to store the numeric records
    numeric_records = []

    with open(ecg_data_path, "r") as file:
        for line in file:
            try:
                # Attempt to convert the line to a numeric value (e.g., float or int)
                numeric_value = float(line)
                numeric_records.append(numeric_value)
            except ValueError:
                # Handle non-numeric lines, if any
                print(f"Ignoring non-numeric line: {line.strip()}")

    return numeric_records


def convert_to_time(number_of_samples, sample_rate):
    stop = number_of_samples / sample_rate
    return np.linspace(0, stop, number_of_samples)


def mkdir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")


def plot(x, y, title, plot_name='', log_scale=False):
    plt.figure(figsize=(10, 6))
    plt.plot(y, x)
    plt.title(title)
    plt.xlabel('Time (s)'),
    plt.ylabel('Amplitude')
    if log_scale:
        plt.xscale('log')

    plt.show()

    if not (plot_name is None or plot_name == ''):
        mkdir_if_not_exists('./output_images')
        plt.savefig('./output_images/' + plot_name + ".svg", format='svg')


""" Frequency domain functions """


def fft(signal):
    return np.fft.fft(signal)


def ifft(fft):
    return np.fft.ifft(fft)


def convert_to_frequency(signal, sample_rate):
    fft_result = fft(signal)
    frequency_values = np.fft.fftfreq(fft_result.size, 1 / sample_rate)
    return fft_result, frequency_values


def plot_in_frequency(frequency_values, fft_result, title, plot_name='', log_scale=False):
    plt.figure(figsize=(10, 6))
    plt.plot(frequency_values[frequency_values > 0], abs(fft_result[frequency_values > 0]), color='g')
    plt.title(title)
    plt.xlabel('Frequency (HZ)')
    plt.ylabel('Amplitude')
    plt.show()

    if not (plot_name is None or plot_name == ''):
        mkdir_if_not_exists('./output_images')
        plt.savefig('./output_images/' + plot_name + ".svg", format='svg')
