"""
Supplementary functions for different minor actions in phonebook.py
"""
import os
import time
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta


def clear_output():
    """
    Clear console output.
    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def helper():
    """
    Shows all commands.
    :return: None
    """
    clear_output()
    print("WELCOME TO THE PHONEBOOK!")
    print()
    print("Please choose the number of the desired operation:")
    print("(1)  Add new record to the phonebook")
    print("(2)  Introduce some changes to the records")
    print("(3)  Remove a record from the phonebook")
    print("(4)  Get age of the person")
    print("(5)  Show all records")
    print("(6)  Find records")
    print("(7)  Get records by birthday")
    print("(8)  Remove a record by phone")
    print("(9)  Sort records")
    print("(10) Get records with birthday within a month")
    print("(11) Get records with the age above/below/exactly N years")
    print("(12) Remove all records")
    print()


def get_day_diff(then) -> int:
    """
    Get difference in days between given and current dates.

    :param then: date
    :return: number of days (can be negative)
    """
    now = datetime.today().date()
    then = then + relativedelta(year=now.year)
    return (then - now).days


def quit_book():
    """
    Quits the console interface.

    :return: None
    """
    clear_output()
    print("Thanks for using this phonebook!")
    time.sleep(1)
    clear_output()
    sys.exit()


def to_menu():
    """
    Returns to the main menu.

    :return: None
    """
    clear_output()
    print('Going back to the menu...')
    time.sleep(0.5)
    helper()


def get_age(record) -> int:
    """
    Calculates person's age at the present time

    :param record: a row from the table
    :return: age
    """
    return abs(relativedelta(datetime.now(), record.birth_date).years)