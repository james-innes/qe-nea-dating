#!/usr/bin/python ->
#States interpreter destination for program execution
#Necessary with minimal IDE ie Visual Studio Code that does not support such comprehensive
#setup of environment like for example PyCharm were code is not run separately from CMD

#*Commenting System:
#* Highlghted Title
#! = important and should be changed before final exercution for user
#? = Questions
#Todo: = Any parts currenlty under development

#*Gnomenclature, Some variable names have been shortened:
#Eth == Ethnicity
#Lan == Language
#Cont == Continent
#i == Index

#*Import Dependencies
#TKinter is Python's de facto solution for implementing a GUI directly within python code
from tkinter import *
import tkinter as tk
from tkinter import ttk
#Can be used to display error messages in small windows
import tkinter.messagebox as tm
#Used to display images within window
from PIL import ImageTk, Image
#PyMySQL allows use of MySQL Query execration within python script
import pymysql
#Used to Quit and Execute from program, clear memory
import os

#*Setup database connection with cursor
db = pymysql.connect("localhost","root","","csneasc5")
c = db.cursor()

#*Defining Globals
global UserID
global Username
global Password
global FirstName
global LastName
global GenderID
global CountryID
global EthID
global LanID
global Age
global Bio
global toUserID
#Tuple can contain results from 'fetchall' on SQL query
global filterResults
#Not all functions should be possible to use without first being logged in
global LoggedIn
globals()["LoggedIn"] = False


def mainMenu():
	#This is the main function and is called first and after completing each other function
    print("\n***Main Menu***")
	#Function names will be executed later using 'print()' function
    options = {1: signup, 2: login, 3: profile, 4: Match, 5: Message, 6: logout, 7: deleteUser}
    #User friendly menu is printed
    print("(1) Create a new account\n(2) Login to existing account\n(3) Edit your Profile\n(4) Start Matching\n(5) Message a Match\n(6) Logout and Exit program\n(7) Delete my Account")
    try:
		#error capturing incase user does not correctly menu option index
        option = int(input("\nEnter option: "))
    except ValueError:
        print("Error, Enter a Number")
        mainMenu()
	#*Makes sure option is valid and that User is logged in before proceeding to certain functions from list
    if (globals()["LoggedIn"] == False) and (option in [3,4,5,7]):
        print("\nError, you must be logged in first\n")
        mainMenu()
    elif (globals()["LoggedIn"] == True) and (option in [3,4,5,7]):
        print(options[option]())
    elif option in [1,2,6]:
        print(options[option]())
    else:
		#Final error capturing
        print("\nError, Invalid Menu Option")
        mainMenu()

def login():
    print("\n***Login, Existing User***")
    #get User input for current Login session
    globals()["Username"] = str(input("Username: "))
    globals()["Password"] = str(input("Password: "))
    #search for account with Login details
    sql = "SELECT * FROM `User` WHERE Username='" + globals()["Username"] + "' AND Password='" + globals()["Password"] + "'"
    c.execute(sql)
	#Results from 'c.fetchall()' are stored within tuple which can be unwrapped and used later
    results = c.fetchall()
    #*update globals with current User info if account found
    if len(results) == 1:
        print("\nSuccess,", globals()["Username"], "Logged in")
        globals()["LoggedIn"] = True
        globals()["UserID"] = str(results[0][0])
        globals()["FirstName"] = str(results[0][3])
        globals()["LastName"] = str(results[0][4])
        globals()["Age"] = str(results[0][9])
        globals()["Bio"] = str(results[0][10])
        #*Query related tables to assign all data to user globals for later use
        sql = "SELECT Gender.Gender, Country.Country, Eth.Eth, Lan.Lan FROM ((((User INNER JOIN Gender ON Gender.GenderID=User.GenderID) INNER JOIN Country ON Country.CountryID=User.CountryID) INNER JOIN Eth ON Eth.EthID=User.EthID) INNER JOIN Lan ON Lan.LanID=User.LanID)"
        c.execute(sql)
        results = c.fetchall()
		#*'results[0][1]' shows example of how tuple holding 'results' can be accessed using an index
        globals()["GenderID"] = str(results[0][0])
        globals()["CountryID"] = str(results[0][1])
        globals()["EthID"] = str(results[0][2])
        globals()["LanID"] = str(results[0][3])
    #*otherwise if account not found show error Message
    else:
		#Error capturing
        print("\nError, Incorrect Username or Password")
    mainMenu()


def signup():
    print("\n***Signup, New User***")
    #Store desired signup details
    globals()["Username"] = str(input("Username: "))
    #Search for existing account with specified details
    sql = "SELECT * FROM `User` WHERE Username='" + globals()["Username"] + "'"
    c.execute(sql)
    if c.fetchall():
		#If query returns result then true so error is printed
        print("Error, Username Taken")
        signup()
    else:
        #*Loop through
        while not passwordStrenght():
            passwordStrenght
        #*Otherwise create new User account record
        else:
            sql = "INSERT INTO `User` (Username,Password,GenderID,CountryID,EthID,LanID) VALUES('" + globals()["Username"] + "','" + globals()["Password"] + "',1,1,1,1)"
            c.execute(sql)
            db.commit()
            print("Success, Account created")
            login()


def passwordStrenght():
	#Print user friendly password requirement instruction
    print("\n***Password Strength Requirements***\nMore than one letter from 'a..z'\nMore than one number between '0..9'\nMore than one 1 special character from '$#@?!'\nBe between 6 and 12 characters in lenght\n")
    globals()["Password"] = str(input("Password: "))
	#'Password' within globals is temporally assigned to value 'p' for typing efficiency
    p = globals()["Password"]
    valid = False
    #*Check for Password requirements
    while not valid:
        if (len(p)<6 or len(p)>12):
            print("\nError, Password must be between 6 and 12 characters in lenght")
            break
        elif not re.search("[a-z]",p):
            print("\nError, Password must contain at leats one capital letter")
            break
        elif not re.search("[0-9]",p):
            print("\nError, Password must contain at least one number")
            break
        elif not re.search("[A-Z]",p):
            print("\nError, Password must contain some letters from the alphabet")
            break
        elif not re.search("[$#@?!]",p):
            print("\nError, Password must contain a special character ")
            break
        elif re.search("\s",p):
            break
        else:
			#*If successful then 'True' is returned so that the 'passwordStregnth' function will no longer be executed form within the while loop in the 'signUp' function
            print("Success, Password Valid")
            valid = True
            return True


def profile():
    print("\n***Enter and Edit your Profile information***")
    #Dictionary with index and name of table to be edited
    fields = {'2': 'Password', '3': 'FirstName', '4': 'LastName', '5': 'Age', '6': 'Gender', '7': 'Eth', '8': 'Country', '9': 'Lan', '11': 'Bio'}
    #Get index of table to be edited
    lookUpTable = ["6","7","8","9"]
    exit = False
    while exit is False:
        index = 0
        #*Prints current Profile info for User including fields from related tables
		#'INNER JOIN' is used is used to enforce a constraint on the query across the related tables, this means the Primary and Foreign key match must be valid
        #The 'WHERE' command is used to only return the profile information for the current user
        sql = "SELECT User.Username, User.Password, User.FirstName, User.LastName, Gender.Gender, Country.Country, Eth.Eth, Lan.Lan, User.Bio, User.Bio, User.UserID FROM `User` INNER JOIN Gender ON (User.GenderID = Gender.GenderID) INNER JOIN Country  ON (User.CountryID = country.CountryID) INNER JOIN Eth  ON (user.EthID = eth.EthID) INNER JOIN Lan  ON (User.LanID = lan.LanID) WHERE (User.Password ='" + globals()["Password"] + "' AND User.UserID ='" + globals()["UserID"] + "')"
        c.execute(sql)
        results = c.fetchall()
        fieldNames = [i[0] for i in c.description]
        print("\nCurrent Profile Information:\n",fieldNames,"\n",results)
		#Prints choices of fields to edit and then checks if inputed index is valid
        print("\nChoice of Fields to Edit:\n", str(fields))
        while index == 0:
            index = str(input("\nEnter Index: "))
            if index not in fields:
                print("Error, You must select a valid option")
                mainMenu()
		#'field' is given the name of the field selected by the user
        field = str(fields[index])
		#*certain tables are lookup tables while the others are fields in the user table
        if index in lookUpTable:
            #*Print options for this lookup field
            sql = "SELECT * FROM " + field + ""
            c.execute(sql)
            results = c.fetchall()
            print("\nSelect an option from the below list for table ",field,":")
			#prints each row on a new line and includes both option and ID so user doesn't have to risk misspelling value
            for row in results:
                print(row)
            #Check to see if value entered is an integer and won't crash the next part
            try:
                value = str(input("\nEnter Value ID: "))
            except KeyError:
				#if invalid then user must start again
                print("Error, Invalid input")
                mainMenu()
			#Each lookup table has for example 'GenderID' and 'Gender' as field names
			#*Makes sure ID exists within the given lookup table
            fieldID = field + "ID"
            sql = "SELECT " + fieldID + " FROM " + field + " WHERE " + fieldID + "='" + value + "'"
            c.execute(sql)
            results = c.fetchall()
			#If the inputed ID does not exist within the lookup table then the User is returned to the main menu
            if not results:
                print("\nError; Enter a valid value for ", field)
                mainMenu()
            else:
				#*If the user inputted data is indeed valid then changes will be committed 
                sql = "UPDATE " + field + " INNER JOIN `User` ON " + field + "." + fieldID + "= User." + fieldID + " SET User." + fieldID + "= " + value + " WHERE (((User.UserID)= '" + str(globals()["UserID"]) + "'))"
                c.execute(sql)
                db.commit()
                print("Sucsess, Updated", field)
        else:
            #Still make sure password is valid for critieria
            if index == "2":
                while not passwordStrenght():
                    passwordStrenght
                value = globals()["Password"]
            else:
			    #If field selection is not from lookup tables then allow user to enter value directly int field in user table
                try:
                    value = input("Enter Value: ")
                except KeyError:
                    print("Error, Invalid input")
                    mainMenu()
			#*Commit change to Field in User table
            sql = "UPDATE `User` SET " + field + "='" + value + "' WHERE UserID='" + str(globals()["UserID"]) + "'"
            c.execute(sql)
            db.commit()
            print("Sucsess, Updated", field)
            #*Allow user to edit another field or return to main menu
        if input("(y)(n) Continue: ") == 'y':
            exit = False
        else:
            exit = True
    mainMenu()


def Match():
	#*Main Match function uses other sub-functions
    if filterUsers() is False:
        print("Error, Filter Users function returned False")
        mainMenu()
    results = globals()["filterResults"]
    print("\n***Send Requests to Users you like the look of***")
   
    root = Tk()
    tk.title = "User Profile"
    #Setups window appearance and size
    cv = tk.Canvas(width=500, height=500, bg='pink')  
    cv.pack()

    for row in results:
		#*Runs for each user profile stored in the global results tuple by the 'filterUsers()' function
		#*Print the user profiles information
        print([i[0] for i in c.description])
        print(row)
        #display profile picture using function
        
        #*Show window with profile image using TKinter
        #Implements name of file into path from local 'UserID' as PictureID
        img=Image.open("images/"+str(row[9])+".jpg")
        #resizes given image in and stores in temporary value 'rimg' in preparation
        rimg = img.resize((400, 400),Image.ANTIALIAS)
        img=ImageTk.PhotoImage(rimg) 
        cv.create_image(250, 250, image=img)
        root.update_idletasks()
        #Sets name of window title to name of given user so multiple open windows can be identified
        root.update()

        #*Promt User for next step
        option = input("\n(e) Exit (r) Request (n) Next: ")
        if option == "r":
            sql = "SELECT * FROM `Match` WHERE (FromID='" + globals()["UserID"] + "' AND ToID='" + str(row[9]) + "') OR (FromID='" + str(row[9]) + "' AND ToID='" + globals()["UserID"] + "')"
            c.execute(sql)
            results2 = c.fetchall()
            if results2:
                name = results[0][0] + " " + results[0][1]
                #If Match record exists then contiune
                if str(results2[0][3]) == "1":
                    #If state is Ture then tell user they can't match again with same user
                    print("\nYou have already matched with User ",name)
                elif str(results2[0][3]) == "0":
                    #if state is false then update status to true and print that the user has made a new match!
                    print("\nCongratulations, You have Matched with",name)
                    sql = "UPDATE `Match` SET State='1' WHERE MatchID='" + str(results2[0][0]) + "'"
                    c.execute(sql)
                    db.commit()
            else:
                #else if match does not exist then insert new match record with state as false
                sql = "INSERT INTO `Match` (FromID, ToID, State) VALUES('" + globals()["UserID"] + "'," + str(results[0][9]) + ",'" + "0" + "')"
                c.execute(sql)
                db.commit()
        elif option == "e":
            break
    mainMenu()


def filterUsers():
	#*Allows user to filter all the users in the database to only see those who fulfill certain criteria
    print("\n***Enter in preferences to Filter Potential Users***")
    # Dictionary with index and name of table to be filtered by
    fields = {1: 'Gender', 2: 'Country', 3: 'Eth', 4: 'Lan'}
	#List which will be used to hold user entered values
    values = []
    index = 0
    exit = False
    count = 0

    for i in fields:
		#Each time loop go's round it will execute commands on next field
        index += 1
        field = fields[index]
        sql = "SELECT * FROM " + field + ""
        c.execute(sql)
        result = c.fetchall()
        print("\nSelect an option from the below list for table ",field,":")
		#prints each row on a new line and includes both option and ID so user doesn't have to risk misspelling value
        for row in result:
            print(row)
        # Take Input from User
        #Check to see if value entered is an integer and won't crash the next part
        try:
            value = str(input("\nEnter Value ID: "))
        except ValueError:
			#if invalid then user must start again
            print("Error, Invalid input")
            mainMenu()
        print("\n")
        #* Check to see if value entered is from lookup field
        fieldID = field + "ID"
        sql = "SELECT " + fieldID + " FROM " + field + " WHERE " + fieldID + "='" + value + "'"
        c.execute(sql)
        if c.fetchall():
            #*If the query is 'True' then the inputed value is appended to the value list which will later be accessed using the list index function
            values.append(value)
        else:
            print("Error for table ",field, ", please start again")
            return False
    else:
		#*Once user has selected options from lookup tables then user specifies options form local fields from 'User' table
		#Min and Max are taken so that the user can select from a range of ages
        min_age = input("Minimum Age: ")
        max_age = input("Maximum Age: ")
        #*Apply User input to SQL query and order results by UserID
		#Selection uses 'INNER JOIN' across related tables
        sql = "SELECT User.FirstName, User.LastName, Gender.Gender, Country.Country, Eth.Eth, Lan.Lan, User.Age, User.Age, User.Bio, User.UserID FROM `User` INNER JOIN Gender ON (User.GenderID = Gender.GenderID) INNER JOIN Country ON (User.CountryID = Country.CountryID) INNER JOIN Eth ON (User.EthID = Eth.EthID) INNER JOIN Lan ON (User.LanID = lan.LanID) WHERE (Gender.GenderID ='" + (values[0]) + "' AND Country.CountryID ='" + (values[1]) + "' AND Eth.EthID ='" + (values[2]) + "' AND lan.LanID ='" + (values[3]) + "' AND User.Age >='" + min_age + "' AND User.Age <='" + max_age + "') ORDER BY User.UserID"
        c.execute(sql)
        results = c.fetchall()
        if results:
			#Counts how many user profiles have been returned and stores them in the global tuple 'globals()["filterResults"]'
            for row in results:
                count =+ 1
            globals()["filterResults"] = results
            print("\nSuccess, found ",count,"Users Matching your filter")
            return True
        else:
            print("\nThe query returned no results")
            return False




def viewMatches():
    #Find total number of users for service
    sql = "SELECT * FROM User"
    c.execute(sql)
    results1 = c.fetchall()
    count = 0
    for row in results1:
        #*If the query of match status is true for given record then proceed
		#the match can be 'From=U1, To=U2, State=True' or 'From=U2, To=U1, State=True', but nothing else
        sql = "SELECT * FROM `Match` WHERE ((FromID='" + globals()["UserID"] + "' AND ToID='" + str(row[0]) + "') OR (FromID='" + str(row[0]) + "' AND ToID='" + globals()["UserID"] + "')) AND State='1'"
        c.execute(sql)
        results2 = c.fetchall()
        #*Select appropriate fields to display from valid match profile
        if len(results2) != 0:
            count =+ 1
            sql = "SELECT UserID, FirstName, LastName FROM `User` WHERE UserID='" + str(row[0]) + "'"
            c.execute(sql)
            results3 = c.fetchall()
			#*Print information for each user
            for User in results3:
                print(User)
    return count



def selectMatch():
	#*Allows user to select which user they want to message from those earlier printed by the 'viewMatches' function
    sql = "SELECT * FROM `User` WHERE UserID='" + input("Enter ID of User you wish to Message: ") + "'"
    c.execute(sql)
    results = c.fetchall()
    if len(results) != 0:
		#*This will be used later by the 'sendMessage()' function
        globals()["toUserID"] = str(results[0][0])
    else:
        print("Error, No Matches found")


def showMessages():
    print("\n***Messages with Selected Match***")
	#Select all messages in the 'Message' field in the 'Message' table that pertain to the users in the selected match
    sql = "SELECT `Message` FROM `Message` WHERE (FromID="+globals()["UserID"]+" AND ToID="+globals()["toUserID"]+") OR (FromID="+globals()["toUserID"]+" AND ToID="+globals()["UserID"]+")"
    c.execute(sql)
    results = c.fetchall()
    for row in results:
        print(row)


def sendMessage():
    print("\n***Send a Message***")
    Message = input("Message: ")
    if Message == "":
        print("Error, Message is empty")
	#*'FromID' and 'ToID' are inserted so that they can be queried later by the 'viewMatches' function
    sql = "INSERT INTO Message (FromID, ToID, Message) VALUES('" + globals()["UserID"] + "','" + globals()["toUserID"] + "','" + Message + "')"
    c.execute(sql)
    db.commit()
    print("Message to " + globals()["toUserID"], "sent")


def Message():
	#Instead of creating one huge multi nested function the 'Message' function has been split-up into smaller sub functions
	#'while' loop used to allow the user to continue messaging as much as they want
	#option 'n' is not checked for because both 'while' statements also work to capture errors
    while input("\n(y)(n) Continue: ") == "y":
        if viewMatches() <1:
            break
            mainMenu()
        else:
            selectMatch()
            showMessages()
            sendMessage()
            showMessages()
        while input("\n(y)(n) Send a Message: ") == "y":
            showMessages()
            sendMessage()
            showMessages()
    mainMenu()
        

def deleteUser():
    print("\n***Delete Your Account***")
    if input("(y)(n) Continue to delete account: ") == "y":
		#Only use of 'DELETE' SQL command within program to permanently delete record for given user in 'User' table
		#SQL Database is setup so that this will not cause any relationship dependency or constraint issues
       sql = "DELETE FROM `User` WHERE UserID='" + globals()["UserID"] + "'"
       c.execute(sql)
       db.commit()
       print("Success, Account Deleted")
    mainMenu()


def logout():
    print("\n***Logout & Exit Program***")
	#*To correctly close the program memory is flushed with globals cleared
    print("Thank you for choosing to use this service, Bye")
    for name in dir():
        if not name.startswith('_'):
            del globals()[name]
    db.commit()
	#The connection used by this application to the database is closed
    db.close()


print("\n***Welcome to Dating Solution***")
#*This is the only function initially called and allows the user to access all other functions as they wish
#*If any of the sub-functions experiences problems then predefined errors are printed to the user before they are returned to the main menu
mainMenu()