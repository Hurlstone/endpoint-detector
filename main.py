import psutil #Processes and system utilities library
import time # For sleeping
from datetime import datetime # For logging time

# Store previous processes
previous_processes = {}

first_run = True

#Keywords to flag in processes
suspicious_processes = ["nc", "nmap", "tcpdump"]

# Function for writing a string/event to the log file
def log_event(event):
    # Timing
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS:MM [:-3] removes the last 3 digits
    formatted_event = f"{formatted_time} | {event}"
    with open("events.log", "a") as file:
        file.write(formatted_event + "\n")
    print(formatted_event)

while True:
    print("Monitoring processes")

    # Store current processes
    current_processes = {}

    # Iterate through all processes running on the device and print it out
    for process in psutil.process_iter(['pid', 'name', 'username', 'create_time']):


        #print(f"PID: {process.info['pid']} | Name: {process.info['name']} | Username: {process.info['username']}")
        try:
            if process.info['create_time'] is None:
                continue
            current_processes[(process.info['pid'], process.info['create_time'])] = process.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


    if first_run:
        previous_processes = current_processes
        first_run = False
    else:
        # Calculate the new processes
        new_processes = current_processes.keys() - previous_processes.keys()

        terminated_processes = previous_processes.keys() - current_processes.keys()

        for process_key in new_processes:
            pid = process_key[0]
            event = f"[NEW PROCESS] PID: {pid} | Name: {current_processes[process_key]}"
            # Write new events to log file
            log_event(event)
            # Check for suspicious processes
            if current_processes[process_key] in suspicious_processes:
                suspicious_event = f"[WARNING SUSPICIOUS PROCESS] PID: {pid} | Name: {current_processes[process_key]}"
                log_event(suspicious_event)


        for process_key in terminated_processes:
            pid = process_key[0]
            event = f"[TERMINATED PROCESS] PID: {pid} | Name: {previous_processes[process_key]}"

            # Write terminated events to log file
            log_event(event)

        previous_processes = current_processes

    # Pause execution for updated list in seconds
    time.sleep(1)
