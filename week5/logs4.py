#!/usr/bin/python3
### Script to analyze mail log file for servers using internal mail server.
### DM-1102024
import re
import csv
import sys
from collections import defaultdict

# Set up initial variables and imports
MAIL_LOG_FILE = sys.argv[1]
OUTPUT_FILE = "servers.csv"

# Main routine that is called when the script is run
def main():
    """Main function to analyze mail log file."""
    log_data = read_log_file(MAIL_LOG_FILE)

    # Extract data for servers.csv
    servers_data = extract_servers_data(log_data)
    write_servers_csv(OUTPUT_FILE, servers_data)

def read_log_file(filename):
    """Read the contents of the mail log file."""
    with open(filename, 'r') as file:
        log_data = file.read()
    return log_data

def extract_servers_data(log_data):
    """Extract data for servers.csv."""
    server_ip_counts = defaultdict(set)
    log_lines = log_data.split('\n')

    for line in log_lines:
        # Use regex to extract server names and IPs
        # Adjust the regex pattern according to your mail log format
        match = re.search(r'from (\S+) \(.*?\[([0-9.]+)\]\)', line)
        if match:
            server_name = match.group(1)
            server_ip = match.group(2)
            server_ip_counts[server_name].add(server_ip)

    servers_data = [{'Server Name': server, 'IP': ', '.join(ips)}
                    for server, ips in server_ip_counts.items()]
    return servers_data

def write_servers_csv(output_filename, servers_data):
    """Write servers.csv file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Server Name', 'IP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(servers_data)

        # Run main() if the script is called directly
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: logs4.py mail.log")
        sys.exit(1)
    main()

