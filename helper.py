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


def plot(x, y, title, x_label, y_label, plot_name='', log_scale=False):
    plt.figure(figsize=(10, 6))
    plt.plot(y, x)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.grid(True)
    if log_scale:
        plt.xscale('log')

    plt.show()

    if not (plot_name is None or plot_name == ''):
        mkdir_if_not_exists('./output_images')
        plt.savefig('./output_images/' + plot_name + ".svg", format='svg')
