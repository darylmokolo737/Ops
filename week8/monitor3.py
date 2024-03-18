#!/usr/bin/python3
### Reading/writing to/from a database
### DM-3132024
# monitor3.py

import csv
import os
import subprocess
import sys
from datetime import datetime
import pymysql
from pinglib import ping

# MySQL database connection details
DB_HOST = 'localhost'
DB_USER = 'cmdb'
DB_PASSWORD = 'Berouz1234!'
DB_NAME = 'cmdb'

# Function to connect to MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

# Function to add a server to the 'servers' table
def add_server_to_database(server):
    try:
        connection = connect_to_database()
        with connection.cursor() as cursor:
            sql = "INSERT INTO servers (DNSorIP) VALUES (%s)"
            cursor.execute(sql, (server,))
        connection.commit()
        print(f"Server {server} added successfully.")
    except Exception as e:
        print(f"Error adding server to the database: {e}")
    finally:
        connection.close()

# Function to delete a server from the 'servers' table
def delete_server_from_database(server):
    try:
        connection = connect_to_database()
        with connection.cursor() as cursor:
            sql = "DELETE FROM servers WHERE DNSorIP = %s"
            cursor.execute(sql, (server,))
        connection.commit()
        print(f"Server {server} deleted successfully.")
    except Exception as e:
        print(f"Error deleting server from the database: {e}")
    finally:
        connection.close()

# Function to run checks and write results to CSV
def run_checks(interval):
    while True:
        try:
            # Perform file hash checks
            perform_file_checks()

            # Perform ping checks for servers
            perform_ping_checks()

            # Sleep for the specified interval
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

# Function to perform file hash checks
def perform_file_checks():
    # Add code to perform file hash checks here
    pass

# Function to perform ping checks for servers
def perform_ping_checks():
    # Add code to perform ping checks here
    pass

# Main function
def main():
    if len(sys.argv) < 3:
        print("Usage: ./monitor3.py <cmd> <options>")
        sys.exit(1)

    cmd = sys.argv[1]
    options = sys.argv[2:]

    if cmd == 'addserver':
        for server in options:
            add_server_to_database(server)
    elif cmd == 'deleteserver':
        for server in options:
            delete_server_from_database(server)
    elif cmd == 'run':
        interval = int(options[0])
        run_checks(interval)
    elif cmd == 'updatehash':
        filepath = options[0]
        update_hash(filepath)
    else:
        print("Invalid command.")
        sys.exit(1)

if __name__ == "__main__":
    main()

