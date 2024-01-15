# Set up initial variables and imports
###< GLOBAL, INITIAL VARIABLES, AND IMPORTS (e.g. import sys)>
import sys


# Main routine that is called when script is run
def main():
    """ This function prompts the user for their name and favorite color. """
    #geting user input
    user_name = input("Hello, What is your name? :  ")
    #Call the sub1 function with username

    sub1(user_name)

    # Function to process user name and ask for favorite color

def sub1(name):

    """This function asks the user for their favorite color."""
    #Display a personalized message using the entered name
    print(f"Hello, {name}!")
    #Get user input of their favorite color

    favorite_color = input("what is your favorite color?")
    #Display a message with the provided favorite color

    print(f"Great choice! {favorite_color} is a fantastic color.")

    #run main() if the script is called directly

if __name__=="__main__":
    main()
