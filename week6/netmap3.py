#!/usr/bin/python3
### Script to perform a DNS scan on a domain using python3-nmap library.
### DM-1102024
import csv
import nmap3
import sys

# Set up initial variables and imports
OUTPUT_FILE = "netmap3.csv"

# Main routine that is called when the script is run
def main():
    """Main function to perform DNS scan on a domain."""
    if len(sys.argv) != 2:
        print("Usage: netmap3.py <domain>")
        sys.exit(1)
    

    DOMAIN = sys.argv[1]
    # Create Nmap object

    nmap = nmap3.Nmap()

    # Run DNS scan on the domain
    dns_results = nmap.nmap_dns_brute_script(DOMAIN)

    # Extract DNS names and IPs from scan results
    scan_results = extract_scan_results(dns_results)

    # Write scan results to CSV file
    write_to_csv(OUTPUT_FILE, scan_results)

def extract_scan_results(dns_results):
    """Extract DNS names and IPs from scan results."""
    scan_results = []

    # Loop through each scanned host
    for host in dns_results:
        # Ignore IPv6 entries
        if ':' in host['address']:
            continue
        # Get DNS name
        dns_name = host['hostname']
        # Get IP address
        ip_address = host['address']
        # Append DNS name and IP address to results list
        scan_results.append({'DNS': dns_name, 'IP': ip_address})

    return scan_results

def write_to_csv(output_filename, scan_results):
    """Write scan results to CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['DNS', 'IP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scan_results)

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

