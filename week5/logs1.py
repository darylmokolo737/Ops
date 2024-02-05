#!/usr/bin/python3
### Script to extract iPhone MAC addresses from dhcpd log file.
### DM-1102024
import re
import csv

# Set up initial variables and imports
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
    # Implement your regex or logic to extract iPhone MAC addresses
    mac_addresses = re.findall(r'(?:[0-9a-fA-F]:?){12}', log_data)
    iphone_macs = [mac.lower() for mac in mac_addresses if is_iphone(mac)]
    return iphone_macs

def is_iphone(mac_address):
    """Check if a MAC address belongs to an iPhone."""
    # Updated regular expression for iPhone MAC addresses
    iphone_mac_pattern = re.compile(r'^(?:[0-9a-fA-F]{2}[:.-]?){5}(?:[0-9a-fA-F]{2})$')

    return bool(iphone_mac_pattern.match(mac_address))


def write_output_file(output_filename, iphone_macs, unique_count):
    """Write iPhone MAC addresses and count to an output file."""
    with open(output_filename, 'w') as file:
        for mac in iphone_macs:
            file.write(f"{mac}\n")
        file.write(f"Count = {unique_count}\n")

    # Run main() if the script is called directly
if __name__ == "__main__":
    main()

