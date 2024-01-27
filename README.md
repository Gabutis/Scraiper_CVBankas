# CVBankas Scraper

This Python web scraper is designed for educational purposes to extract job listings from [cvbankas.lt](https://www.cvbankas.lt), targeting specifically those related to information technology fields. It allows users to search for specific keywords within job descriptions, currently focusing on the keyword "Python".

## Features

- Scrape job listings from cvbankas.lt
- Search for job descriptions containing the word "Python"
- Configuration through `config.json` to set the desired city for job search
- Error logging to file for troubleshooting
- Output the job titles and links directly to the terminal

## Requirements

- Python 3.x
- Packages: `requests`, `beautifulsoup4`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Gabutis/Scraiper_CVBankas.git
   cd Scraiper_CVBankas

2. Set up a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   .\venv\Scripts\Activate  # On Windows
   source venv/bin/activate # On Unix or MacOS

2. Install the required packages:
   ```sh
   pip install -r requirements.txt

## Configuration

Before running the scraper, configure your search preferences in the config.json file. Specify the city where you want to search for jobs. If the city name is left blank or the city is not in the list, the scraper will search all available job listings.

## Usage

  Run the scraper with the following command:
  ```sh
  python -m scraiper.main
```
The job listings will be displayed in the terminal as they are processed.

## Output
The scraper currently prints the job titles and links to the terminal. No data is saved to files or databases at this stage.

Example output:

  ```sh
  2. Job Title: Programuotojas (Web Developer)
     Job Link: https://www.cvbankas.lt/programuotojas-web-developer-klaipedoje/1-6548227
     Does not contain 'Python'.
```
## Error Logs
Check the logs directory for the scraper.log file if you encounter any errors. The log file contains details about any issues the scraper has encountered during execution.

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to add new features, feel free to fork the repository and submit a pull request.

#### Some ideas for contribution:

Allow the scraper to write results to a file.
Extend configuration options to include different keywords for job searches.
Implement different job search filters besides "Informacinės technologijos".
License
This project is open-sourced under the MIT License.

## Contact
If you have any questions or need support with the scraper, please open an issue in the repository.
