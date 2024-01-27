#!/usr/bin/python3
### This script takes a birthdate and a number of days as command line arguments,
### then prints out the date when the person will reach that number of days.
### DM-1102024
import sys
from datetime import datetime, timedelta

  # Main routine that is called when the script is run
def main():
    """This function processes the command line arguments and prints the result."""
# Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: ./dates.py <birthdate> <days_to_add>")
        sys.exit(1)

# Get the birthdate and days to add from command line arguments
    birthdate_str = sys.argv[1]
    days_to_add_str = sys.argv[2]

# Check if the provided birthdate is a valid date
    if not is_valid_date(birthdate_str):
        print("Error: Invalid birthdate format. Use mm-dd-yyyy.")
        sys.exit(1)

# Check if the provided days_to_add is a positive integer
    if not days_to_add_str.isdigit() or int(days_to_add_str) <= 0:
        print("Error: Days to add must be a positive integer.")
        sys.exit(1)

# Convert birthdate string to a datetime object
    birthdate = datetime.strptime(birthdate_str, "%m-%d-%Y")
# Add the specified number of days to the birthdate
    result_date = birthdate + timedelta(days=int(days_to_add_str))

# Print the result
    print(f"Person born on {birthdate_str} will have their {days_to_add_str} birthday on {result_date.strftime('%m-%d-%Y')}.")

# Function to check if a date string is in the correct format
def is_valid_date(date_str):
    """This function checks if a date string is in the correct format."""
    try:
        datetime.strptime(date_str, "%m-%d-%Y")
        return True
    except ValueError:
        return False

# Run main() if the script is called directly
if __name__ == "__main__":
    main()
