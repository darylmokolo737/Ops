#!/usr/bin/python3
# Get information on the server and print to the screen
# Daryl -2024204: initial version

# Set up initial variables and imports
import socket
import psutil
import distro
import subprocess
import re

# Main routine that is called when script is run
def main():
  """Print out system information"""
  print('HostName = '+get_hostname())
  print('CPU (count): '+get_cpu_count())
  print('RAM (GB): '+get_ram())
  print('OSType: '+get_ostype())
  print('OSVersion: '+get_osversion())
  print('Disks (Count): '+get_disk_count())
  ip_mac = get_eth0_ip_mac()
  print('ip of eth0: '+ip_mac[0])
  print('mac of eth0: '+ip_mac[1])

def get_hostname():
  """Returns the hostname"""
  return(socket.gethostname())

def get_cpu_count():
  """Returns the cpu count"""
  return(str(psutil.cpu_count()))

def get_ram():
  """Returns the ram as GB"""
  ram = round((psutil.virtual_memory().total)/(1024*1024*1024),0)
  return(str(ram))

def get_ostype():
  """Returns the OS Type"""
  return(distro.name())

def get_osversion():
  """Returns the OS Version"""
  return(distro.version())

def get_disk_count():
  """Returns the number of disks"""
  proc = subprocess.run("lsblk | grep disk | wc -l", shell=True, \
          universal_newlines=True, capture_output=True, text=True)
  if proc.returncode == 0:
    res = proc.stdout.rstrip()
    return(res)
  else:
    exit('Error in subprocess.run to get disk count')

def get_eth0_ip_mac():
  """Returns of IP of eth0"""
  proc = subprocess.run("ip addr show eth0", shell=True, universal_newlines= \
          True, capture_output=True, text=True)
  if proc.returncode == 0:
    res = proc.stdout
    m = re.search('ether (.*) brd.*inet (.*)\/.. metric',res,re.DOTALL)
    if m:
      return([m.group(2),m.group(1)])
    else:
      return('No pattern match on Eth0')
  else: 
    exit('Error in subprocess.run to get IP')

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()

