#!/usr/bin/python3
### Script to extract iPhone MAC addresses from dhcpd log file.
### DM-2052024
import re
import sys

# # Global variables
LOG_FILE = sys.argv[1]
OUTPUT_FILE = "logs1.csv"


def main():
    """Main function to extract iPhone MAC addresses and count."""
    log_data = read_log_file(LOG_FILE)
    iphone_macs = extract_iphone_macs(log_data)
    unique_count = len(iphone_macs)

    write_output_file(OUTPUT_FILE, iphone_macs, unique_count)

def read_log_file(filename):
    """Read the contents of the DHCP log file."""
    with open(filename, 'r') as file:
        log_data = file.read()
    return log_data

def extract_iphone_macs(log_data):
    """Extract unique iPhone MAC addresses from the log data."""
    # Regex pattern for iPhone MAC addresses (complete MAC address)
    iphone_mac_pattern = re.compile(r'\b([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')

    # This help me find all matches in the log data
    iphone_macs = iphone_mac_pattern.findall(log_data)

    return list(set(iphone_macs))

def write_output_file(output_filename, iphone_macs, unique_count):
    """This will Write unique iPhone MAC addresses and count to an output file."""
    with open(output_filename, 'w') as file:
        for mac in iphone_macs:
            file.write(f"{mac}\n")
        file.write(f"Count = {unique_count}\n")

# Run main() if the script is called directly
if __name__ == "__main__":
    main()
