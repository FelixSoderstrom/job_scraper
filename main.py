from web_utils.scraper import BlocketScraper
from web_utils.get_url import UrlConstructor
from data_structures.custom_exceptions import InputError, ApiError
import os

"""
Note to self:


"""

# Assuming this is set to None if it doesn't exist in the users OS.
API_KEY = os.environ.get("OPENAI_API_KEY")
PEOJECT_ID = os.environ.get("OPENAI_PROJECT_ID_JOB_SCRAPER")


def run():
    # handling swarm agents.
    # Syntac should be more along the lines of:
    # if API_enabled():
    #     agent = JobCoach()
    # Instantiating this class should send out a
    # disclaimer regarding api calls and costs

    # This entire logic should be moved into a separate class
    # api_enabled = disclaimer()
    # if api_enabled:
    #     if API_KEY is None:
    #         raise ApiError(
    #             "Environment variable 'OPENAI_API' does not exist."
    #         )

    constructor = UrlConstructor()

    url = constructor.url
    search_terms = constructor.search_term_strings
    job_finder = BlocketScraper(
        url, search_terms
    )  # This only finds the cards(jobs).
    jobs = job_finder.jobs

    #
    # chat gippity stuff here
    print_scraped_jobs_debugger(jobs)


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


# def prompt_user_amount_cards(scraper) -> int:
#     """
#     Raises InputError.
#     Presents the amount of cards found to user.
#     User picks how many jobs to scrape.
#     Integer is returned.
#     """
#     while True:
#         print(
#             f"Scraper found {scraper.total_cards} relevant jobs.\n"
#             "This will take approximately "
#             f"{round(scraper.total_cards / 5) + 1} seconds to scrape."
#         )

#         try:
#             amount_cards = int(
#                 input("How many jobs would you like to scrape? ").strip()
#             )
#         except ValueError:
#             print(InputError("You did not enter a number."))
#             continue

#         try:
#             if 0 < amount_cards < scraper.total_cards:
#                 return amount_cards
#             else:
#                 print(InputError("You did not enter a valid number."))
#                 continue

#         except InputError as e:
#             print(e)


def print_scraped_jobs_debugger(jobs):
    # Remove this function
    try:
        for job in jobs:
            print(f"Title: {job["title"]}")
            print(f"Company: {job["company"]}")
            print(f"Description: {job["description"]}")
            print(f"Link: {job["link"]}")
            print("-" * 50)
    except TypeError as e:
        print(f"One or more jobs were missing: {e}")


if __name__ == "__main__":
    run()
