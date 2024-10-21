"""
I think thats more correct

"""

RED = "\033[91m"
YEL = "\033[93m"
RES = "\033[0m"


class ApiError(Exception):
    def __init__(self, message):
        self.message = f"\n{RED}ApiError:{RES} {message}"
        super()._init__(self.message)


class InputError(Exception):
    def __init__(self, message):
        self.message = f"\n{YEL}InputError:{RES} {message}\nPlease try again.\n"
        super().__init__(self.message)
