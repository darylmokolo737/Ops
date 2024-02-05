#!/usr/bin/python3
import subprocess
import sys
import re
import csv


def main():
    """Main function to be called when the script is run."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: ./ping3.py <filename | IP | Domainname> [output_filename]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    with open(input_arg, 'r') as file:
        lines = file.readlines()
        
        results = []

        for line in lines:
            ipordns = line.strip()
            result = pingthis(ipordns)
            results.append(result)
            print(f"{result[0]}, {result[1]}")

        if output_filename:
            write_to_csv(results, output_filename)

def pingthis(ipordns, max_attempts=3):
    """Function to ping the specified IP or domain name."""
    for _ in range(max_attempts):
        try:
           # Run ping command and capture output
            output = subprocess.check_output(['ping', '-c', '4', ipordns], text=True)
                                                                                                                                       # Use regex to extract time from output
            time_match = re.search(r'min/avg/max/stddev = \d+\.\d+/(\d+\.\d+)/\d+\.\d+/\d+\.\d+', output)

            if time_match:
                time_to_ping = round(float(time_match.group(1)), 2)
                return [ipordns, str(time_to_ping)]
            else:
                return [ipordns, 'Error: Unable to parse ping output.']

        except subprocess.CalledProcessError:
                                                                                                                                        # Retry if the ping fails
            continue

    return [ipordns, 'NotFound']          


def write_to_csv(results, output_filename):
    """Write results to a CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['IP', 'TimeToPing (ms)'])
        csv_writer.writerows(results)

# Run main() if the script is called directly
if __name__ == "__main__":
    main()
