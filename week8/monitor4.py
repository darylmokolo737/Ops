#!/usr/bin/python3
### Script to monitor local machine health status including file hashes, ping checks, CPU load, disk usage, and memory usage.
### DM-1102024

import os
import csv
import subprocess
import psutil
import platform
import hashlib
from datetime import datetime
import time
import sys

# Function to calculate the MD5 hash of a file
def calculate_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except FileNotFoundError:
        return None

def add_server(server):
    # Add code to add server to the database
    pass  # Placeholder for the actual implementation


# Function to perform disk usage check
def check_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent

# Function to perform CPU load check
def check_cpu_load():
    cpu_load = os.getloadavg()[0]  # 1-minute CPU load
    return cpu_load

# Function to perform free memory check
def check_free_memory():
    mem = psutil.virtual_memory()
    free_mem_percent = (mem.available / mem.total) * 100
    return free_mem_percent

# Function to perform ping check
def ping_check(server):
    try:
        output = subprocess.check_output(["ping", "-c", "1", server]).decode()
        if "1 received" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Function to append data to CSV file
def append_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: monitor4.py <cmd> <options>")
        return

    command = sys.argv[1]
    options = sys.argv[2]

    if command == 'run':
        interval = int(options)
        while True:
            check_date = datetime.utcnow().isoformat()
            
            # File hash check
            # Perform file hash check for each file in the database
            # Assuming filepath is stored in a list named 'filepaths'
            for filepath in filepaths:
                old_hash = get_old_hash(filepath)  # Get old hash from database
                current_hash = calculate_file_hash(filepath)
                if old_hash == current_hash:
                    status = "OK"
                else:
                    status = "FAIL"
                message = f"FILE={filepath}, OLD_HASH={old_hash}, CURRENT_HASH={current_hash}"
                append_to_csv("monitor4.csv", [check_date, "filehash", status, message])

            # Ping check
            # Assuming server IPs are stored in a list named 'servers'
            for server in servers:
                if ping_check(server):
                    status = "OK"
                else:
                    status = "FAIL"
                message = f"SERVER={server}, TIME(MS)={ping_time(server)}"
                append_to_csv("monitor4.csv", [check_date, "ping", status, message])

            # Host CPU load check
            cpu_load = check_cpu_load()
            if cpu_load <= 2.00:
                cpu_status = "OK"
            else:
                cpu_status = "FAIL"
            cpu_message = f"CPU_LOAD={cpu_load}"
            append_to_csv("monitor4.csv", [check_date, "host-cpu", cpu_status, cpu_message])

            # Host disk usage check
            disk_usage = check_disk_usage()
            if disk_usage <= 85:
                disk_status = "OK"
            else:
                disk_status = "FAIL"
            disk_message = f"DISK_USED={disk_usage}%"
            append_to_csv("monitor4.csv", [check_date, "host-disk", disk_status, disk_message])

            # Host memory check
            free_memory = check_free_memory()
            if free_memory >= 25:
                mem_status = "OK"
            else:
                mem_status = "FAIL"
            mem_message = f"FREE_MEM={free_memory}%"
            append_to_csv("monitor4.csv", [check_date, "host-mem", mem_status, mem_message])

            time.sleep(interval)

    elif command == 'updatehash':
        filepath = options
        current_hash = calculate_file_hash(filepath)
        # Update hash in the database
        update_hash(filepath, current_hash)

    elif command == 'addserver':
        server = options
        # Add server to the database
        add_server(server)

    elif command == 'deleteserver':
        server = options
        # Delete server from the database
        delete_server(server)

    else:
        print("Invalid command")

if __name__ == "__main__":
    main()

