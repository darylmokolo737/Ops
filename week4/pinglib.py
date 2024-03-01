#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1102024

import subprocess

def pingthis(ipordns):
    try:
        # this will run ping command and capture output
        result = subprocess.run(['ping', '-c', '1', ipordns], capture_output=True, text=True, timeout=5)
        # Parse the output to extract the ping time
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'time=' in line:  # Find the line containing 'time='
                    time_to_ping = line.split('time=')[-1].split(' ')[0]
                    return ipordns, time_to_ping
            return ipordns, "NotFound"  # If 'time=' not found, return None
        else:
            raise Exception(f"Unable to ping {ipordns}")
    except subprocess.TimeoutExpired:
        return ipordns, "NotFound"
    except Exception as e:
        return ipordns, str(e)


