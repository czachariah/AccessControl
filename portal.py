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
        else:
            if len(sys.argv) == 4:
                AddUser(sys.argv[2], sys.argv[3])
            else:
                AddUser(sys.argv[2], "EMPTY_STRING")

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


# method used to add new Users
def AddUser(username, password):
    if checkForUser(username):
        print("\nSTATUS: ERROR! User already exists.\n")
    else:
        # user not found in the data, so now add the user
        if insertNewUser(username, password):
            print("\nSTATUS: SUCCESS! User added.\n")
        else:
            print("\nSTATUS: ERROR! Problems adding new user.\n")


# method to check whether the user has already been added
def checkForUser(username):
    # look for UsersData.txt file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    user_data = os.path.join(dir_name, "UsersData" + "." + "txt")

    if os.path.exists(user_data):
        # separate the lines into words and store each word into a list
        dataList = list()
        try:
            file = open("UsersData.txt", "r")
            for line in file:
                for word in line.replace("\r", "").replace("\n", "").split():
                    dataList.append(word)
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()
        file.close()

        for x in range(0, len(dataList), 2):
            # user found in the data
            if (dataList[x]) == str(username):
                return True
        return False
    else:
        # file not found, so user is not in the list
       return False


# method used to insert a new user into the UsersData
def insertNewUser(username, password):
    # look for UsersData.txt file
    dir_name = os.path.dirname(os.path.abspath(__file__))
    user_data = os.path.join(dir_name, "UsersData" + "." + "txt")

    if os.path.exists(user_data):
        # separate the lines into words and store each word into a list
        dataList = list()
        try:
            file = open("UsersData.txt", "r")
            for line in file:
                for word in line.replace("\r", "").replace("\n", "").split():
                    dataList.append(word)
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()
        file.close()

        dataList.append(username)
        dataList.append(password)

        os.remove(user_data)
        try:
            f = open("UsersData.txt", "a+")
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()

        for x in range(0, len(dataList), 2):
            f.write(str(dataList[x]))
            f.write("\t")
            f.write(str(dataList[x+1]))
            f.write("\n")
        f.close()

        return True
    else:
        dataList = list()
        dataList.append(username)
        dataList.append(password)
        try:
            f = open("UsersData.txt", "a+")
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()

        for x in range(0, len(dataList), 2):
            f.write(str(dataList[x]))
            f.write("\t")
            f.write(str(dataList[x + 1]))
            f.write("\n")
        f.close()
        return True


# runs the program by calling the main() method
if __name__ == "__main__":
    main()

'''
UserDataTable = []
        count = 0
# get the number of lines in UserData.txt
        try:
            file = open("UsersData.txt", "r")
            for line in file:
                count = count + 1
        except IOError:
            print("\nSTATUS: ERROR obtaining user data.\n")
            exit()

        # create the table and initialize it
        for i in range(count):
            UserDataTable.append([])
            for j in range(2):
                UserDataTable[i].append(".")
'''