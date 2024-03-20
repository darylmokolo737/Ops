#!/usr/bin/python3
### This script returns ll help me information about the machine it is running on.
### DM-1192024

import platform
import psutil
import subprocess

#!/usr/bin/python3
### This script returns ll help me information about the machine it is running on.
### DM-1192024

import platform
import psutil
import subprocess

def main():
    """This function retrieves and prints information about the server."""
    # Get and print hostname
    hostname = platform.node()
    print(f"Hostname: {hostname}")

    # Get and print CPU count
    cpu_count = psutil.cpu_count(logical=False)
    print(f"CPU (count): {cpu_count}")

    # Get and print RAM in GB
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    print(f"RAM (GB): {ram_gb}")

    # Get and print OS type and version
    os_type = platform.system()
    os_version = platform.release()
    print(f"OSType: {os_type}")
    print(f"OSVersion: {os_version}")

    # Get and print disk count using the lsblk command
    try:
        disk_count = int(subprocess.check_output(["lsblk", "-d", "-n", "-o", "NAME"]).decode().strip().count('\n')) 
        print(f"Disks (Count): {disk_count}")
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve disk information.")

    # This will Get and print IP and MAC address of eth0
    try:
        ip_eth0 = subprocess.check_output(["/bin/ip", "-4", "addr", "show", "eth0"]).decode("utf-8").split("inet ")[1].split("/")[0]
        mac_eth0 = subprocess.check_output(["/bin/cat", "/sys/class/net/eth0/address"]).decode("utf-8").strip()
        print(f"ip of eth0: {ip_eth0}")
        print(f"mac of eth0: {mac_eth0}")
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve network information.")


if __name__ == "__main__":
    main()

