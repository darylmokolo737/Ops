#!/usr/bin/python3
### Script to extract iPhone MAC addresses from dhcpd log file.
### DM-2052024

# Set up initial variables and imports
import sys
import re
iphones = {}

# Main routine that is called when script is run
def main():
  """Loops over a file and counts unique iPhones"""
  if len(sys.argv) == 2:
    with open(sys.argv[1],'r',newline='') as fin:
      for line in fin:
        line = line.rstrip()
        m = re.search(".*DHCPACK.*to (.*) .*iPhone",line)
        if m:
          mac = m.group(1)
          iphones[mac] = 1
    for k,v in iphones.items():
      print(k)
    print('Count = '+str(len(iphones)))
  else:
    usage()

def usage():
  """How to use this script"""
  print('Usage: logs1.py filename')

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()

