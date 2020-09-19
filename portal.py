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
                add_user(sys.argv[2], "@#$EMPTY_STRING@#$")

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
                authenticate(sys.argv[2], "@#$EMPTY_STRING@#$")

    elif sys.argv[1] == "SetDomain":
        if len(sys.argv) < 3:
            print("\nSTATUS: ERROR! Username missing.\n")
            exit()
        elif len(sys.argv) > 4:
            print("\nSTATUS: ERROR! Please check the input and try again.\n")
            exit()
        elif len(sys.argv) == 3:
            print("\nSTATUS: ERROR! Missing domain.\n")
            exit()
        else:
            set_domain(sys.argv[2], sys.argv[3])

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
        print("\nSTATUS: ERROR! User already exists.\n")
    else:
        # user not found in the data, so now add the user
        if update_user_data(username, password):
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
            file.close()
            return data_list
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()
    else:
        try:
            f = open("UserData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()


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
def update_user_data(username, password):
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
        for x in range(0, len(data_list), 2):
            f.write(str(data_list[x]))
            f.write("\t")
            f.write(str(data_list[x + 1]))
            f.write("\n")
        f.close()
    except IOError:
        print("\nSTATUS: ERROR obtaining user data.\n")
        exit()
    return True


# method used to add new Users
def authenticate(username, password):
    if check_for_user(username):
        if check_user_and_pass(username, password):
            print("\nSTATUS: SUCCESS! User authenticated.\n")
        else:
            print("\nSTATUS: ERROR! Password incorrect.\n")

    else:
        print("\nSTATUS: ERROR! User not found.\n")


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


# method used to create new domains
def set_domain(username, domain):
    if check_for_user(username):
        data_list = get_domain_data()
        if not data_list:
            # there is no domain data, add first entry
            add_to_domain_data(username, domain, 1)
            print("\nSTATUS: SUCCESS! User added to domain.\n")
        else:
            # existing data, find domain or make new one
            if check_for_domain(domain):
                # user and domain exist
                # check if the user is already part of the domain
                # if true, do nothing and print SUCCESS
                # if false, add user and print SUCCESS
                if check_if_user_in_domain(username, domain):
                    print("\nSTATUS: SUCCESS! User added to domain.\n")
                else:
                    insert_user_into_domain(username, domain)
                    print("\nSTATUS: SUCCESS! User added to domain.\n")
            else:
                # there is no domain entry for, so update it
                add_to_domain_data(username, domain, 1)
                print("\nSTATUS: SUCCESS! User added to domain.\n")
    else:
        print("\nSTATUS: ERROR! User not found.\n")


# method that get domain data
def get_domain_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))

    # look for UserData.txt file
    domain_data = os.path.join(dir_name, "DomainData" + "." + "txt")

    # list to be returned
    data_list = list()
    if os.path.exists(domain_data):
        try:
            file = open("DomainData.txt", "r")
            for line in file:
                for word in line.replace("\r", "").replace("\n", "").split():
                    data_list.append(word)
            file.close()
            return data_list
        except IOError:
            print("\nSTATUS: ERROR obtaining domain data.\n")
            exit()
    else:
        try:
            f = open("DomainData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("\nSTATUS: ERROR obtaining domain data.\n")
            exit()


# method to add to the domain data (new entries)
def add_to_domain_data(username, domain, add_new):
    # insert new user into the list
    data_list = get_domain_data()

    # addNew = 1 = means new domain
    if add_new == 1:
        data_list.append(domain)
        data_list.append(str(1))
        data_list.append(username)

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    domain_data = os.path.join(dir_name, "DomainData" + "." + "txt")
    os.remove(domain_data)

    try:
        f = open("DomainData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the domain
            f.write("\t")
            x += 1
            f.write(data_list[x])  # writes in number of users in domain
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next user
                f.write("\n")
                x += 1
                i -= 1
            f.write("\n")
        f.close()
    except IOError:
        print("\nSTATUS: ERROR obtaining domain data.\n")
        exit()
    return True


# method to check if a domain exists
def check_for_domain(domain):
    data_list = get_domain_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == domain:
                return True
            x += 1
            x = x + int(data_list[x]) + 1
        return False


# method will check if a user is already part of a specific domain
def check_if_user_in_domain(username, domain):
    data_list = get_domain_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == domain:
                x += 1
                z = int(data_list[x])
                x += 1
                while z > 0:
                    if data_list[x] == username:
                        return True
                    z -= 1
                    x += 1
                return False
            x += 1
            x = x + int(data_list[x]) + 1
        return False


# this method will add users into a domain group
def insert_user_into_domain(username, domain):
    data_list = get_domain_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == domain:
                # change the number of users
                x += 1
                numb = int(data_list[x])
                data_list[x] = str(numb+1)

                # insert user
                x += 1
                data_list.insert(x, username)

                # update the file
                update_domain_data(data_list)
                return True

            x += 1
            x = x + int(data_list[x]) + 1
        return False


# method to update (after an insert) to the domain
def update_domain_data(data):
    # insert new user into the list
    data_list = data

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    domain_data = os.path.join(dir_name, "DomainData" + "." + "txt")
    os.remove(domain_data)

    try:
        f = open("DomainData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the domain
            f.write("\t")
            x += 1
            f.write(data_list[x])  # writes in number of users in domain
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next user
                f.write("\n")
                x += 1
                i -= 1
            f.write("\n")
        f.close()
    except IOError:
        print("\nSTATUS: ERROR obtaining domain data.\n")
        exit()
    return True


# runs the program by calling the main() method
if __name__ == "__main__":
    main()
