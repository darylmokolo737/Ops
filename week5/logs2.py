#!/usr/bin/python3
### Script to analyze DHCP log file for potential DOS attacks.
### DM-1102024
import re
import csv
import sys
from collections import defaultdict

# Set up initial variables and imports
LOG_FILE = "dhcpdsmall.log"
OUTPUT_FILE = "logs2.csv"
PROBLEM_MACS_FILE = "ProblemMacs.csv"

# Main routine that is called when the script is run
def main():
    """Main function to analyze DHCP log file."""
    log_data = read_log_file(LOG_FILE)

    # Extract data for logs2.csv
    logs_data = extract_logs_data(log_data)
    write_logs_csv(OUTPUT_FILE, logs_data)

    # Extract data for ProblemMacs.csv
    problem_macs_data = extract_problem_macs_data(log_data)
    write_problem_macs_csv(PROBLEM_MACS_FILE, problem_macs_data)

def read_log_file(filename):
    """Read the contents of the DHCP log file."""
    with open(filename, 'r') as file:
        log_data = file.read()
    return log_data

def extract_logs_data(log_data):
    """Extract data for logs2.csv."""
    mac_ip_ack_counts = defaultdict(int)
    log_lines = log_data.split('\n')

    for line in log_lines:
        if 'DHCPACK' in line:
            mac_address_match = re.search(r'from (\S+) via', line)
            ip_address_match = re.search(r'DHCPACK on (\S+) to', line)
            if mac_address_match and ip_address_match:
                mac_address = mac_address_match.group(1)
                ip_address = ip_address_match.group(1)
                mac_ip = f"{mac_address}-{ip_address}"
                mac_ip_ack_counts[mac_ip] += 1

    logs_data = [{'Macs': mac_ip.split('-')[0], 'IPs': mac_ip.split('-')[1], 'ACKs': acks}
                    for mac_ip, acks in mac_ip_ack_counts.items()]
    return logs_data

def write_logs_csv(output_filename, logs_data):
    """Write logs2.csv file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Macs', 'IPs', 'ACKs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs_data)

def extract_problem_macs_data(log_data):
    """Extract data for ProblemMacs.csv."""
    mac_ack_counts = defaultdict(int)
    log_lines = log_data.split('\n')

    for line in log_lines:
        if 'DHCPACK' in line:

            mac_address = re.search(r'from (\S+) via', line)
            if mac_address_match:
                mac_address = mac_address_match.group(1)
                mac_ack_counts[mac_address] += 1
    
    threshold = max(mac_ack_counts.values()) // 2
    problem_macs_data = [{'Macs': mac, 'ACKs': acks}
                         for mac, acks in mac_ack_counts.items() if acks > threshold]
    return problem_macs_data

def write_problem_macs_csv(output_filename, problem_macs_data):
    """Write ProblemMacs.csv file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Macs', 'ACKs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(problem_macs_data)

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

