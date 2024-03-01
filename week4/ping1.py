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
    # Print the header line before opening the file
    print("IP, TimeToPing (ms)")

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Iterate over each line in the file
        for line in lines:
            ipordns = line.strip()

            try:
                # Call the pingthis function and handle exceptions
                result = pingthis(ipordns)
                print(f"{result[0]}, {result[1]}")
            except Exception as e:
                print(f"{ipordns}, Error: {e}")

# Run main() if the script is called directly
if __name__ == "__main__":
    main()
