#!/usr/bin/python3
### Script to extract vendor information from MAC addresses in DHCP log file.
### DM-1102024
import requests
import re
import csv
import sys

# Set up initial variables and imports
IP_FILE = sys.argv[1]
LOG_FILE = sys.argv[2]
OUTPUT_CSV = "logs3.csv"
OUTPUT_IPS_TXT = "IPsForLogs3.txt"
API_URL = "https://api.macvendors.com/"

# Main routine that is called when the script is run
def main():
    """Main function to extract vendor information."""
    # Read the list of IPs from the file
    ips = read_ips_from_file(IP_FILE)

    # Process each IP and extract vendor information
    results = []
    for ip in ips:
        mac_address = extract_mac_address(ip)
        vendor = query_mac_vendor(mac_address)
        results.append({'IP': ip, 'Mac Address': mac_address, 'Vendor': vendor})

    # Write the results to logs3.csv
    write_csv_results(OUTPUT_CSV, results)

    # Write the processed IPs to IPsForLogs3.txt
    write_ips_to_file(OUTPUT_IPS_TXT, ips)

def read_ips_from_file(filename):
    """Read the list of IPs from the file."""
    with open(filename, 'r') as file:
        ips = [line.strip() for line in file]
    return ips


def extract_mac_address(ip):
    """Extract the MAC address associated with the given IP from the log file."""
    with open(LOG_FILE, 'r') as file:
        log_data = file.read()
    mac_address_match = re.search(rf'DHCPREQUEST for {re.escape(ip)}.*?from (\S+) via', log_data)
    if mac_address_match:
        return mac_address_match.group(1)
    else:
        return "Not Found"

def query_mac_vendor(mac_address):
    """Query the Mac Vendors API to obtain the vendor information for the given MAC address."""
    if mac_address == "Not Found":
        return "Unknown"
    else:
        response = requests.get(API_URL + mac_address)
        if response.status_code == 200:
            return response.text
        else:
            return "Error"

def write_csv_results(output_filename, results):
    """Write the results to a CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Mac Address', 'Vendor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def write_ips_to_file(output_filename, ips):
    """Write the processed IPs to a text file."""
    with open(output_filename, 'w') as file:
        for ip in ips:
            file.write(ip + '\n')

    # Run main() if the script is called directly
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: logs3.py <filename of IPs> <dhcpd log file>")
        sys.exit(1)
    main()

