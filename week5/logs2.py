#!/usr/bin/python3
### Script to analyze DHCP log file for potential DOS attacks.
### DM-1102024

# Set up initial variables and imports
import sys
import re
import csv
mac_ip = {}

# Main routine that is called when script is run
def main():
  """Loops over a file and counts acks on unique ip-mac combinations"""
  if len(sys.argv) == 2:
    with open(sys.argv[1],'r',newline='') as fin:
      for line in fin:
        line = line.rstrip()
        m = re.search(".*DHCPACK (?:on (.*) to ((?:..\:){5}..)|\
                      to (.*) \((.*) via)",line)
        if m:
          ip = m.group(1)
          mac = m.group(2)
          macip = mac+'-'+ip
          if macip in mac_ip:
            mac_ip[macip] = mac_ip[macip] + 1
          else:
            mac_ip[macip] = 1
    # sort the mac_ip dict to make it easier to see the problems
    mac_ip_sorted = sorted(mac_ip.items(), key=lambda x:x[1])
    with open('logs2.csv','w',newline='') as fout:
      csvout = csv.writer(fout)
      csvout.writerow(['Mac address','IP address','Total number of acks'])
      for macip,count in mac_ip_sorted:
        (mac,ip) = macip.split('-')
        csvout.writerow([mac,ip,count])
    # write out the problemmac.csv file
    with open('ProblemMacs.csv','w',newline='') as fout:
      csvout = csv.writer(fout)
      csvout.writerow(['Mac address','IP address','Total number of acks'])
      with open('logs2.csv','r',newline='') as fin:
        csvin = csv.reader(fin)
        for row in csvin:
          if row[0] == 'Mac address':
            continue
          elif int(row[2]) > 35:
            csvout.writerow(row)

  else:
    usage()


# Subroutines
def usage():
  """How to use this script"""
  print('Usage: logs2.py filename')

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()
