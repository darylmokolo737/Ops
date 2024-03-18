#!/usr/bin/python3
### Script to extract iPhone MAC addresses from dhcpd log file.
### DM-2052024
import re

# this will set up initial variables and imports
# < GLOBAL, INITIAL VARIABLES, AND IMPORTS (e.g., import sys) >
LOG_FILE = "dhcpdsmall.log"
OUTPUT_FILE = "logs1.txt"

# Main routine that is called when the script is run
def main():
    """Main function to extract iPhone MAC addresses and count."""
    log_data = read_log_file(LOG_FILE)
    iphone_macs = extract_iphone_macs(log_data)
    unique_count = len(set(iphone_macs))

    write_output_file(OUTPUT_FILE, iphone_macs, unique_count)

def read_log_file(filename):
    """Read the contents of the DHCP log file."""
    with open(filename, 'r') as file:
        log_data = file.read()
    return log_data

def extract_iphone_macs(log_data):
    """Extract iPhone MAC addresses from the log data."""
    # Regex pattern for iPhone MAC addresses
    iphone_mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b')

    # Find all matches in the log data
    iphone_macs = iphone_mac_pattern.findall(log_data)

    return iphone_macs

def write_output_file(output_filename, iphone_macs, unique_count):
    """Write iPhone MAC addresses and count to an output file."""
    with open(output_filename, 'w') as file:
        for mac in iphone_macs:
            file.write(f"{mac}\n")
        file.write(f"Count = {unique_count}\n")

    # Run main() if the script is called directly
if __name__ == "__main__":
    main()

