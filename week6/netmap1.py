#!/usr/bin/python3
### Script to perform a syn scan on a network subnet using python3-nmap library.
### DM-1102024
import csv
import nmap3
import sys

# Set up initial variables and imports
SUBNET = "152.157.64.0/24"
OUTPUT_FILE = "netmap1.csv"

# Main routine that is called when the script is run
def main():
    """Main function to perform syn scan on a network subnet."""
    # Create Nmap PortScanner object
    nm = nmap3.Nmap()

    # Perform syn scan on the subnet
    nm_scan_results = nm.nmap_list_scan(SUBNET)

    # Extract IP addresses and open ports from scan results
    scan_results = extract_scan_results(nm_scan_results)

    # Write scan results to CSV file
    write_to_csv(OUTPUT_FILE, scan_results)

def extract_scan_results(nm_scan_results):
    """Extract IP addresses and open ports from scan results."""
    scan_results = []

    # Loop through each scanned host
    for ip_address, scan_result in nm_scan_results.items():
        # Get open ports
        open_ports = ""
        # Check if 'ports' key exists and is not empty
        if 'ports' in scan_result and isinstance(scan_result['ports'], list):
        # Extract open ports from each port entry
            open_ports = ', '.join(str(port['portid']) for port in scan_result['ports'] if port['state']['state'] == 'open')
        
        scan_results.append({'IP': ip_address, 'Open Ports': open_ports})

    return scan_results

def write_to_csv(output_filename, scan_results):
    """Write scan results to CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Open Ports']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scan_results)
# Run main() if the script is called directly
if __name__ == "__main__":
    main()

