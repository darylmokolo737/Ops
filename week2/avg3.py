#!/usr/bin/python3
### <THIS SCRIPT CALCULATES THE AVERAGE OF THREE POSITIVE NUMBERS>
### <DM-1152024>



import sys


# This script calculates the average of three positive numbers.

# Get input from the user (command line)
num1 = float(input("Enter the first positive number: "))
num2 = float(input("Enter the second positive number: "))
num3 = float(input("Enter the third positive number: "))

# Check if numbers are positive
if num1 <= 0 or num2 <= 0 or num3 <= 0:
    print("Error: Please enter positive numbers.")
else:
    # Calculate the average
    average = (num1 + num2 + num3) / 3

    # Print the average to two decimal places
    print(f"The average is: {average:.2f}")

