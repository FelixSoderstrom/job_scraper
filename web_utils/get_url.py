from difflib import get_close_matches
from ..data_structures.custom_exceptions import InputError
from ..data_structures.regions import cities, län

"""
Kid woke up when I was in the zone.
My brain operates at 25% capacity.
Will revisit this tmrw.

Note to self:
We moved the constructing of url into this class.
Untouched working code is commentd out in main.py.
Dont remove that until this class is working.

You left off between confirm_location_exists and get_suggestions.
Rename variables nad stuff.
"""


class UrlConstructor:
    def __init__(self):
        self.search_term: str = self.get_search_term()
        self.location_type: str = self.get_location_type()
        self.filters: list = self.get_filters()
        self.url: str = self.construct_url()

    def construct_url(self):
        base_url = "jobb.blocket.se/lediga-jobb?q="

        # Example URL
        # https://jobb.blocket.se/lediga-jobb?q=Python&filters=oerebro-laen

        url = base_url + self.search_term + "".join(self.filters)

        return url

    def get_search_term(self) -> str:
        """
        Raises InputError.
        Defines self.search_term.
        Modifies to fit url.
        """
        while True:
            user_input = input("Enter a job search-term: ").lower()
            search_term = user_input.replace(" ", "+")

            if search_term:
                return search_term

            else:
                raise InputError(
                    "After processing your input, "
                    "the search term was left empty."
                )

    def get_location_type(self) -> str:
        """
        Raises InputError.
        Defines self.location_type.
        City or Region.
        """
        valid_location_types = ["region", "city"]
        while True:
            location_type = (
                input(
                    "Would you like to search within a city or region/län? "
                )
                .lower()
                .strip()
            )
            if location_type in valid_location_types:
                return location_type
            else:
                raise InputError(
                    "Input did not match any of the "
                    f"following: {", ".join(valid_location_types)}"
                )

    def get_filters(self) -> list[str]:
        """
        Defines self.filters
        list[str]
        """
        filter_prefix = "&filters="
        filters = []
        while True:
            user_input = (
                input(f"Enter a {self.location_type}: ").lower().strip()
            )
            location_string = self.confirm_location_exists(
                location=user_input
            )
            filter = filter_prefix + location_string
            filters.append(filter)
            more_filters = input(
                "Would you like to add another "
                f"{self.location_type}? [yes/no] "
            )
            if more_filters == "no":
                break
        return filters

    def confirm_location_exists(self, location):
        """
        Checks if ciry or region exists.
        If not, calls get_suggestions.
        Always returns a valid location.
        """
        while True:
            if self.location_type == "city":
                cities_set = set(cities)

                if location in cities_set:
                    # Correctly formatted cities only
                    # needs replacing 'å', 'ä' and 'ö'.
                    location_string = (
                        location.replace("å", "aa")
                        .replace("ä", "ae")
                        .replace("ö", "oe")
                        .replace(" ", "-")
                    )
                    break
                else:
                    location = self.find_suggestions(
                        location, available_searches=cities
                    )
            else:
                # Correctly formatted regions however are very inconsistent.
                # Some Swedish regions
                if location in set(län.keys()):
                    location_string = län[location]
                    break
                else:
                    location = self.find_suggestions(
                        location, available_searches=län
                    )

        return location_string

    def find_suggestions(self, user_input, location, available_searches):
        """
        Uses difflib to find close matches to users input.
        Presents suggestions and prompts user to enter location again.
        This is a part of the loop found in 'confirm_region_city_exists'
        and can be called recursively.
        """
        suggestions = get_close_matches(
            user_input,
            available_searches,
            n=len(available_searches),
            cutoff=0.65,
        )

        if suggestions:
            print(
                f"The {self.location_type}: '{user_input}' could not be found.\n"
                "Did you mean any of these?"
            )
            for suggestion in suggestions:
                print(suggestion.capitalize())

            return input("Please re-enter your choice here: ").lower().strip()
        else:
            print(
                "Your input didn't match any available options.\n"
                "Please try again."
            )
            return
