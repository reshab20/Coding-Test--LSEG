import csv
from datetime import datetime, timedelta
import logging

# Configure logging and it's severity( Any logs upper than INFO will get triggered)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# Thresholds defined 
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

# Parse the CSV log file and take all the values as per the row and arranged in a dictionary and every dictionary is being appended over a list.
def parse_log_file(file_path):
    job_events = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 4:
                continue  
            timestamp_str, description, status, pid = map(str.strip, row)
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')
            job_events.append({
                'timestamp': timestamp,
                'description': description,
                'status': status,
                'pid': pid
            })
    return job_events

# On this function the list with dictionary of events is passed and from that list we are parsing the values and proivding the differences of time for PID's
def process_jobs(events):
    active_jobs = {}
    completed_jobs = []
    no_ending_jobs = []
    end_without_start_jobs = []  
    for event in events:
        pid = event['pid']
        if event['status'] == 'START':
            active_jobs[pid] = event
        elif event['status'] == 'END':
            if pid in active_jobs:
                start_event = active_jobs.pop(pid)
                duration = event['timestamp'] - start_event['timestamp']

                completed_jobs.append({
                    'pid': pid,
                    'description': start_event['description'],
                    'start_time': start_event['timestamp'],
                    'end_time': event['timestamp'],
                    'duration': duration
                })

                # Getting the outputs as per the threshold
                
                if duration > ERROR_THRESHOLD:
                    logging.error(f"Job {pid} ({start_event['description']}) took {duration}, which exceeds 10 minutes. i.e. ({start_event['timestamp']}) => ({event['timestamp']})")
                elif duration > WARNING_THRESHOLD:
                   logging.warning(f"Job {pid} ({start_event['description']}) took {duration}, which exceeds 5 minutes.  i.e. ({start_event['timestamp']}) => ({event['timestamp']})")
            else:
                logging.warning(f"END event found for unknown START (PID: {pid})")
                # Collect END without START
                end_without_start_jobs.append({
                    'pid': pid,
                    'description': event['description'],
                    'end_time': event['timestamp']
                })

    # Handling jobs with no END and printing those
    latest_timestamp = max(event['timestamp'] for event in events) if events else datetime.now()

    for pid, job in active_jobs.items():
        duration = latest_timestamp - job['timestamp']
        no_ending_jobs.append({
            'pid': pid,
            'description': job['description'],
            'start_time': job['timestamp'],
            'duration': duration
        })

        # Updated Rule for Logging NO ENDING JOB
        if duration > ERROR_THRESHOLD:
           logging.error(f"Job {pid} ({job['description']}) started at {job['timestamp']} and has NO ENDING JOB after {duration}.")
        elif duration > WARNING_THRESHOLD:
            logging.warning(f"Job {pid} ({job['description']}) started at {job['timestamp']} and has NO ENDING JOB after {duration}.")

    return completed_jobs, no_ending_jobs, end_without_start_jobs

# Generate final report
def generate_report(completed_jobs, no_ending_jobs, end_without_start_jobs):
    print("\n=== Completed Job Report ===")
    for job in completed_jobs:
        print(f"{job['description']} (PID: {job['pid']}): {job['start_time']} - {job['end_time']} => Duration: {job['duration']}")

    if no_ending_jobs:
        print("\n=== Jobs With NO ENDING EVENT ===")
        for job in no_ending_jobs:
            print(f"{job['description']} (PID: {job['pid']}): STARTED at {job['start_time']} => Duration so far: {job['duration']} (NO ENDING JOB)")

    if end_without_start_jobs:
        print("\n=== Jobs With END But NO START ===")
        for job in end_without_start_jobs:
            print(f"{job['description']} (PID: {job['pid']}): ENDED at {job['end_time']} but NO START recorded.")

# Main 
if __name__ == "__main__":
    log_file = "logs.log.csv"  
    events = parse_log_file(log_file)
    completed_jobs, no_ending_jobs, end_without_start_jobs = process_jobs(events)
    generate_report(completed_jobs, no_ending_jobs, end_without_start_jobs)
