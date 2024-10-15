from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from time import sleep
import sys
import requests
import logging

"""
Ruff is fucking my life right now
Fix it tmrw
good night
"""

class BlocketScraper():
    def __init__(self, url):

        self.url = url
        self.jobs = self.find_and_append()


    def find_and_append(self) -> list[dict[str]]:
        soup = self.scrape()
        cards = soup.find_all("div", class_="sc-b071b343-0 eujsyo")
        for card in cards:
            title = card.find("h2",class_="sc-f74edbc7-0 sc-6694485c-3 bZDiVh eUtWPK").string
            company = card.find("span",class_="sc-6694485c-5 hCmCSo").string
            link = ("https://jobb.blocket.se" +card.find("a", class_="sc-bc48e3a4-0 hwRjcc sc-b071b343-1 fpcmct")["href"])
            description = None # This needs to be not none
            job = {
                "Title": title,
                "Company": company,
                "Link": link,
                "Description": description
            }
            



    
    def scrape(self) -> BeautifulSoup:
        retry_amount = 3
        retry_delay = 5
        for attempt in range(retry_amount):
            logging.info("Requesting URL...")
            try:
                r = requests.get(self.url)
                r.raise_for_status()
                return BeautifulSoup(r.content, "html.parser")
            except RequestException as e:
                logging.error(f"Request failed (attempt {attempt +1}/{retry_amount}): {e}")
                if attempt < retry_amount:
                    logging.info(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
                else:
                    logging.error(f"Could not fetch data in {retry_amount} retries. Exiting program...")
                    sys.exit(1)







