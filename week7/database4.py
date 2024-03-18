#!/usr/bin/python3
### This script inserts server information into a MySQL database.
### DM-1192024

import platform
import psutil
import subprocess
import pymysql
import sys

# Initial variables and imports
host = 'localhost'
user = 'cmdb'
password = 'Berouz1234!'
database = 'cmdb'
table = 'device'

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

# Function to create the 'device' table if it doesn't exist
def create_device_table(connection):
    try:
        with connection.cursor() as cursor:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS device (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hostname VARCHAR(255),
                    cpu_count INT,
                    ram_gb FLOAT,
                    os_type VARCHAR(255),
                    os_version VARCHAR(255)
                )
            """
            cursor.execute(create_table_query)
            print("Device table created successfully.")
            connection.commit()
    except Exception as e:
        print(f"Error creating device table: {e}")
        connection.rollback()

# Function to insert server information into the database
def insert_server_info(connection):
    try:
        with connection.cursor() as cursor:
            # Get and format server information
            hostname = platform.node()
            cpu_count = psutil.cpu_count(logical=False)
            ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
            os_type = platform.system()
            os_version = platform.release()

            # Insert data into the device table
            sql_query = f"INSERT INTO {table} (hostname, cpu_count, ram_gb, os_type, os_version) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (hostname, cpu_count, ram_gb, os_type, os_version))

        # Commit the transaction
        connection.commit()
        print("Server information inserted successfully.")
    except Exception as e:
        print(f"Error inserting server information: {e}")
        connection.rollback()

# Main function
def main():
    # Connect to the database
    connection = connect_to_database()

    # Create the 'device' table if it doesn't exist
    create_device_table(connection)

    # Insert server information into the database
    insert_server_info(connection)

    # Close the database connection
    connection.close()

# Run main() if the script is called directly
if __name__ == "__main__":
    main()

