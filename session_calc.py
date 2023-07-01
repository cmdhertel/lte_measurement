#!/usr/bin/env python
import csv
from datetime import datetime


class Session:
    def __init__(self, pci) -> None:
        self.pci = pci
        self.timestamps = []

    def add_timestamp(self, timestamp):
        self.timestamps.append(timestamp)

    def get_starttime(self) -> int:
        return int(self.timestamps[0])

    def get_endtime(self) -> int:
        return int(self.timestamps[-1])

    def get_duration_ms(self) -> int:
        return int(self.timestamps[-1]) - int(self.timestamps[0])

def read_sessions(csv_file) -> list:
    '''
    read csv file which include the lte measurements and create from this a list from session
    '''
    # Read CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        sessions = []

        # Skip header row if present
        next(csv_reader)
        last_pci = 0
        # Process each row
        for row in csv_reader:
            timestamp, pci = row[0], row[9]
            if pci != last_pci:
               session = Session(row[9]) 
               session.add_timestamp(timestamp)
               sessions.append(session)
            else:
               session.add_timestamp(timestamp)
            last_pci = pci
    # Calculate session durations and create a list of tuples
    return sessions

def write_csv(sessions, filename):
    '''
    write for each session a line in a csv file
    '''
    counter = 0
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['uid','pci', 'starttime', 'endtime', 'duration'])  # Write the header row

        # Write data for each object
        for session in sessions:
            duration = session.get_duration_ms()
            writer.writerow([counter, session.pci, datetime.utcfromtimestamp(session.get_starttime() / 1000).strftime('%H:%M:%s'), datetime.utcfromtimestamp(session.get_endtime() / 1000).strftime('%H:%M:%s'), duration])
            counter += 1

    print(f"CSV file '{filename}' created successfully.")

def calculate_session_time(sessions):
    '''
    simple output for each session, which pci was connected and the duration in s
    '''
    for session in sessions:
        duration_ms = session.get_duration_ms()
        duration = duration_ms / 1000
        print(f"Connection for {session.pci} was {duration}s long.")
# Usage
if __name__ == "__main__":
    #calculate_session_time(read_sessions("./data/hfapp_measrurement.csv"))
    write_csv(read_sessions("./data/hfapp_measrurement.csv"), "./sessions.csv")
    calculate_session_time(read_sessions("./data/hfapp_measrurement.csv"))
