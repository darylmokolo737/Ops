#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1302024
import sys
from pinglib import pingthis

# the main routine that is called when the script is run
def main():
    """Main function to be called when the script is run."""
    if len(sys.argv) != 2:
        print("Usage: ./ping1.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        lines = file.readlines()

    print("IP, TimeToPing (ms)")

    for line in lines:
        ipordns = line.strip()
        result = pingthis(ipordns)
        print(f"{result[0]}, {result[1]}")

        # Run main() if the script is called directly
if __name__ == "__main__":
    main()
