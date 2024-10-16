from scraper import BlocketScraper


"""
Maybe we should look into the GPT api and see what we can do with that.
Also; fix ruff next time will you, asshat?
"""

def run(url):
    data = BlocketScraper(url)
    jobs = data.jobs # list[dict[str:str]]

    # placeholder debugger
    for job in jobs:
        print(f"Title: {job["title"]}")
        print(f"Company: {job["company"]}")
        print(f"Description: {job["description"]}")
        print("-" * 50)


if __name__ == "__main__":
    url = "https://jobb.blocket.se/lediga-jobb?q=Python&filters=oerebro-laen"
    run(url)