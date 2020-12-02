#!/usr/bin/env python3
"""
This is the the phonebook represented as a console application.
"""
import datetime as dt
import operator
import re
import time

from pony.orm import *  # ORM

from credhandlers import Credentials, get_details, normalize_credentials, get_credentials
from supplementary import clear_output, helper, quit_book, to_menu, get_day_diff, get_age

book = Database()
book.bind(provider="sqlite", filename="phone_book.sqlite", create_db=True)  # connect to the db


class Person(book.Entity):
    """
    Database table representing a person with their contact details.
    """
    name = Required(str)
    surname = Required(str)
    phone = Required(str)
    office_phone = Optional(str, nullable=True)
    landline_phone = Optional(str, nullable=True)
    birth_date = Optional(dt.date)


book.generate_mapping(create_tables=True)  # connecting table entities to db


@db_session
def show_book() -> None:
    """
    Prints the whole table.

    :return: None
    """
    clear_output()
    print("Here is your phonebook.")
    print()
    Person.select().show()


@db_session
def generate_query(details, required_credentials, allow_null=True):
    """
    Requests specific credentials from user
    and generates a query based on these credentials from the table.

    :param details: credentials to request from user
    :param required_credentials: credentials which can't be omitted by user
    :param allow_null: defines if unfilled credentials (with None values) will be returned
    :return: a query object from the table
    """
    creds = get_credentials(details, required_credentials, allow_null)
    query = Person.select().filter(**creds)
    return query


@db_session
def find_record():
    """
    Searches for the records matching user-provided credentials.

    :return: None
    """
    print(f"You chose to find records. Provide credentials of the person.\n")

    required_credentials = {}
    query = generate_query(Credentials, required_credentials, allow_null=False)

    print("\nThese are the appropriate records.\n")
    query.show()


@db_session
def get_record_by_names() -> Person:
    """
    Requests first and last names from user, validates them and retrieves a matching row from the table.

    :return: matching row from the table (table entity)
    """
    credentials = ("name", "surname")
    details = get_details(credentials)

    creds = get_credentials(details, credentials, allow_null=False)
    record = Person.get(name=creds["name"].capitalize(), surname=creds["surname"].capitalize())

    return record


@db_session
def change_names(creds):
    """
    Change first and last names in the given query.

    :param creds: a dict with credentials
    :return: a dict with new credentials (name and surname)
    """
    print("You chose to change you query. Provide credentials.\n")
    old_creds = creds.copy()

    required_credentials = ("name", "surname")
    details = get_details(required_credentials)

    credentials = get_credentials(details, required_credentials, allow_null=False)
    old_creds.update(credentials)

    return old_creds


@db_session
def add_record() -> None:
    """
    Adds new record to the table if provided name and surname attributes aren't present in the table.

    :returns: None
    """
    print(f"You chose to add a new record. Provide credentials of the person.\n")

    required_credentials = ("name", "surname", "phone")
    creds = get_credentials(Credentials, required_credentials)

    while True:
        if not Person.get(name=creds["name"].capitalize(), surname=creds["surname"].capitalize()):

            creds = normalize_credentials(creds)
            Person(**creds)
            print(f"\n{creds['name']} {creds['surname']} was added to your phonebook.\n")
            break

        else:
            print("\nThis person is already in the phonebook.\n")

            print(
                "Choose one of the options below:\n"
                "--- 'overwrite' to change the existing record\n"
                "--- 'change' to change your query\n"
                "--- 'menu' to return to the menu\n"
            )

            # creds = normalize_credentials(creds)
            response = input("OPTION >> ")
            print()

            if response == 'overwrite':
                record = Person.get(name=creds['name'], surname=creds['surname'])
                record.set(**creds)
                print("Record was overwritten successfully.")
                time.sleep(1)
                to_menu()

            elif response == 'change':
                Person(change_names(creds))
                continue

            elif response == 'menu':
                to_menu()

            else:
                print("Invalid option.\n")


@db_session
def remove_record():
    """
    Removes a record matching first and last names (requested from the user) from the table.

    :return: None
    """
    print(f"You chose to remove a record. Provide credentials of the person.\n")

    record = get_record_by_names()

    if record:
        record.delete()
        print(f"\nThis person was removed from your phone book.\n")
    else:
        print("\nThis person isn't in the phonebook.\n")


@db_session
def change_record():
    """
    Changes user-provided attributes of the records matching user-defined credentials.

    :return: None
    """
    print(f"You chose to change a record. Provide credentials of the person.\n")

    required_credentials = {}

    while True:
        query = generate_query(Credentials, required_credentials, allow_null=False)

        if len(query) == 1:
            print(f"\nSpecify attributes which you want to change.\n")

            record = query.get()
            creds = get_credentials(Credentials, required_credentials, allow_null=False)
            record.set(**creds)

            print("\nCredentials were successfully changed.")
            break
        else:
            print("\nThere is more than one appropriate row. Provide more details.\n")
            query.show()
            print()


@db_session
def get_age_by_names():
    """
    Calculates age of the person whose name and surname are defined by the user.

    :return: None
    """
    print(f"You chose to get someone's age. Provide credentials of the person.\n")

    record = get_record_by_names()

    if record:
        if record.birth_date:
            print(f"\nThis person is {get_age(record)} years old.\n")
        else:
            print("\nBirth date isn't specified.\n")
    else:
        print("\nThis person isn't in the phonebook.\n")


@db_session
def remove_by_phone() -> None:
    """
    Removes a record which contains the given phone number.
    If there are multiple records with this phone number, it lets user choose which one to remove.

    :return: None
    """
    print("You chose to remove a record given its phone number. Provide the phone number.\n")

    credentials = ("phone",)
    details = get_details(credentials)

    creds = get_credentials(details, credentials, allow_null=False)
    creds["phone"] = "8" + creds["phone"]

    query = Person.select().filter(**creds)

    if len(query) == 1:
        Person.get(**creds).delete()
        print("\nRecord was removed.")

    elif not len(query):
        print("\nThis phone number isn't in the phonebook. Try again.\n")

    else:
        print()
        query.show()

        print("\nThere are multiple records with this phone number.\n")

        while True:
            response = input("Enter ID (leftmost column) of the record you want to remove >> ")

            try:
                Person[int(response)].delete()
                print("\nRecord was removed.")
                break
            except (ObjectNotFound, ValueError):
                print("\nThere is no such ID in the phonebook. Try again.\n")


@db_session
def get_by_birthday():
    """
    Finds and shows people (records) whose birthday date corresponds to the user-provided one.

    :return: None
    """
    print(f"You chose to get records given the birthday. Provide day and month.\n")

    while True:
        response = input("BIRTHDAY (DD.MM) >> ")

        if birthday := re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])$", response):
            day, month = birthday.group().split(".")

            query = select(p for p in Person if
                           p.birth_date.day == day and
                           p.birth_date.month == month)
            print()
            query.show()
            break

        print("\nInvalid birthday format. Try again.\n")


@db_session
def get_nearest_birthdays():
    """
    Show people (records) who have birthday within 30 days.

    :return: None
    """
    print("You chose to get a list of the nearest birthdays.\n")

    records = []
    for p in Person.select():
        if p.birth_date and 0 <= get_day_diff(p.birth_date) <= 30:
            records.append(p)

    query = select((person.name, person.surname) for person in Person if person in records)
    query.show()


@db_session
def get_year_diff():
    """
    Shows all records, which are elder/younger/exactly N years old.
    N is provided by the user.

    :return: None
    """
    print(
        "You chose to select people whose age is above/below/equals N years.\n"
        "Provide age (e.g. 5) and comparison type (above/below/equals).\n"
    )

    op_dict = {"above": operator.gt, "below": operator.lt, "equals": operator.eq}

    while True:
        response = re.match(r"\d{,3}", input("AGE >> "))
        op = re.match(r"above|below|equals", input("COMPARISON TYPE >> "))
        print()

        records = []

        if response and op:
            for p in Person.select():
                if op_dict[op.group()](get_age(p), int(response.group())):
                    records.append(p)

            select(p for p in Person if p in records).show()
            break

        print("Invalid number of years or comparison type. Try again.\n")


@db_session
def remove_all_records():
    """
    Removes all records from the table.

    :return: None
    """
    response = input("Are you sure you want to remove all records? (yes/no) >> ")

    if response.lower() == "yes":
        Person.select().delete()
        print("\nAll records were removed.")

    elif response.lower() == "no":
        print("\nOperation aborted.")

    else:
        print("\nInvalid option.")


@db_session
def sort_by_attribute():
    """
    Sorts the table by given attribute (in ascending/descending order).

    :return: None
    """
    while True:

        response = input("Credential you want to sort by (name, surname, birth_date) >> ")
        response = re.match(r"name|surname|birth_date", response, re.I)

        sort_order = input("Order you want to use for sorting (ascending/descending) >> ")
        sort_order = re.match(r"ascending|descending", sort_order, re.I)

        if response and response.group():

            if sort_order == "ascending":
                query = Person.select().sort_by(f"p.{response.group()}")
            else:
                query = Person.select().sort_by(desc(f"p.{response.group()}"))

            print(f"\nYour phonebook sorted by {response.group()} is below.\n")
            query.show()
            break

        print("\nInvalid credential or sort order. Try again.\n")


commands = {
    "quit": quit_book,
    "menu": to_menu,
    "1": add_record,
    "2": change_record,
    "3": remove_record,
    "4": get_age_by_names,
    "5": show_book,
    "6": find_record,
    "7": get_by_birthday,
    "8": remove_by_phone,
    "9": sort_by_attribute,
    "10": get_nearest_birthdays,
    "11": get_year_diff,
    "12": remove_all_records,
}


def main():
    """
    Entry point.
    Displays console interface, executes user-requested actions and
    handles exceptions, connected with the user input.

    :return: None
    """
    helper()

    while True:
        try:
            print(
                "\nPlease enter:\n"
                "--- a command number\n"
                "--- 'quit' to quit\n"
                "--- 'menu' to return to the menu\n"
            )

            response = input("COMMAND >> ")

            clear_output()

            if response.lower() not in commands:
                print("You entered invalid command. Try again.")
                time.sleep(1)
                helper()
                continue

            commands[response]()

        except KeyboardInterrupt:
            to_menu()

        except UnicodeDecodeError:
            print("Input is corrupted.")


if __name__ == "__main__":
    main()
