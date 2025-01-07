import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy
def plot_columns(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Extract the columns for arrivalTime and processedTime as numpy arrays
    arrival_time = df['arrivalTime'].to_numpy()  # Convert to numpy array
    processed_time = df['processedTime'].to_numpy()  # Convert to numpy array
    #event_time = df['eventTime'].to_numpy()  # Convert to numpy array

    # Plot the data as two separate lines
    plt.figure(figsize=(10, 6))
    plt.plot(arrival_time, label='Arrival Time', color='b', linestyle='-')
    plt.plot(processed_time, label='Processed Time', color='r', linestyle='-')
    #plt.plot(event_time, label='Event Time', color='g', linestyle='-')

    # Set labels and title
    plt.xlabel('Index')
    plt.ylabel('Time')
    plt.title('Event Time, Arrival Time,Processed Time')

    # Show the legend
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Check if a CSV file was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    # Get the CSV file name from the argument
    csv_file = sys.argv[1]

    # Plot the columns
    plot_columns(csv_file)
