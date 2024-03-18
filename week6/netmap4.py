#!/usr/bin/python3
### Script to discover the geographic locations of a company's devices using python3-nmap library and IP-API.
### DM-1102024

import csv
import requests
import sys

# Function to get location data from IP-API
def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: netmap4.py <input_file_name>")
        return

    input_file = sys.argv[1]
    output_file = "netmap4.csv"

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['DNS', 'IP', 'Services', 'Country', 'RegionName', 'City', 'Zipcode', 'ISP'])
        writer.writeheader()

        for row in reader:
            ip = row['IP']
            location_data = get_location(ip)
            if location_data:
                writer.writerow({
                    'DNS': row['DNS'],
                    'IP': row['IP'],
                    'Services': row.get('Services', ''),
                    'Country': location_data.get('country', ''),
                    'RegionName': location_data.get('regionName', ''),
                    'City': location_data.get('city', ''),
                    'Zipcode': location_data.get('zip', ''),
                    'ISP': location_data.get('isp', '')
                })
            else:
                writer.writerow({
                    'DNS': row('DNS', ''),
                    'IP': row.get('IP', ''),
                    'Services': row.get('Services', ''),
                    'Country': '',
                    'RegionName': '',
                    'City': '',
                    'Zipcode': '',
                    'ISP': ''
                })         

if __name__ == "__main__":
    main()

