#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1302024
import sys
import os
from pinglib import pingthis  
    # Importing pingthis function from the pinglib module
    # this main routine will call when the script is run
def main():
    """Main function to be called when the script is run."""
    if len(sys.argv) != 2:
        print("Usage: ./ping2.py <filename | IP | Domainname>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        # If the argument is a file, read lines from the file
        try:
            with open(target, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{target}' not found.")
            sys.exit(1)

        print("IP, TimeToPing (ms)")

        for line in lines:
            ipordns = line.strip()
            result = pingthis(ipordns)
            print(f"{result[0]}, {result[1]}")
    else:
        # If the argument is not a file, assume it's an IP or Domainname
        print("IP, TimeToPing (ms)")
        result = pingthis(target)
        print(f"{result[0]}, {result[1]}")

if __name__ == "__main__":
    main()

