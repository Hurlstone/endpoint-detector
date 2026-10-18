import psutil #Processes and system utilities library
import time # For sleeping

# Store previous processes
previous_processes = {}
first_run = True

while True:
    print("Monitoring processes")
    # Store current processes
    current_processes = {}
    # Iterate through all processes running on the device and print it out
    for process in psutil.process_iter(['pid', 'name', 'username']):
        #print(f"PID: {process.info['pid']} | Name: {process.info['name']} | Username: {process.info['username']}")
        current_processes[process.info['pid']] = process.info['name']


    if first_run:
        previous_processes = current_processes
        first_run = False
    else:
        # Calculate the new processes
        new_processes = current_processes.keys() - previous_processes.keys()

        terminated_processes = previous_processes.keys() - current_processes.keys()

        for pid in new_processes:
            print(f"[NEW PROCESS] PID: {pid} | Name: {current_processes[pid]}")

        for pid in terminated_processes:
            print(f"[TERMINATED PROCESS] PID: {pid} | Name: {previous_processes[pid]}")

        previous_processes = current_processes
    # Pause execution for updated list in seconds
    time.sleep(1)