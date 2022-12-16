import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass




# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        if not isinstance(date, datetime.date):
            raise("date incorrect type")
        self.name = name
        self.date = date
                
    
    def __str__(self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date})"


    def get_name(self):
        return self.name
    
    def get_date(self):
        return self.date

    def get_week(self):
        return self.date.isocalendar()[1]

    def get_year(self):
        return self.date.year

    def __eq__(self, other):
        if self.name == other.get_name() and self.date == other.get_date():
            return True
        else:
            return False
        
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if not isinstance(holidayObj, Holiday):
            raise("holidayObj data type incorrect")
        # Use innerHolidays.append(holidayObj) to add holiday
        self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday


    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        find_holiday = Holiday(HolidayName, Date)
        for holiday in self.innerHolidays:
            if holiday == find_holiday:
                return holiday
        return False
        # Return Holiday

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        remove_holiday = self.findHoliday(HolidayName, Date)
        # remove the Holiday from innerHolidays
        if not isinstance(remove_holiday, Holiday):
            return False
        else:
            self.innerHolidays.remove(remove_holiday)
        # inform user you deleted the holiday


    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, "r") as f:
            data = json.load(f)
            for i in data['holidays']:
                holiday = i["name"]
                date = i["date"]
                date = date.split("-")
                date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                # Use addHoliday function to add holidays to inner list.
                self.addHoliday(Holiday(holiday, date))
            f.close()

     
    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        holidays = []
        for holiday in self.innerHolidays:
            holidays.append({"name": holiday.get_name(), "date": str(holiday.get_date())})
        with open(filelocation, "w") as outfile:
            json.dump({"holidays": holidays}, outfile, indent = 4)
        
    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     
        pass

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        year, week_number = int(year), int(week_number)
        holidays = list(filter(lambda holiday: (holiday.get_week() == week_number and holiday.get_year() == year), self.innerHolidays))
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        return holidays

    def displayHolidaysInWeek(self, year, week):       # second param: holidayList?????
        filtered_holidays = self.filter_holidays_by_week(year, week)
        print(f"\nThese are the holidays for this week ({year}, {week}): ")
        for holiday in filtered_holidays:
            print(holiday)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        return True

    def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        pass

    def viewCurrentWeek(self, year):
        # Use the Datetime Module to look up current week and year
        currentDate = datetime.date.today()
        currentWeek = currentDate.isocalendar()[1]
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(year, currentWeek)
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        return currentWeek




# Helper Functions 
# Used in main() for the different options
# handle printouts and actual calls to neccesary functions 
def option1(holidayList):
    print("\nAdd a Holiday \n==================")
    holidayName = input("Holiday: ")
    date = input("Date (yyyy-mm-dd): ")
    date = date.split("-")
    while type(date) != datetime.date:
        try: 
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        except:
            print("Error: \nInvalid date. Please try again. \n")
            date = input(f"Date for {holidayName} (yyyy-mm-dd): ")
            date = date.split("-")
    holidayObj = Holiday(holidayName, date)
    holidayList.addHoliday(holidayObj)
    print(f"\nSuccess: \n{str(holidayObj)} has been added to the holiday list.")


def option2(holidayList):
    print("\nRemove a Holiday \n==================")
    holidayName = input("Holiday Name: ")
    date = input("Date (yyyy-mm-dd): ")
    date = date.split("-")
    while type(date) != datetime.date:
        try: 
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        except:
            print("Error: \nInvalid date. Please try again. \n")
            date = input("Date (yyyy-mm-dd): ")
            date = date.split("-")
    holidayObj = Holiday(holidayName, date)
    didWork = holidayList.removeHoliday(holidayName, date)
    if didWork == False:
        print(f"\nError: \n{str(holidayObj)} was not found. \nPlease try again.")
    else:
        print(f"\nSuccess: \n{str(holidayObj)} has been removed from the holiday list.")


def option3(holidayList):
    print("\nSaving Holiday List \n====================")
    save_input = input("Are you sure you want to save your changes? [y/n]: ")
    if save_input == "y":
        filelocation = input("Enter filename.json (ex. holiday_list.json): ")
        holidayList.save_to_json(filelocation)
        print(f"\nSuccess: \nYour changes have been saved to {filelocation}")
    else:
        print("\nCanceled \nHoliday list file save canceled.")
    

def option4(holidayList):
    print("\nView Holidays")
    print("=================")
    year = input("Which year? (2020 - 2024): ")
    week = input("Which week? (1-52, or leave blank for the current week): ")
    if week == "":
        holidayList.viewCurrentWeek(year)
    else:
        holidayList.displayHolidaysInWeek(year, week)


def option5(holidayList, isSaved):
    print("\nExit \n=====")
    if isSaved:
        exit_input = input("Are you sure you want to exit? [y/n]: ")
        if exit_input.lower() == "y":
            print("\nGoodbye!")
            exit()
    else:
        print("Are you sure you want to exit? \nYour changes will be lost.")
        exit_input = input("[y/n]: ")
        if exit_input.lower() == "y":
            print("\nGoodbye!")
            exit()
    


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    holidayList = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    fileLocation = "holidays.json"
    holidayList.read_json(fileLocation)
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.


    print("\nHoliday Management \n===================")
    print(f"There are {holidayList.numHolidays()} holidays stored in the system. \n")
    # 3. Create while loop for user to keep adding or working with the Calender
    saved = False
    stillInMenu = True
    while stillInMenu:
    # 4. Display User Menu (Print the menu)
        user_input = input("\nHoliday Menu \n=================== \n1. Add a Holiday \n2. Remove a Holiday \n3. Save Holiday List \n4. View Holidays \n5. Exit \n")
    # 5. Take user input for their action based on Menu and check the user input for errors
        if user_input == "1":
            option1(holidayList)
            saved = False
        elif user_input == "2":
            option2(holidayList)
            saved = False
        elif user_input == "3":
            option3(holidayList)
            saved = True
        elif user_input == "4":
            option4(holidayList)
        elif user_input == "5":
            option5(holidayList, saved)
        else:
            print("Incorrect input.")
    # 6. Run appropriate method from the HolidayList object depending on what the user input is 
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
        continue_input = "\nDo you want to continue using the Holiday Manager? [y/n]: "
        if continue_input.lower() == "n":
            print("\nThank you for using the Holiday Manager. \nGoodbye!")
            exit()
        else:
            continue

if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.

