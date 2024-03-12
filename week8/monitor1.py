#!/usr/bin/python3
### This script will monitor and update file hashes in a MySQL database.
### DM-3122024

import os
import hashlib
import pymysql
import sys
from datetime import datetime

# MySQL database connection details
host = 'localhost'
user = 'cmdb'
password = 'Berouz1234!'
database = 'cmdb'
table = 'files'

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

# Function to create the files table if it doesn't exist
def create_files_table(connection):
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            if not result:
                # Create the table if it doesn't exist
                cursor.execute(f"CREATE TABLE {table} (timestamp VARCHAR(30), path VARCHAR(200), hash VARCHAR(50))")
                print("Files table created successfully.")
            else:
                print("Files table already exists.")
        connection.commit()
    except Exception as e:
        print(f"Error creating files table: {e}")
        connection.rollback()

# Function to generate MD5 hash of a file
def generate_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(4096):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        print(f"Error generating hash for file '{file_path}': {e}")
        return None

# Function to update or insert file information into the database
def update_file_info(connection, file_path, file_hash):
    try:
        with connection.cursor() as cursor:
            # Check if the file already exists in the database
            cursor.execute(f"SELECT * FROM {table} WHERE path=%s", (file_path,))
            result = cursor.fetchone()
            timestamp = datetime.utcnow().isoformat()
            if result:
                # Update the timestamp and hash if the file already exists
                cursor.execute(f"UPDATE {table} SET timestamp=%s, hash=%s WHERE path=%s", (timestamp, file_hash, file_path))
                print(f"File information updated: {file_path}")
            else:
                # Insert new file information if it doesn't exist
                cursor.execute(f"INSERT INTO {table} (timestamp, path, hash) VALUES (%s, %s, %s)", (timestamp, file_path, file_hash))
                print(f"New file information inserted: {file_path}")
        connection.commit()
    except Exception as e:
        print(f"Error updating file information: {e}")
        connection.rollback()

# Main function
def main():
    # Connect to the MySQL database
    connection = connect_to_database()

    # Create the files table if it doesn't exist
    create_files_table(connection)

    # List of file paths to monitor
    file_paths = [
        '/etc/hosts',
        '/etc/group',
        '/etc/passwd',
        '/etc/ssh/sshd_config',
        '/etc/environment',
        '~/testfile.txt'
    ]

    # Iterate over each file path
    for file_path in file_paths:
        # Expand the '~' in the file path
        file_path = os.path.expanduser(file_path)
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Generate MD5 hash of the file
            file_hash = generate_file_hash(file_path)
            if file_hash:
                # Update or insert file information into the database
                update_file_info(connection, file_path, file_hash)
        else:
            print(f"File not found: {file_path}")

    # Close the database connection
    connection.close()

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

