#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1102024
import subprocess
import sys
import re

def main():
    """This Main function to be called when the script is run."""
    if len(sys.argv) != 2:
        print("Usage: ./pinglib.py <IP | Domainname>")
        sys.exit(1)

    ipordns = sys.argv[1]
    result = pingthis(ipordns)
    print(f"{result[0]}, {result[1]}")

def pingthis(ipordns):
    """Function to ping the specified IP or domain name."""
    try:
        # This will run ping command and capture output
        output = subprocess.check_output(['ping', '-c', '4', ipordns], text=True)
                                                                                    
        # I used regex to extract time from output
        time_match = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', output)

        if time_match:
            time_to_ping = round(float(time_match.group(1)), 2)
            return [ipordns, str(time_to_ping)]                                                                                     
        else:
            return [ipordns, 'Error: Unable to parse ping output.'] 
    except subprocess.CalledProcessError:
        return [ipordns, 'Error: Unable to ping the specified IP or domain name.']

       # finally this will run main() if the script is called directly
if __name__ == "__main__":
    main()

