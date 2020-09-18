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
        if len(sys.argv) < 3:
            print("\nSTATUS: ERROR! Username missing.\n")
            exit()
        elif len(sys.argv) > 4:
            print("\nSTATUS: ERROR! Please make sure there are no spaces in the username or password.\n")
            exit()
        else:
            if len(sys.argv) == 4:
                add_user(sys.argv[2], sys.argv[3])
            else:
                add_user(sys.argv[2], "EMPTY_STRING")

    elif sys.argv[1] == "Authenticate":
        if len(sys.argv) < 3:
            print("\nSTATUS: ERROR! Username missing.\n")
            exit()
        elif len(sys.argv) > 4:
            print("\nSTATUS: ERROR! Please make sure there are no spaces in the username or password.\n")
            exit()
        else:
            if len(sys.argv) == 4:
                authenticate(sys.argv[2], sys.argv[3])
            else:
                authenticate(sys.argv[2], "EMPTY_STRING")

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


# method used to add new Users
def add_user(username, password):
    if check_for_user(username):
        print("\nSTATUS: FAILURE! User already exists.\n")
    else:
        # user not found in the data, so now add the user
        if insert_new_user(username, password):
            print("\nSTATUS: SUCCESS! User added.\n")
        else:
            print("\nSTATUS: ERROR! Problems adding new user.\n")


# this method will get user data
def get_user_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))

    # look for UserData.txt file
    user_data = os.path.join(dir_name, "UserData" + "." + "txt")

    # list to be returned
    data_list = list()
    if os.path.exists(user_data):
        try:
            file = open("UserData.txt", "r")
            for line in file:
                for word in line.replace("\r", "").replace("\n", "").split():
                    data_list.append(word)
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()
        file.close()
        return data_list
    else:
        try:
            f = open("UserData.txt", "a+")
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()
            f.close()
            return data_list


# method to check whether the user has already been added
def check_for_user(username):
    data_list = get_user_data()
    if not data_list:
        # list is empty, so user is not found
        return False
    else:
        for x in range(0, len(data_list), 2):
            # user found in the data
            if (data_list[x]) == str(username):
                return True
        # user not found in the list
        return False


# method used to insert a new user into the UsersData
def insert_new_user(username, password):
    # insert new user into the list
    data_list = get_user_data()
    data_list.append(username)
    data_list.append(password)

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    user_data = os.path.join(dir_name, "UserData" + "." + "txt")
    os.remove(user_data)

    try:
        f = open("UserData.txt", "a+")
    except IOError:
        print("\nSTATUS: ERROR obtaining user data.\n")
        exit()

    for x in range(0, len(data_list), 2):
        f.write(str(data_list[x]))
        f.write("\t")
        f.write(str(data_list[x + 1]))
        f.write("\n")
    f.close()
    return True


# method used to add new Users
def authenticate(username, password):
    if check_for_user(username):
        if check_user_and_pass(username, password):
            print("\nSTATUS: SUCCESS! User authenticated.\n")
        else:
            print("\nSTATUS: FAILURE! Password incorrect.\n")

    else:
        print("\nSTATUS: FAILURE! User not found.\n")


# method used to check the username and password for a match
def check_user_and_pass(username, password):
    data_list = get_user_data()
    if not data_list:
        # list is empty
        return False
    else:
        for x in range(0, len(data_list), 2):
            # user found in the data, check if the password matches
            if (data_list[x]) == str(username) and (data_list[x+1]) == str(password):
                return True
        # matching username and password not in list
        return False


# runs the program by calling the main() method
if __name__ == "__main__":
    main()
