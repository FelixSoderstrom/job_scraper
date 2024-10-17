import sys

"""
Read up more on this and add more custom exceptions here

"""


class ApiError(Exception):
    def __init__(self, message):
        print(f"\nApiError: {message}")
        print("Exiting script..")
        sys.exit(1)
