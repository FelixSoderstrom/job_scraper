from scraper import BlocketScraper
from data import regions
from data import InputError, ApiError
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
    amount_cards = user_choose_amount_of_cards()
    scraper.scrape_cards(amount_cards)  # This scrapes every card.
    jobs = scraper.jobs  # list[dict[str:str]]

    # chat gippity stuff here
    # print_scraped_jobs_debugger(jobs)


def user_choose_amount_of_cards(scraper) -> int: #change this name
    #CONTINUE HERE
    # The correct logic/syntax is in test.py
    """
    RAISES InputError.
    Presents the amount of cards found to user.
    User picks how many jobs to scrape.
    Integer is returned.
    """
    while True:
        print(
            f"Scraper found {scraper.total_cards} jobs to fit your search.\n"
            "This will take approximately "
            f"{round(scraper.total_cards / 5) + 1} seconds to scrape."
        )
        choice = input(
            "Would you like to scrape them all? [yes/no] "
        ).lower().strip()

        if choice == "yes":
            return scraper.total_cards
        elif choice =="no":
            break

    while True:
        try:
            amount_cards = int(
                input("How many jobs would you like to scrape? ").strip()
            )
            
        except ValueError:
            raise InputError(
                "You did not enter a number."
            )
        
        if 0 < amount_cards < scraper.total_cards:
            return amount_cards
        else:
            raise InputError(
                "You did not enter a valid number."
            )


def print_scraped_jobs_debugger(jobs):
    # Remove this function
    for job in jobs:
        print(f"Title: {job["title"]}")
        print(f"Company: {job["company"]}")
        print(f"Description: {job["description"]}")
        print(f"Link: {job["link"]}")
        print("-" * 50)


def disclaimer() -> bool:
    RED = '\033[31m'
    RESET = '\033[0m'
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
    Takes input and modifies the search term to fit in url.
    """
    while True:
        user_input = input("What kind of job are you looking for? ").lower()
        search_term = re.sub(" ", "+", user_input)
        if search_term:
            return f"=q{search_term}"
        else:
            raise InputError(
                "After processing your input, the search term was left empty.")


def get_region() -> str:
    """
    Takes input and matches against available regions.
    Translates input to fit in the url.
    """
    while True:
        valid_choices = ["region", "län", "city"]
        choice = input(
            "Would you like to search for jobs in a region(län) or a specific city? "
        ).lower()
        if choice in valid_choices:
            break
        else:
            raise InputError(
                f"Input did not match any of the following: {valid_choices}"
            )

    if choice == "region" or choice == "län":
        user_input = input("Please enter a region (län): ").lower().strip()
        if user_input in regions.län.keys():
            region = regions.län[user_input]
        else:
            region = find_suggestions(user_input)

    return region


def find_suggestions(user_input):
    # Use difflib here
    pass


if __name__ == "__main__":
    run()
