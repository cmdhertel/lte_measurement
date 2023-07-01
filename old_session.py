import csv
from datetime import datetime


class Session:
    def __init__(self, pci) -> None:
        self.pci = pci
        self.timestamps = []

    def add_timestamp(self, timestamp):
        self.timestamps.append(timestamp)

def calculate_session_duration(csv_file):
    session_times = {}
    
    # Read CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        
        # Skip header row if present
        next(csv_reader)
        last_pci = 0
        # Process each row
        for row in csv_reader:
            timestamp, pci = row[0], row[9]
            if pci is not last_pci:
               session = Session(row[9]) 
               session.add_timestamp(timestamp)
            else:
               session.add_timestamp(timestamp)
            last_pci = pci
    # Calculate session durations and create a list of tuples
    session_table = []
    for session_id, timestamps in session_times.items():
        start_timestamp = timestamps['start']
        end_timestamp = timestamps['end']
        duration = end_timestamp - start_timestamp
        session_table.append((start_timestamp, end_timestamp, duration, session_id))
    
    # Sort the session table by start timestamp
    session_table.sort(key=lambda x: x[0])
    
    # Print the session table
    print("Start Timestamp\tEnd Timestamp\tDuration\tID")
    for row in session_table:
        start_timestamp, end_timestamp, duration, session_id = row
        print(f"{start_timestamp}\t{end_timestamp}\t{duration}\t{session_id}")

# Usage
if __name__ == "__main__":
    calculate_session_duration("./data/hfapp_measrurement.csv")
