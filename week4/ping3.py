#!/usr/bin/python3
import sys
import csv
from pinglib import pingthis  # Importing pingthis function from the pinglib module


def main():
    """Main function to be called when the script is run."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: ./ping3.py <filename | IP | Domainname> [output_filename]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None

    if not isfile(input_arg):
        results = [pingthis(input_arg)]
        print_results(results)
        if output_filename:
            write_to_csv(results, output_filename)
    else:
        with open(input_arg, 'r') as file:
            lines = file.readlines()
        
        results = []

        for line in lines:
            ipordns = line.strip()
            result = pingthis(ipordns)
            results.append(result)

            print_results(results)
            if output_filename:
                write_to_csv(results, output_filename)        

def isfile(path):
    """Check if the given path is a file."""
    try:
        with open(path, 'r') as file:
            return True
    except FileNotFoundError:
        return False


def print_results(results):
    """Print results to console."""
    print("IP, TimeToPing (ms)")
    for result in results:
        print(f"{result[0]}, {result[1]}")


def write_to_csv(results, output_filename):
    """Write results to a CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['IP', 'TimeToPing (ms)'])
        csv_writer.writerows(results)

# Run main() if the script is called directly
if __name__ == "__main__":
    main()
