import json
import requests
from bs4 import BeautifulSoup
import logging
import functools
import os

project_root = os.path.dirname(os.path.dirname(__file__))

log_directory = os.path.join(project_root, 'logs')
os.makedirs(log_directory, exist_ok=True)

log_file_path = os.path.join(log_directory, 'scraper.log')
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file_path, encoding='utf-8')]
)
logger = logging.getLogger(__name__)

def log_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

@log_errors
def fetch_job_ad_details(job_link):
    try:
        response = requests.get(job_link)
        if response.status_code == 200:
            job_soup = BeautifulSoup(response.text, "html.parser")
            job_description_selector = "#jobad_content_main > section"
            job_description_element = job_soup.select_one(job_description_selector)
            if job_description_element:
                return job_description_element.get_text(strip=True)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job details: {e}")
    return ""

@log_errors
def fetch_job_ads(page_url):
    downloaded_html = requests.get(page_url)
    soup = BeautifulSoup(downloaded_html.text, "html.parser")
    job_ads = soup.select("div.list_a_wrapper > div:nth-child(1) > h3")
    return job_ads, soup

@log_errors
def process_job_ads(job_ads, start_number, seen_jobs):
    for n, job_ad in enumerate(job_ads, start=start_number):
        job_title = job_ad.get_text(strip=True)
        job_link_element = job_ad.find_parent("a")
        if job_link_element and "href" in job_link_element.attrs:
            job_link = job_link_element["href"]
            if job_link in seen_jobs:
                print("Detected a repeated job ad, stopping...")
                return None
            seen_jobs.add(job_link)
            job_description_text = fetch_job_ad_details(job_link)
            if "Python" in job_description_text:
                print(f"{n}. Job Title: {job_title}")
                print(f"    Job Link: {job_link}")
                print(f"    Contains 'Python' in the job description!")
            else:
                print(f"{n}. Job Title: {job_title}")
                print(f"    Job Link: {job_link}")
                print("    Does not contain 'Python'.")
            print()
    return n + 1

@log_errors
def load_config():
    config_path = os.path.join(project_root, 'config.json')
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


@log_errors
def load_valid_cities():
    valid_cities_path = os.path.join(project_root, 'data', 'valid_cities.json')
    with open(valid_cities_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@log_errors
def main():
    config = load_config()
    valid_cities = load_valid_cities()

    location_number = ""
    for number, city in valid_cities.items():
        if city == config["location_name"]:
            location_number = number
            break

    if location_number == "":
        print(f"City name {config["location_name"]} not found in the valid cities list, continuing without city location")
    else:
        print(f"City name '{config["location_name"]}' found with number: {location_number}")

    work_area = 76
    base_url = f"https://www.cvbankas.lt/?location%5B%5D={location_number}&padalinys%5B%5D={work_area}&page="
    page_num = 1
    job_count = 1
    seen_jobs = set()

    while True:
        page_url = f"{base_url}{page_num}"
        job_ads, _ = fetch_job_ads(page_url)
        if not job_ads:
            print(f"No more job ads found on page {page_num}. Stopping.")
            break
        result = process_job_ads(job_ads, job_count, seen_jobs)
        if result is None:
            break
        job_count = result
        page_num += 1

    print(f"Finished scraping. Processed {job_count} job ads.")


if __name__ == "__main__":
    main()
