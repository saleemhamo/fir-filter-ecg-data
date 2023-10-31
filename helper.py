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
