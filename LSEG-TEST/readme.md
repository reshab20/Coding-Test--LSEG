# Log Monitoring Application

This project provides a **Python-based log analyzer** designed to process CSV logs of job executions.  
It tracks jobs from their `START` and `END` events, calculates durations, detects anomalies, and produces a structured report.  
The tool is particularly useful for **monitoring batch jobs, scheduled tasks, or background processes**.

---

##  Features

- **CSV Parsing**
  - Reads structured job event logs in CSV format.
  - Ignores malformed lines automatically.

- **Job Duration Tracking**
  - Calculates job execution times between `START` and `END`.
  - Reports ongoing jobs with no `END` entry.

- **Threshold Monitoring**
  - **Warning**: Jobs exceeding **5 minutes**.
  - **Error**: Jobs exceeding **10 minutes**.

- **Anomaly Detection**
  - Logs cases where `END` events appear without a matching `START`.
  - Identifies jobs that started but never ended.

- **Readable Report**
  - Summarizes **completed jobs** with execution times.
  - Lists **jobs still running** without an ending event.

---

##  Log File Format

The log file must be in **CSV format** with 4 fields per row:

```
timestamp, description, status, pid
```

- **timestamp** → Time of the event in `HH:MM:SS` (24-hour format).  
- **description** → Short description of the job.  
- **status** → Either `START` or `END`.  
- **pid** → Process/job ID (must match across start and end events).  

###  Example Log File (`logs.log.csv`)

```csv
12:00:00, Job A, START, 101
12:03:00, Job B, START, 102
12:08:00, Job A, END, 101
12:15:00, Job B, END, 102
12:20:00, Job C, START, 103
```

---

##  How to Use

1. Clone or download this repository.  
   ```bash
   git clone https://github.com/reshab20/Coding-Test--LSEG.git
   cd LSEG-TEST
   ```

2. Place your log file in the same directory as the script.  
   By default, the script looks for:
   ```
   logs.log.csv
   ```

3. Run the analyzer:
   ```bash
   python Log_Monitoring_application.py
   ```

---


##  Requirements

- Python 3.x  
- No third-party dependencies (uses only Python Standard Library).  

---

---

##  Configuration

You can configure job duration thresholds directly in the script:

```python
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)
```

- Modify the values to suit your monitoring requirements.  
- Example: Set to 2 minutes and 4 minutes for shorter tasks.

---



##  Example Output

### Console Report
```
=== Completed Job Report ===
scheduled task 032 (PID: 37980): 1900-01-01 11:35:23 - 1900-01-01 11:35:56 => Duration: 0:00:33
scheduled task 796 (PID: 57672): 1900-01-01 11:36:11 - 1900-01-01 11:36:18 => Duration: 0:00:07
scheduled task 386 (PID: 10515): 1900-01-01 11:38:33 - 1900-01-01 11:40:24 => Duration: 0:01:51

=== Jobs With NO ENDING EVENT ===
scheduled task 333 (PID: 72029): STARTED at 1900-01-01 12:03:20 => Duration so far: 0:15:54 (NO ENDING JOB)
scheduled task 016 (PID: 72897): STARTED at 1900-01-01 12:12:27 => Duration so far: 0:06:47 (NO ENDING JOB)
```

### Logging Messages
Depending on job duration and state:
```
ERROR: Job 39547 (scheduled task 051) took 0:11:29, which exceeds 10 minutes. i.e. (1900-01-01 11:37:53) => (1900-01-01 11:49:22)
ERROR: Job 45135 (scheduled task 515) took 0:12:23, which exceeds 10 minutes. i.e. (1900-01-01 11:37:14) => (1900-01-01 11:49:37)
WARNING: Job 71766 (scheduled task 074) took 0:05:47, which exceeds 5 minutes.  i.e. (1900-01-01 11:45:04) => (1900-01-01 11:50:51)
ERROR: Job 81258 (background job wmy) took 0:14:46, which exceeds 10 minutes. i.e. (1900-01-01 11:36:58) => (1900-01-01 11:51:44)
```






