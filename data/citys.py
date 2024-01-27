import json
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
    return None

def check_invalid_city(soup):
    invalid_city_text = "Skelbimų pagal Jūsų pasirinktus kriterijus nėra."
    message_container = soup.select_one("#main > div > div")
    if message_container:
        return invalid_city_text in message_container.text
    return False

def find_city_name(soup, location_number):
    city_name_container = soup.select_one(f"select[name='location[]'] option[value='{location_number}']")
    if city_name_container and city_name_container.text.strip():
        return city_name_container.text.strip()
    return None

def main():
    base_url = 'https://www.cvbankas.lt/?location%5B%5D={location_number}&page=1'
    location_number = 500
    consecutive_failures = 0
    max_failures = 100
    valid_cities = {}

    while consecutive_failures < max_failures:
        url = base_url.format(location_number=location_number)
        print(f"Fetching {url}")  # Debugging print statement
        soup = fetch_page(url)

        if soup and not check_invalid_city(soup):
            city_name = find_city_name(soup, location_number)
            if city_name:
                valid_cities[location_number] = city_name
                print(f"Found: Location Number: {location_number}, City Name: {city_name}")
                consecutive_failures = 0
            else:
                print(f"City name not found for location number: {location_number}")
                consecutive_failures += 1
        else:
            print(f"Invalid city or failed to fetch for location number: {location_number}")
            consecutive_failures += 1

        if consecutive_failures >= max_failures:
            print("Reached the maximum number of consecutive failures. Stopping.")
            break

        location_number += 1

    with open('valid_cities.json', 'w', encoding='utf-8') as f:
        json.dump(valid_cities, f, ensure_ascii=False, indent=4)

    print("Finished scraping. The valid city names and numbers have been saved to 'valid_cities.json'.")

if __name__ == "__main__":
    main()
