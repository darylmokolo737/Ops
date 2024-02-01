#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1302024
import subprocess
import sys
import re
import os

    # this main routine will call when the script is run
def main():
    """Main function to be called when the script is run."""
    if len(sys.argv) != 2:
        print("Usage: ./ping2.py <filename | IP | Domainname>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        # If the argument is a file, read lines from the file
        with open(target, 'r') as file:
            lines = file.readlines()

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

def pingthis(ipordns, max_attempts=3):
    """Function to ping the specified IP or domain name."""
    for _ in range(max_attempts):
        try:
            # this will run ping command and capture output
            output = subprocess.check_output(['ping', '-c', '4', ipordns], text=True)

            # Use of the regex to extract time from output
            time_match = re.search(r'min/avg/max/stddev = \d+\.\d+/(\d+\.\d+)/\d+\.\d+/\d+\.\d+', output)

            if time_match:
                time_to_ping = round(float(time_match.group(1)), 2)
                return [ipordns, str(time_to_ping)]
            else:
                return [ipordns, 'Error: Unable to parse ping output.']

        except subprocess.CalledProcessError:
        # this will Retry if the ping fails
            continue

    return [ipordns, 'NotFound']                                                                                                                                                                                                                            # Run main() if the script is called directly
if __name__ == "__main__":
    main()

