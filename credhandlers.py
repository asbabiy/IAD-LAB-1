"""
Supplementary function for validating and handling credentials from phonebook.py
"""
import re
from enum import Enum
from datetime import datetime


# regex for validating user-defined credentials
validation = re.compile(r"""
                        (?P<name>^[a-z][\w ]+$)|  # validates name and surname
                        (?P<date>^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.((19|20)\d{2})$)|  # validates dates
                        ^(\+7|8)(?P<phone>\d{10}$)|  # validates mobile phone numbers
                        (?P<landline_phone>^[348]\d{9})$  # validates landline phone numbers
                        """, re.X | re.I
                        )


class Credentials(Enum):
    """
    Credentials of each record in the table (attribute name),
    credentials which are shown to the user while requesting his data (1st value),
    regular expression patterns names (2nd value).
    """
    name = "NAME", "name"
    surname = "SURNAME", "name"
    birth_date = "DATE", "date"
    phone = "PERSONAL PHONE NUMBER", "phone"
    office_phone = "OFFICE PHONE NUMBER", "phone"
    landline_phone = "LANDLINE PHONE NUMBER", "landline_phone"


def get_details(details=Credentials.__members__.keys()):
    """
    Creates a tuple of credentials from Credentials,
    which will be requested from user during execution of specific functions.

    :param details: credentials which will be requested from the user
    :return: tuple of corresponding credential sets (cf. Credentials docs)
    """
    return tuple(x for x in Credentials if x.name in details)


def normalize_credentials(creds):
    """
    Normalizes user-defined credentials. Capitalizes name and surname,
    validates dates and transforms them into datetime format, normalizes phone numbers.

    :param creds: a dict with credentials
    :return: a dict with normalized credentials
    """
    new_creds = creds.copy()

    try:
        new_creds['birth_date'] = datetime.strptime(creds.get("birth_date"), "%d.%m.%Y")
    except (ValueError, TypeError):
        new_creds['birth_date'] = None
        print("\nDate is incorrect. Record was added without it.\n")

    new_creds['name'] = creds['name'].capitalize()
    new_creds['surname'] = creds['surname'].capitalize()

    new_creds['phone'] = "8" + creds["phone"]
    new_creds['office_phone'] = "8" + creds["office_phone"] if creds["office_phone"] else None

    return new_creds


def get_credentials(details, required_credentials, allow_null=True):
    """
    Requests credentials from user and validates them via regular expressions.

    :param details: credentials to request from user
    :param required_credentials: credentials which can't be omitted by user
    :param allow_null: defines if unfilled credentials (with None values) will be returned
    :return: dict with validated user-provided credentials
    """
    creds = {}

    for cred in details:
        while True:
            response = input(f"{cred.value[0]} >> ")
            response = validation.match(response)

            if response and response.groupdict()[cred.value[1]]:
                creds[cred.name] = response.groupdict()[cred.value[1]]
                break
            elif not response and cred.name not in required_credentials:
                creds[cred.name] = None
                break

            print("\nIt seems to be incorrect. Try again.\n")

    return {k: v for k, v in creds.items() if v} if not allow_null else creds
