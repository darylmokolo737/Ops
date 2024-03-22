#!/usr/bin/python3
### This script returns information about the machine it is running on.
### DM-1102024

# Global variables and imports
import sys
import subprocess
import re


# Main routine that is called when script is run
def main():
  """Gets data from the cli, pings it, and prints out results"""
  if len(sys.argv) == 2:
    (ip,ms) = pingthis(sys.argv[1])
    print('IP, TimeToPing(ms)')
    print(ip+','+ms)


def usage(message):
  """What does this function do"""
  print('Usage: pinglib.py [IP|DNS]')

def pingthis(ip_dns):
  """Ping and IP or DNS name and return the IP and milliseconds in a list"""
  cmd = 'ping -c 1 -W 2 ' + ip_dns
  proc = subprocess.run(cmd, shell=True, universal_newlines=True, \
          capture_output=True, text=True)
  if proc.returncode == 0:
    res = proc.stdout
    m = re.search('PING (.*) \((.*)\) 56.*time=(.*) ms.*ping',res,re.DOTALL)
    if m:
      ip = m.group(1)
      ms = m.group(3)
      return([ip,ms])
    else:
      exit('Error in pattern match')
  else:
    if proc.stderr:
      exit('Error in subprocess: '+proc.stderr)
    else: return([ip_dns,'Not Found'])


# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()
