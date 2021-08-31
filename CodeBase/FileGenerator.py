import os
import time
import csv


def add_to_file(package, path):
    # Creating the filename
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    filename = f"{month}{day}_StockCapture_Results.csv"

    os.chdir(path)

    api_data = package["api_data"]
    iteration = package["iteration"]
    timestamp = package["timestamp"]
    if not os.path.exists("Data\\" + filename):
        with open("Data\\" + filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            columns = list(api_data["MSFT"]["quote"].keys())
            columns.remove("fifty_two_week")
            columns.append("Iteration")
            columns.append("Timestamp")
            writer.writerow(columns)

    with open("Data\\" + filename, "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for symbol in api_data:
            api_data[symbol]["quote"].pop("fifty_two_week")
            row = list(api_data[symbol]["quote"].values())
            row.append(iteration)
            row.append(timestamp)
            writer.writerow(row)


if __name__ == "__main__":
    pass
