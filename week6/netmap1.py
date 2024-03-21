#!/usr/bin/python3
### Script to perform a syn scan on a network subnet using python3-nmap library.
### DM-1102024

# Set up The Global Variable
import nmap3
import csv
import sys

# Main routine that is called when script is run
def main():
    """Does an OS scan over a list of IPs from nmap1.py"""
    if len(sys.argv) != 2:
        usage()

    mynmap = nmap3.Nmap()
    # Output file
    with open('netmap2.csv', 'w', newline='') as fout:
        csvout = csv.writer(fout)
        csvout.writerow(['IP', 'Open Ports', 'OS Guess'])
        # Input file
        with open(sys.argv[1], 'r', newline='') as fin:
            csvin = csv.reader(fin)
            # for each ip, get the OS and write it out
            for row in csvin:
                if row[0] == 'IP':
                    continue
                result = mynmap.nmap_os_detection(row[0])
                if result[row[0]]['osmatch']:
                    os = result[row[0]]['osmatch'][0]['name']
                else:
                    os = 'Unknown'
                csvout.writerow([row[0], row[1], os])

def usage():
    print("Usage: sudo netmap2.py <inputfile>")
    sys.exit()

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
    main()

