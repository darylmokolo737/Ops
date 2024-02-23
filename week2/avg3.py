#!/usr/bin/python3
### <THIS SCRIPT CALCULATES THE AVERAGE OF THREE POSITIVE NUMBERS>
### <DM-1152024>
#!/usr/bin/env python3

import sys


    #function that calculate input from a list of numbers input and calculate the sum.
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return round(average, 2)

def main():
    # here I Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: ./avg3.py <number1> <number2> <number3>")
        sys.exit(1)
  
    # Check if all arguments are positive numbers
    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
        if any(num < 0 for num in numbers):
            raise ValueError
    except ValueError:
        print("Error: All arguments must be positive numbers.")
        sys.exit(1)

    # Calculate and print the average
    average = calculate_average(numbers)
    print("The average of the numbers is:", average)

                                                                                                
if __name__ == "__main__":                                                                            main()
