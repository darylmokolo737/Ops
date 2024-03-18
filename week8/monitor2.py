#!/usr/bin/env python3

import os
import sys
import time
import hashlib
import csv
from datetime import datetime
import pymysql

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'cmdb'
DB_PASSWORD = 'Berouz1234!'
DB_NAME = 'cmdb'

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

# Function to read file paths from the database
def get_file_paths(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT path FROM files")
            result = cursor.fetchall()
            return [row['path'] for row in result]
    except Exception as e:
        print(f"Error reading file paths from the database: {e}")
        sys.exit(1)

# Function to calculate MD5 hash of a file
def calculate_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating MD5 hash for {file_path}: {e}")
        return None

# Function to write results to CSV file
def write_to_csv(results):
    try:
        with open('monitor2.csv', 'a', newline='') as csvfile:
            fieldnames = ['check date', 'check type', 'status', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for result in results:
                writer.writerow(result)
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Function to monitor files for changes
def monitor_files(run_interval):
    connection = connect_to_database()
    file_paths = get_file_paths(connection)
    
    while True:
        results = []
        for file_path in file_paths:
            old_hash = None
            new_hash = calculate_md5(file_path)
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT hash FROM files WHERE path=%s", (file_path,))
                    result = cursor.fetchone()
                    if result:
                        old_hash = result['hash']
            except Exception as e:
                print(f"Error reading hash from the database: {e}")

            if old_hash is None:
                status = "OK"
                message = f"FILE={file_path}, CURRENT_HASH={new_hash}"
            elif old_hash == new_hash:
                status = "OK"
                message = f"FILE={file_path}, OLD_HASH={old_hash}, CURRENT_HASH={new_hash}"
            else:
                status = "File Changed"
                message = f"FILE={file_path}, OLD_HASH={old_hash}, CURRENT_HASH={new_hash}"
            
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            result = {'check date': timestamp, 'check type': 'filehash', 'status': status, 'message': message}
            results.append(result)
        
        write_to_csv(results)
        time.sleep(run_interval)

# Main function
def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ['run', 'updatehash']:
        print("Usage: ./monitor2.py <cmd> <options>")
        print("<cmd> is 'run' or 'updatehash'")
        print("<options> is number of seconds between runs or filepath")
        sys.exit(1)
    
    if sys.argv[1] == 'run':
        try:
            run_interval = int(sys.argv[2])
            monitor_files(run_interval)
        except ValueError:
            print("Invalid interval value. Please provide a valid integer value for seconds.")
            sys.exit(1)
    
    elif sys.argv[1] == 'updatehash':
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)
            
        file_hash = calculate_md5(file_path)
        if file_hash:
            connection = connect_to_database()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("REPLACE INTO files (path, hash) VALUES (%s, %s)", (file_path, file_hash))
                connection.commit()
                print(f"Hash for {file_path} updated successfully.")
                
                # Append the result to the CSV file
                with open('monitor2.csv', 'a') as f:
                    check_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    check_type = 'filehash'
                    status = 'OK'
                    message = f"FILE={file_path}, HASH={file_hash}"
                    csv_line = f"{check_date}, {check_type}, {status}, {message}\n"
                    f.write(csv_line)
            except Exception as e:
                print(f"Error updating hash for {file_path}: {e}")
        else:
            print(f"Failed to calculate hash for {file_path}.")

if __name__ == "__main__":
    main()


