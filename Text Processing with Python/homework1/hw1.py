# Homework 1 - CS 4395
# Zachary Tarell - zjt170000
# Mazidi - Fall 2020
# Program takes in an employee info .csv file and makes into an employee list with corrected info

import sys
import re
import pickle
import pathlib


#   Create a class Person
class Person:
    #   create a constructor that initializes data
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    #   Display information about person with proper indention and formatting
    def display(self):
        print('\nEmployee id: ', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)


#   Function to process file data line by line
def process_lines(persons):
    #   Avoid header by reading first line then starting while loop
    line = f.readline()
    #   Read each line inside while loop after avoiding header
    while True:
        line = f.readline().strip()
        #   break out of while loop if no more lines to read
        if not line:
            break
        #   split line with comma separated value
        tempList = line.split(',')
        #   First letter capitalize text of last then first names
        tempList[0] = tempList[0].capitalize()
        tempList[1] = tempList[1].capitalize()
        #   check for middle initial or substitute an X
        if (len(tempList[2]) != 1):
            tempList[2] = 'X'
        #   check id and make sure first 2 letters are capitalized and followed by 4 digits
        while (re.match('[A-Z][A-Z]\d{4}', tempList[3]) == None):
            print('ID invalid: ', tempList[3])
            print('ID is two capital letters followed by 4 digits')
            tempList[3] = input('Please enter a valid id: ')
        #   phone number check for proper digits separated by hyphens
        while (re.match('\w{3}-\w{3}-\w{4}', tempList[4]) == None):
            print('Phone ', tempList[4], ' is invalid')
            print('Enter phone number in form 123-456-7890')
            tempList[4] = input('Enter phone number: ')
        # Add into dictionary which is created in the main() function
        employee = Person(tempList[0], tempList[1], tempList[2].capitalize(), tempList[3], tempList[4])
        employees[tempList[3]] = employee
    return employees


#   Code given that runs main and uses the pickle library
if __name__ == '__main__':
    #   check to see if the arg is there, else quit with a message
    if len(sys.argv) < 2:
        print('Please enter a file name as a system arg')
        quit()

    #   uses pathlib library that reads data.csv file
    rel_path = sys.argv[1]
    f = open(pathlib.Path.cwd().joinpath(rel_path), 'r')

    #   creates the dictionary and adds employee data from the processed_lines() function
    employees = {}
    employees = process_lines(employees)  # Ignore heading line

    #   pickle the employees
    pickle.dump(employees, open('employees.pickle', 'wb'))

    #   read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    #   output employees
    print('\n\nEmployee List:')

    #   calls the display() function inside loop with pickle load
    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
