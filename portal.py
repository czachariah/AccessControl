"""
Access Control Program

CS419: Computer Security
Project 1

Author: Chris Zachariah (cvz2)
"""
import sys
import os


# main method for the program
def main():
    # make sure that the correct number of arguments are given
    if len(sys.argv) < 2:
        print("\nSTATUS: ERROR! Please include a command and the proper arguments.\n")
        exit()

    # make sure the command given is valid
    if sys.argv[1] == "AddUser":
        print("AddUser Command!")

    elif sys.argv[1] == "Authenticate":
        print("Authenticate Command!")

    elif sys.argv[1] == "SetDomain":
        print("SetDomain Command!")

    elif sys.argv[1] == "DomainInfo":
        print("DomainInfo Command!")

    elif sys.argv[1] == "SetType":
        print("SetType Command!")

    elif sys.argv[1] == "TypeInfo":
        print("TypeInfo Command!")

    elif sys.argv[1] == "AddAccess":
        print("AddAccess Command!")

    elif sys.argv[1] == "CanAccess":
        print("CanAccess Command!")

    else:
        print("\nSTATUS: ERROR! Please use a proper command.\n")
        exit()


# runs the program by calling the main() method
if __name__ == "__main__":
    main()

