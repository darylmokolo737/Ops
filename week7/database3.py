#!/usr/bin/python3
### Script to perform a syn scan on a network subnet using python3-nmap library.
### DM-1102024

import pymysql
import serverinfo1

# Initial variables and imports
host = 'localhost'
user = 'cmdb'
password = 'Berouz1234!'
database = 'cmdb'
table = 'device'

# Main routine that is called when script is run
def main():
    """Add system information to database"""
    # Get the server information
    info = get_server_info()

    # Connect to the database
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()

    # Prepare SQL statement
    sql = "INSERT INTO device (name, macaddress, ip, cpucount, disks, ram, ostype, osversion) \
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute SQL statement
    try:
        cursor.execute(sql, (info["Hostname"], info["MAC Addr"], info["IP Addr"], \
                             info["CPU (count)"], info["Disks (Count)"], info["RAM (GB)"], \
                             info["OSType"], info["OSVersion"]))
        db.commit()
        print("Inserted server information into database successfully!")
    except Exception as e:
        db.rollback()
        print("Error inserting server information into database:", e)
    finally:
        db.close()

# Function to get server information using serverinfo1.py
def get_server_info():
    """Use serverinfo1 as a library to get system information"""
    sinfo = {}
    sinfo['Hostname'] = serverinfo1.get_hostname()
    sinfo['CPU (count)'] = serverinfo1.get_cpu_count()
    sinfo["RAM (GB)"] = serverinfo1.get_ram()
    sinfo["OSType"] = serverinfo1.get_ostype()
    sinfo["OSVersion"] = serverinfo1.get_osversion()
    sinfo["Disks (Count)"] = serverinfo1.get_disk_count()
    ip, mac = serverinfo1.get_eth0_ip_mac()
    sinfo["IP Addr"] = ip
    sinfo["MAC Addr"] = mac
    return sinfo

# Run main() if script called directly
if __name__ == "__main__":
    main()

