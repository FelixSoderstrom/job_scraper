from scraper import BlocketScraper
from custom_exceptions import ApiError
import os

"""
Continue from here.
Start dabbling with the open ai API
send it the description and come up with a good setting
implement the logic for api keys and selections

api enables = false should skip the process entirely and 
review the dict to the user. user will then be prompted to save to file.

with apienabled=True
calls the api with description
presents the new data to the user. user will then be prompted to save file.

"""


def run(url):
    API_KEY = os.environ.get("OPENAI_API")

    api_enabled = disclaimer()
    if api_enabled:
        if API_KEY is None:
            raise ApiError("Environment variable 'OPENAI_API' does not exist.")

    url = define_search_term()
    # url = f"https://jobb.blocket.se/lediga-jobb?q={search_term}&filters={region}"
    scraper = BlocketScraper(url)
    jobs = scraper.jobs  # list[dict[str:str]]

    # placeholder debugger
    # for job in jobs:
    # print(f"Title: {job["title"]}")
    # print(f"Company: {job["company"]}")
    # print(f"Description: {job["description"]}")
    # print(f"Link: {job["link"]}")
    # print("-" * 50)


def disclaimer() -> bool:
    while True:
        print(
            "DISCLAIMER\n"
            "This script scrapes data from job applications on 'jobb.blocket.se'"
            "and uses the OpenAI API for every job found.\n"
            "Be aware that using broad search terms in large regions may result "
            "in a lot of data and therefore alot of API calls.\n"
            "If you decide to use the API: \n"
            "Remember that OpenAI will charge you according "
            "to your agreed payment plan!\n"
            "Make sure you read the code and understand it before you proceed.\n"
            "Note: The API is completely optional and the script will run "
            "with limited functinality without an API-key.\n"
        )

        choice = input("Would you like to use the OpenAI API? [yes/no] ")
        if choice == "yes":
            return True
        elif choice == "no":
            return False


def define_search_term():
    pass


if __name__ == "__main__":
    url = "https://jobb.blocket.se/lediga-jobb?q=Python&filters=oerebro-laen"
    run(url)
