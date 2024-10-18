from scraper import BlocketScraper
from data.regions import län, cities
from data.custom_exceptions import InputError, ApiError
from difflib import get_close_matches
import os
import re

"""
Continue from here.
I will probbably use OpenAI's Swarm for this project.
For everyy job I can instantiate a class that creates agents.
Agent1 takes descr-text and summarized into 2-3 sentences.
We relay this summary to the user, they decide if the job is relevant or not.
We ask the user for their skillset (no need for agent call here).
We relay the full job desc-text alongsite user skillset to agent2.
Agent2 writes a cover letter for user.
Cover letter is previewed.
User is prompted to save letter to a file.


I think the logic is done. In a hurry. Will look again tonight.


"""


def run(url):
    API_KEY = os.environ.get("OPENAI_API")
    api_enabled = disclaimer()
    if api_enabled:
        if API_KEY is None:
            raise ApiError(
                "Environment variable 'OPENAI_API' does not exist."
            )

    url = define_search_term()

    scraper = BlocketScraper(url)  # This only finds the cards(jobs).
    amount_cards = prompt_user_amount_cards()
    scraper.scrape_cards(amount_cards)  # This scrapes every card.
    jobs = scraper.jobs  # list[dict[str:str]]

    # chat gippity stuff here
    # print_scraped_jobs_debugger(jobs)


def disclaimer() -> bool:
    RED = "\033[31m"
    RESET = "\033[0m"
    while True:
        print(
            f"{RED}DISCLAIMER!{RESET}\n"
            "This script scrapes data from 'www.blocket.se' "
            "and can therefore only look for job applications in Sweden.\n"
            f"This script uses the OpenAI API for every job that is found.\n"
            "You will be warned and prompted to confirm "
            "before any calls are made.\n"
            f"{RED}Be aware{RESET} that using broad search terms "
            "in large regions may result "
            "in a lot of listings and therefore alot of API calls.\n"
            "If you decide to use the API: \n"
            f"Remember that OpenAI will charge you according "
            "to your agreed payment plan!\n"
            f"Make sure you {RED}read the code and understand it{RESET} "
            "before you proceed.\n"
            f"I do {RED}NOT{RESET} take responsibility for your own stupidity.\n"
            "The API is completely optional and the script will run "
            "with limited functinality without an API-key.\n"
        )

        choice = input("Would you like to use the OpenAI API? [yes/no] ")
        if choice == "yes":
            return True
        elif choice == "no":
            return False


def define_search_term() -> str:
    base = "jobb.blocket.se/lediga-jobb?"
    job = get_job_title()
    region = get_region()

    url = base + job + region
    return url


def get_job_title() -> str:
    """
    Takes input and modifies the job search-term to fit in url.
    """
    while True:
        user_input = input("What kind of job are you looking for? ").lower()
        search_term = re.sub(" ", "+", user_input)
        if search_term:
            return f"=q{search_term}"
        else:
            raise InputError(
                "After processing your input, the search term was left empty."
            )


def get_region() -> str:
    """
    Takes input and matches against available regions.
    Translates input to fit in the url.
    """
    while True:
        valid_location_types = ["region", "län", "city"]
        location_type = (
            input(
                "Would you like to search for jobs in a region(län) or a specific city? "
            )
            .lower()
            .strip()
        )
        if location_type in valid_location_types:
            break
        else:
            raise InputError(
                "Input did not match any of the "
                f"following: {", ".join(valid_location_types)}"
            )

    if location_type == "region" or location_type == "län":
        user_input = input(f"Enter a {location_type}: ").lower().strip()

    elif location_type == "city":
        user_input = input(f"Enter a {location_type}: ").lower().strip()

    search_term = confirm_region_city_exists(user_input, location_type)

    return search_term


def confirm_region_city_exists(user_input, location_type) -> str:
    """
    Takes the city or region choice as location_type.
    Changes and returns the string depending on location type.
    Calls find_suggestions and loops with
    """
    while True:
        if location_type == "city":
            cities_set = set(cities)

            if user_input in cities_set:
                search_term = (
                    user_input.replace("å", "aa")
                    .replace("ä", "ae")
                    .replace("ö", "oe")
                    .replace(" ", "-")
                )
                break
            else:
                user_input = find_suggestions(
                    user_input, location_type, available_searches=cities
                )
        else:
            if user_input in län.keys():
                search_term = län[user_input]
                break
            else:
                user_input = find_suggestions(
                    user_input, location_type, available_searches=län
                )

    return search_term


def find_suggestions(user_input, location_type, available_searches):
    """
    Uses difflib to find close matches to users input.
    Presents suggestions and prompts user to enter location again.
    This is a part of the loop found in 'confirm_region_city_exists'
    and can be called recursively.
    """
    suggestions = get_close_matches(
        user_input, available_searches, n=len(available_searches), cutoff=0.65
    )

    if suggestions:
        print(
            f"The {location_type}: '{user_input}' could not be found.\n"
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


def prompt_user_amount_cards(scraper) -> int:
    """
    RAISES InputError.
    Presents the amount of cards found to user.
    User picks how many jobs to scrape.
    Integer is returned.
    """
    while True:
        print(
            f"Scraper found {scraper.total_cards} relevant jobs.\n"
            "This will take approximately "
            f"{round(scraper.total_cards / 5) + 1} seconds to scrape."
        )

        try:
            amount_cards = int(
                input("How many jobs would you like to scrape? ").strip()
            )
        except ValueError:
            print(InputError("You did not enter a number."))
            continue

        try:
            if 0 < amount_cards < scraper.total_cards:
                return amount_cards
            else:
                print(InputError("You did not enter a valid number."))
                continue

        except InputError as e:
            print(e)


def print_scraped_jobs_debugger(jobs):
    # Remove this function
    for job in jobs:
        print(f"Title: {job["title"]}")
        print(f"Company: {job["company"]}")
        print(f"Description: {job["description"]}")
        print(f"Link: {job["link"]}")
        print("-" * 50)


if __name__ == "__main__":
    run()
