#!/usr/bin/env python3

import sys
import pymysql
import json
import csv

# Initial variables and imports
host = 'localhost'
user = 'cmdb'
password = 'Berouz1234!'
database = 'cmdb'
table = 'device_1'

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

# Function to retrieve data from the devices table
def retrieve_data(connection):
    try:
        with connection.cursor() as cursor:
            sql_query = f"SELECT * FROM {table}"
            cursor.execute(sql_query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error retrieving data from the database: {e}")
        sys.exit(1)

# Function to write data to a JSON file
def write_to_json(data):
    with open('database2.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

#Function to write data to a CSV file
def write_to_csv(data):
    if data:
        keys = data[0].keys()
        with open('database2.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print("Data written to database2.csv")
    else:
        print("No data retrieved from the database.")

# Main function
def main():
    # Check if correct number of arguments provided
    if len(sys.argv) != 2 or sys.argv[1] not in ['json', 'csv']:
        print("Usage: database2.py <json | csv>")
        sys.exit(1)

    # Connect to the database
    connection = connect_to_database()

    # Retrieve data from the devices table
    data = retrieve_data(connection)

    # Close the database connection
    connection.close()

    # Write data to either JSON or CSV file based on script argument
    if sys.argv[1] == 'json':
        write_to_json(data)
        print("Data written to database2.json")
    elif sys.argv[1] == 'csv':
        write_to_csv(data)
        print("Data written to database2.csv")

if __name__ == "__main__":
    main()

