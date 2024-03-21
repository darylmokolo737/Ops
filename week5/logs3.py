#!/usr/bin/python3
### Script to extract vendor information from MAC addresses in DHCP log file.
### DM-1102024
import requests
import re
import csv
import sys
import time

# Main routine that is called when script is run
def main():
  """Reads in IPs to check, looks up their mac, then used API to find vendor"""
  if len(sys.argv) != 3:
    usage()
  with open(sys.argv[1],'r',newline='') as fin:
    with open('logs3.csv','w',newline='') as fout:
      csvout = csv.writer(fout)
      csvout.writerow(['IP','Mac address','Vendor'])
      for line in fin:
        ip = line.rstrip()
        mac = find_mac(ip)
        vendor = find_vendor(mac)
        csvout.writerow([ip,mac,vendor])
        time.sleep(3)

def find_vendor(macaddress):
  url = 'https://api.macvendors.com/'+macaddress
  res = requests.get(url)
  if res.status_code == 200:
    return(res.text)

def find_mac(ipaddress):
  with open(sys.argv[2],'r',newline='') as fin:
    for line in fin:
      line = line.rstrip()
      regex = ipaddress+' from ((?:..\:){5}..)'
      m = re.search(regex,line)
      if m:
        mac = m.group(1)
        return(mac)

def usage():
  """How to use this script"""
  print('Usage: logs3.py filename')
  exit()

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()

