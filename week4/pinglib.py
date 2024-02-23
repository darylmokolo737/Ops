#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1102024



import subprocess
import re

def pingthis(ipordns, max_attempts=3):
    """Function to ping the specified IP or domain name."""
    for _ in range(max_attempts):
        try:
            # this will run ping command and capture output
            output = subprocess.check_output(['ping', '-c', '4', ipordns], text=True)

            # Use regex to extract time from output
            time_match = re.search(r'min/avg/max/stddev = \d+\.\d+/(\d+\.\d+)/\d+\.\d+/\d+\.\d+', output)

            if time_match:
                time_to_ping = round(float(time_match.group(1)), 2)
                return [ipordns, str(time_to_ping)]
            else:
                return [ipordns, 'Error: Unable to parse ping output.']

        except subprocess.CalledProcessError:
            # Retry if the ping fails
            continue

    return [ipordns, 'NotFound']


