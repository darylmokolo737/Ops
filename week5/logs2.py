#!/usr/bin/python3
### Script to analyze DHCP log file for potential DOS attacks.
### DM-1102024

import re
import sys
from collections import defaultdict

# Global variables
LOG_FILE = sys.argv[1]
OUTPUT_FILE = "logs2.csv"

# Main routine
def main():
    """Main function to extract MAC addresses, IPs, and ACKs."""
    log_data = read_log_file(LOG_FILE)
    macs_ips_acks = extract_macs_ips_acks(log_data)
    write_output_file(OUTPUT_FILE, macs_ips_acks)

def read_log_file(filename):
    """Read the contents of the DHCP log file."""
    with open(filename, 'r') as file:
        log_data = file.read()
    return log_data

def extract_macs_ips_acks(log_data):
    """Extract MAC addresses, IPs, and ACKs from the log data."""
    # Regex pattern for MAC addresses, IPs, and ACKs
    pattern = re.compile(r'DHCPACK on (\S+) to (\S+)')

    # Initialize dictionary to store MACs, IPs, and ACKs
    macs_ips_acks = defaultdict(int)

    # Find all matches in the log data
    matches = pattern.findall(log_data)
    for match in matches:
        mac_address, ip_address = match
        key = f"{mac_address}-{ip_address}"
        macs_ips_acks[key] += 1

    return macs_ips_acks

def write_output_file(output_filename, macs_ips_acks):
    """Write MAC addresses, IPs, and ACKs to an output file."""
    with open(output_filename, 'w') as file:
        file.write("Macs, IPs, ACKs\n")
        for key, acks in macs_ips_acks.items():
            mac_address, ip_address = key.split('-')
            file.write(f"{mac_address}, {ip_address}, {acks}\n")

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

