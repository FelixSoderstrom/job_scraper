from bs4 import BeautifulSoup, NavigableString, Tag
from requests.exceptions import RequestException
from time import sleep
import re
import sys
import requests
import logging

"""
This class scrapes in two stages.

Stage 1:
    Scrapes all job-cards from the search page.
    Returns a list of BeautifulSoup Tags (cards).
    Here, we can access title, company and the link to the full description.
    Note: Link mentioned above is NOT the same link that is being retuend below.

Stage 2:
    Upon user confirmation, scrapes a specified amount of cards.
    Here we can access 
    application link (the one we return in the deictionary below)
    and description text.

    Return example:
        jobs = [
            {
                "title": "Look here, come work for us!",
                "company": "Uncle Bobs Indentation Error Inc.",
                "link": "https://www.example.com",
                "description": "Lorem ipsum"
            }, 
            ...
        ]


Note to self:
Instead of having this be funtional programming with extra steps:
Try to set init variable-values to functions that return.
Look at UrlConstructor for reference.
We still want the class to work in two stages.
But having variable values be return values of methods allows for 
more explicit type annotation throughout the class.
"""


class BlocketScraper:
    def __init__(self, url):
        self.url = url
        self.jobs = []  # Ready data
        self.total_cards = 0
        self.cards_scraped = 0
        self.all_cards = self.find_cards()

    def find_cards(self) -> list[Tag]:
        """
        Finds each job-card from the search page.
        Appends the tags and returns the list.
        """
        soup = self.scrape(url=self.url)
        cards = soup.find_all("div", class_="sc-b071b343-0 eujsyo")
        return cards

    def scrape_cards(self, amount_cards):
        if amount_cards == self.toal_cards:
            pass

        else:
            self.all_cards = self.all_cards[:amount_cards]

        for card in self.all_cards:
            self.cards_scraped += 1
            print(f"Scraping page {self.cards_scraped}/{self.total_cards}")
            sleep(0.2)
            job = self.get_information(card)
            self.jobs.append(job)

    def scrape(self, url) -> BeautifulSoup:
        """
        Scrapes and returns a BeautifulSoup class
        Raises RequestException.
        """
        retry_amount = 3
        retry_delay = 5
        for attempt in range(retry_amount):
            logging.info("Requesting URL...")
            try:
                r = requests.get(url)
                r.raise_for_status()
                return BeautifulSoup(r.content, "html.parser")

            except RequestException as e:
                logging.error(
                    f"Request failed (attempt {attempt + 1}"
                    f"/{retry_amount}): {e}"
                )

                if attempt < retry_amount:
                    logging.info(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)

                else:
                    logging.error(
                        f"Could not fetch data in {retry_amount} "
                        "retries. Exiting program..."
                    )
                    sys.exit(1)

    def get_information(self, card) -> dict[str:str]:
        title = card.find(
            "h2", class_="sc-f74edbc7-0 sc-6694485c-3 bZDiVh eUtWPK"
        ).string

        company = card.find("span", class_="sc-6694485c-5 hCmCSo").string

        prefix = "https://jobb.blocket.se"
        specific = card.find(
            "a", class_="sc-bc48e3a4-0 hwRjcc sc-b071b343-1 fpcmct"
        )["href"]
        card_link = prefix + specific

        job_page = self.scrape(url=card_link)
        description = self.get_description_text(job_page)
        application_link = self.get_application_link(job_page)

        if application_link is None:
            application_link = card_link

        job = {
            "title": title,
            "company": company,
            "link": application_link,
            "description": description,
        }
        return job

    def get_description_text(self, job_page) -> str:
        """
        The format on each job application is very inconsistent.
        Some pages have all text within one paragraph.
        Others might be a bunch of paragraphs, strong, list etc.
        This method extracts the job description from the closest
        shared parent I could find.
        With that, we got some text we didn't want.
        These tags are defined within 'ignore_classes'.
        """
        # This was the closest uniform class name I could find.
        parent = job_page.find("div", class_="sc-5fe98a8b-12 fyLthZ")

        if not parent:
            print(
                "Something went wrong when looking for job description: "
                "Parent div not found"
            )
            sys.exit(1)

        text_content = []

        # Excluded from the parent div
        ignore_classes = [
            "sc-b08acc7e-1 eROHBI",  # "Anmäl annons"
            "sc-d7bf9244-0 bGhufW",  # "Denna annons kommer från..."
            "sc-dbdab9bd-0 betiZj",  # "Länk till ansökning"
        ]

        def extract_text(element):
            """
            This separates the bs4 elements within out parent div,
            ignores them if they match anything in 'ignore_classes'
            and appends it to text_content.
            """
            for child in element.children:
                if isinstance(child, NavigableString):
                    text = child.strip()

                    if text:
                        text_content.append(text)

                elif child.name not in ["script", "style"]:
                    class_string = " ".join(child.get("class", []))

                    if class_string in ignore_classes:
                        continue
                    extract_text(child)

        extract_text(parent)

        full_text = "\n".join(text_content)
        full_text = re.sub(r"\s", " ", full_text).strip()
        return full_text

    def get_application_link(self, job_page) -> str:
        application_link = job_page.find("a", class_="sc-dbdab9bd-0 betiZj")[
            "href"
        ]
        return application_link
