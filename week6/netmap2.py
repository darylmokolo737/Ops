#!/usr/bin/python3
### Script to detect OS of machines found in netmap1.py using python3-nmap library.
### DM-1102024

import csv
import nmap3
import sys
# Set up initial variables and imports
OUTPUT_FILE = "netmap2.csv"

# Main routine that is called when the script is run
def main():
    """Main function to detect OS of machines found in netmap1.py."""
    if len(sys.argv) != 2:
        print("Usage: sudo ./netmap2.py <input file name>")
        sys.exit(1)

    INPUT_FILE = sys.argv[1]  # Input file name passed as command-line argument

    scan_results = read_input(INPUT_FILE)

    os_results = detect_os(scan_results)

    write_to_csv(OUTPUT_FILE, os_results)

def read_input(input_filename):
    """Read IP addresses and open ports from netmap1.csv."""
    results = []
    with open(input_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address = row['IP']
            open_ports = row['Open Ports']
            results.append({'IP': ip_address, 'Open Ports': open_ports})
    return results

def detect_os(scan_results):
    """Perform OS detection scan."""
    nm = nmap3.Nmap()
    os_results = []
    for result in scan_results:
        ip_address = result['IP']
        os_guess = ''  # Initialize best guess OS
        try:
            # Perform OS detection scan for each IP address with a timeout of 30 seconds
            os_scan_result = nm.nmap_os_detection(ip_address)
            if os_scan_result and 'osmatch' in os_scan_result and os_scan_result['osmatch']:
            # Get the most likely OS guess
                os_guess = os_scan_result['osmatch'][0]['name']
        except Exception as e:
            print(f"Error scanning {ip_address}: {e}")
            os_guess = 'Unknown'
        os_results.append({'IP': ip_address, 'Open Ports': result['Open Ports'], 'OS': os_guess})
    return os_results

def write_to_csv(output_filename, os_results):
    """Write scan results to CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Open Ports', 'OS']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(os_results)

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

