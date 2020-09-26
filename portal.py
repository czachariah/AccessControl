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
        print("Error: Please include a command and the proper arguments.")
        exit()

    # make sure the command given is valid
    if sys.argv[1] == "AddUser":
        if len(sys.argv) <= 3:
            print("Error: Missing arguments.")
            exit()
        elif len(sys.argv) > 4:
            print("Error: Too many arguments given.")
            exit()
        else:
            if sys.argv[2] == "":
                print("Error: Username cannot be empty.")
                exit()

            if sys.argv[3] == "":
                add_user(sys.argv[2], "@#$EMPTY_STRING@#$")
            else:
                add_user(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "Authenticate":
        if len(sys.argv) <= 3:
            print("Error: Missing arguments.")
            exit()
        elif len(sys.argv) > 4:
            print("Error: Too many arguments given.")
            exit()
        else:
            if sys.argv[2] == "":
                print("Error: Username cannot be empty.")
                exit()

            if sys.argv[3] == "":
                authenticate(sys.argv[2], "@#$EMPTY_STRING@#$")
            else:
                authenticate(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "SetDomain":
        if len(sys.argv) <= 3:
            print("Error: Missing arguments.")
            exit()
        elif len(sys.argv) > 4:
            print("Error: Too many arguments given.")
            exit()
        else:
            if sys.argv[2] == "":
                print("Error: Username is empty.")
                exit()
            elif sys.argv[3] == "":
                print("Error: Domain name is empty.")
                exit()
            else:
                set_domain(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "DomainInfo":
        if len(sys.argv) <= 2:
            print("Error: Missing arguments.")
            exit()
        elif len(sys.argv) > 3:
            print("Error: Too many arguments given.")
        else:
            if sys.argv[2] == "":
                print("Error: Domain name is empty.")
                exit()
            else:
                get_domain_users(sys.argv[2])

    elif sys.argv[1] == "SetType":
        if len(sys.argv) <= 3:
            print("Error: Arguments missing.")
            exit()
        elif len(sys.argv) > 4:
            print("Error: Too many arguments given.")
            exit()
        else:
            if sys.argv[2] == "":
                print("Error: Object name is empty.")
                exit()
            if sys.argv[3] == "":
                print("Error: Type name is empty.")
                exit()
            set_type(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "TypeInfo":
        if len(sys.argv) < 3:
            print("Error: Arguments missing.")
            exit()
        elif len(sys.argv) > 3:
            print("Error: Too many arguments given.")
        else:
            if sys.argv[2] == "":
                print("Error: Type name is empty")
                exit()
            get_type_objects(sys.argv[2])

    elif sys.argv[1] == "AddAccess":
        if len(sys.argv) <= 4:
            print("Error: Arguments missing.")
            exit()
        elif len(sys.argv) > 5:
            print("Error: Too many arguments given.")
            exit()
        else:
            if sys.argv[2] == "":
                print("Error: Operation name is empty.")
                exit()
            if sys.argv[3] == "":
                print("Error: Domain name is empty.")
                exit()
            if sys.argv[4] == "":
                print("Error: Type name is empty.")
                exit()
            add_access(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "CanAccess":
        print("CanAccess Command!")

    else:
        print("Error: Please use a proper command.")
        exit()


# method used to add new users
def add_user(username, password):
    if does_user_exist(username):
        print("Error: User already exists.")
    else:
        # user not found in the data, so now add the user
        if update_user_data(username, password):
            print("Success")
        else:
            print("Error: Problems adding new user.")


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
                line = line.split("\n")[0]
                data_list.append(line)
            file.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining user data.")
            exit()
    else:
        try:
            f = open("UserData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining user data.")
            exit()


# method to check whether the user has already been added
def does_user_exist(username):
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
            f.write("\n")
            f.write(str(data_list[x + 1]))
            f.write("\n")
        f.close()
    except IOError:
        print("Error: Problems obtaining user data.")
        exit()
    return True


# method used to authenticate users
def authenticate(username, password):
    if does_user_exist(username):
        if check_user_and_pass(username, password):
            print("Success")
        else:
            print("Error: Password incorrect.")

    else:
        print("Error: User not found.")


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
    if does_user_exist(username):
        data_list = get_domain_data()
        if not data_list:
            # there is no domain data, add first entry
            add_new_domain(username, domain)
            print("Success")
        else:
            # existing data, find domain or make new one
            if does_domain_exist(domain):
                # user and domain exist
                if check_if_user_in_domain(username, domain):
                    print("Success")
                else:
                    insert_user_into_domain(username, domain)
                    print("Success")
            else:
                # there is no domain entry for, so update it
                add_new_domain(username, domain)
                print("Success")
    else:
        print("Error: User not found.")


# method that get domain data
def get_domain_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))

    # look for DomainData.txt file
    domain_data = os.path.join(dir_name, "DomainData" + "." + "txt")

    # list to be returned
    data_list = list()
    if os.path.exists(domain_data):
        try:
            file = open("DomainData.txt", "r")
            for line in file:
                line = line.split("\n")[0]
                data_list.append(line)
            file.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining domain data.")
            exit()
    else:
        try:
            f = open("DomainData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining domain data.")
            exit()


# method to add new domain entries
def add_new_domain(username, domain):
    # insert new user into the list
    data_list = get_domain_data()

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
            f.write("\n")
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
        f.close()
    except IOError:
        print("Error: Problems obtaining domain data.")
        exit()
    return True


# method to check if a domain exists
def does_domain_exist(domain):
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


# this method will add users into an existing domain group
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


# method to update the domain info in file once a new user is added
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
            f.write("\n")
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
        f.close()
    except IOError:
        print("Error: Problems obtaining domain data.")
        exit()
    return True


# method used to get all the users of a specific domain
def get_domain_users(domain):
    if does_domain_exist(domain):
        print_users_in_domain(domain)


# method to print out all the users in a specific domain
def print_users_in_domain(domain):
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
                    print(data_list[x])
                    z -= 1
                    x += 1
                return
            x += 1
            x = x + int(data_list[x]) + 1


# method will be used in order set objects to types
def set_type(object_name, type_name):
    data_list = get_type_data()
    if not data_list:
        # there is no domain data, add first entry
        add_new_type(object_name, type_name)
        print("Success")
    else:
        # existing data, find domain or make new one
        if does_type_exist(type_name):
            # type exists
            if check_if_object_in_type(object_name, type_name):
                print("Success")
            else:
                insert_object_into_type(object_name, type_name)
                print("Success")
        else:
            # there is no type entry, so add it
            add_new_type(object_name, type_name)
            print("Success")


# method will be used in order to get data about Types
def get_type_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))

    # look for TypeData.txt file
    type_data = os.path.join(dir_name, "TypeData" + "." + "txt")

    # list to be returned
    data_list = list()
    if os.path.exists(type_data):
        try:
            file = open("TypeData.txt", "r")
            for line in file:
                line = line.split("\n")[0]
                data_list.append(line)
            file.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining type data.")
            exit()
    else:
        try:
            f = open("TypeData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining type data.")
            exit()


# method to add a type to the type data
def add_new_type(object_name, type_name):
    # insert new user into the list
    data_list = get_type_data()

    data_list.append(type_name)
    data_list.append(str(1))
    data_list.append(object_name)

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    type_data = os.path.join(dir_name, "TypeData" + "." + "txt")
    os.remove(type_data)

    try:
        f = open("TypeData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the type
            f.write("\n")
            x += 1
            f.write(data_list[x])  # writes in number of objects in type
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next object
                f.write("\n")
                x += 1
                i -= 1
        f.close()
    except IOError:
        print("Error: Problems obtaining type data.")
        exit()
    return True


# method will check if a specific type already exists
def does_type_exist(type_name):
    data_list = get_type_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == type_name:
                return True
            x += 1
            x = x + int(data_list[x]) + 1
        return False


# method will check if an object is already part of a type
def check_if_object_in_type(object_name, type_name):
    data_list = get_type_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == type_name:
                x += 1
                z = int(data_list[x])
                x += 1
                while z > 0:
                    if data_list[x] == object_name:
                        return True
                    z -= 1
                    x += 1
                return False
            x += 1
            x = x + int(data_list[x]) + 1
        return False


# method will add new objects to an existing type
def insert_object_into_type(object_name, type_name):
    data_list = get_type_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == type_name:
                # change the number of object
                x += 1
                numb = int(data_list[x])
                data_list[x] = str(numb + 1)

                # insert object
                x += 1
                data_list.insert(x, object_name)

                # update the file
                update_type_data(data_list)
                return True

            x += 1
            x = x + int(data_list[x]) + 1
        return False


# method to update the type info in file once a new object is added
def update_type_data(data):
    # insert new user into the list
    data_list = data

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    type_data = os.path.join(dir_name, "TypeData" + "." + "txt")
    os.remove(type_data)

    try:
        f = open("TypeData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the type
            f.write("\n")
            x += 1
            f.write(data_list[x])  # writes in number of object in type
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next object
                f.write("\n")
                x += 1
                i -= 1
        f.close()
    except IOError:
        print("Error: Problems obtaining type data.")
        exit()
    return True


# method used to get all the objects of a specific type
def get_type_objects(type_name):
    if does_type_exist(type_name):
        print_objects_in_type(type_name)


# method to print out all the objects in a specific type
def print_objects_in_type(type_name):
    data_list = get_type_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == type_name:
                x += 1
                z = int(data_list[x])
                x += 1
                while z > 0:
                    print(data_list[x])
                    z -= 1
                    x += 1
                return
            x += 1
            x = x + int(data_list[x]) + 1


# method to add an access right
def add_access(op_name, domain_name, type_name):
    if not does_domain_exist(domain_name):
        add_new_empty_domain(domain_name)
    if not does_type_exist(type_name):
        add_new_empty_type(type_name)
    set_access_right(op_name, domain_name, type_name)


# method will set the access correctly in the data
def set_access_right(op_name, domain_name, type_name):
    if does_operation_exist(op_name):
        if op_has_dom_and_type_already(op_name, domain_name, type_name):
            print("Success")
        else:
            add_to_existing_operation(op_name, domain_name, type_name)
            print("Success")
    else:
        add_new_operation(op_name, domain_name, type_name)
        print("Success")


# method checks if a specific operation already exists
def does_operation_exist(op_name):
    data_list = get_access_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == op_name:
                return True
            x += 1
            x = x + (2*(int(data_list[x]))) + 1
        return False


# method will add a new operation
def add_new_operation(op_name, domain_name, type_name):
    # insert new user into the list
    data_list = get_access_data()

    data_list.append(op_name)
    data_list.append(str(1))
    data_list.append(domain_name)
    data_list.append(type_name)

    update_access_data(data_list)


# method will add domain and type to an existing operation
def add_to_existing_operation(op_name, domain_name, type_name):
    data_list = get_access_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == op_name:
                # change the number of object
                x += 1
                numb = int(data_list[x])
                data_list[x] = str(numb + 1)

                # insert object
                x += 1
                data_list.insert(x, type_name)
                data_list.insert(x, domain_name)

                # update the file
                update_access_data(data_list)
                return True

            x += 1
            x = x + 2*(int(data_list[x])) + 1
        return False


# method will update the operation data
def update_access_data(access_data):
    data_list = access_data

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    access_data = os.path.join(dir_name, "AccessData" + "." + "txt")
    os.remove(access_data)

    try:
        f = open("AccessData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the operation
            f.write("\n")
            x += 1
            f.write(data_list[x])  # writes in number of groups for that operation (group = domain + type)
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next object
                f.write("\n")
                x += 1
                f.write(str(data_list[x]))  # writes in the next object
                f.write("\n")
                x += 1
                i -= 1
        f.close()
    except IOError:
        print("Error: Problems obtaining access data.")
        exit()
    return True


# method will get the current access data
def get_access_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))

    # look for TypeData.txt file
    access_data = os.path.join(dir_name, "AccessData" + "." + "txt")

    # list to be returned
    data_list = list()
    if os.path.exists(access_data):
        try:
            file = open("AccessData.txt", "r")
            for line in file:
                line = line.split("\n")[0]
                data_list.append(line)
            file.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining access data.")
            exit()
    else:
        try:
            f = open("AccessData.txt", "a+")
            f.close()
            return data_list
        except IOError:
            print("Error: Problems obtaining access data.")
            exit()


# method will make a new empty domain
def add_new_empty_domain(domain_name):
    data_list = get_domain_data()

    data_list.append(domain_name)
    data_list.append(str(0))

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    domain_data = os.path.join(dir_name, "DomainData" + "." + "txt")
    os.remove(domain_data)

    try:
        f = open("DomainData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the domain
            f.write("\n")
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
        f.close()
    except IOError:
        print("Error: Problems obtaining domain data.")
        exit()
    return True


# method will make a new empty type
def add_new_empty_type(type_name):
    # insert new user into the list
    data_list = get_type_data()

    data_list.append(type_name)
    data_list.append(str(0))

    # remove the current file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    type_data = os.path.join(dir_name, "TypeData" + "." + "txt")
    os.remove(type_data)

    try:
        f = open("TypeData.txt", "a+")
        x = 0
        while x < len(data_list):
            f.write(str(data_list[x]))  # writes in the type
            f.write("\n")
            x += 1
            f.write(data_list[x])  # writes in number of objects in type
            f.write("\n")
            i = int(data_list[x])
            x += 1
            while i > 0:
                f.write(str(data_list[x]))  # writes in the next object
                f.write("\n")
                x += 1
                i -= 1
        f.close()
    except IOError:
        print("Error: Problems obtaining type data.")
        exit()
    return True


# method checks if the domain and type pair already has the operation
def op_has_dom_and_type_already(op_name, dom_name, type_name):
    data_list = get_access_data()
    if not data_list:
        # data empty
        return False
    else:
        # look through data
        x = 0
        while x < len(data_list):
            if data_list[x] == op_name:
                x += 1
                z = int(data_list[x])
                x += 1
                while z > 0:
                    dom = data_list[x]
                    x += 1
                    t_name = data_list[x]
                    if dom == dom_name and t_name == type_name:
                        return True
                    z -= 1
                    x += 1
                return False
            x += 1
            x = x + (2 * (int(data_list[x]))) + 1
        return False


# runs the program by calling the main() method
if __name__ == "__main__":
    main()
