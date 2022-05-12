from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--limit", help="Number of races to scrape, default is 100. All races will be scraped if set to -1.",
                    type=int,
                    default=100)
parser.add_argument("-o", "--output_path", help="Output file name.",
                    type=str,
                    default='output.csv')
args = parser.parse_args()

if args.limit == -1:
    limit = False
else:
    limit = True
    stop_at = args.limit

def parse_race(race_url): 
    race_results = []
    driver.get(race_url)

    # get race description
    season = driver.find_element(By.XPATH, "//a[@data-name=\"year\"][contains(concat(' ',normalize-space(@class),' '),' selected ')]").text
    race_name = driver.find_element(By.XPATH, "//a[@data-name=\"meetingKey\"][contains(concat(' ',normalize-space(@class),' '),' selected ')]").text
    full_race_name = driver.find_element(By.CLASS_NAME, 'ResultsArchiveTitle').text.replace(' - RACE RESULT', '')
    race_date = driver.find_element(By.CLASS_NAME, 'full-date').text
    race_location = driver.find_element(By.CLASS_NAME, 'circuit-info').text

    # get race results by driver    
    results_table_rows = driver.find_elements(By.XPATH, '//table[@class="resultsarchive-table"]//tr')
 
    for row in results_table_rows[1:]: # skipping the header
        race_results.append({'SEASON': season,
        'RACE_NAME': race_name,
        'FULL_RACE_NAME': full_race_name,
        'RACE_DATE': race_date,
        'RACE_LOCATION': race_location,
        'POS': row.find_element(By.XPATH, './td[2]').text,
        'DRIVER': row.find_element(By.XPATH, './td[4]').text,
        'CAR': row.find_element(By.XPATH, './td[5]').text,
        'LAPS': row.find_element(By.XPATH, './td[6]').text,
        'TIME': row.find_element(By.XPATH, './td[7]').text, 
        'PTS': row.find_element(By.XPATH, './td[8]').text})
    
    return race_results

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

url = 'https://www.formula1.com/en/results/archive-1950-2016.html'
driver.get(url)

# get list of year urls

year_urls = [el.get_attribute('href') for el in driver.find_elements(By.CSS_SELECTOR, r"a[data-name='year']")]

race_urls = []

for year_url in year_urls:
    # we don't need to collect more race urls than our scraping limit
    if limit and len(race_urls) >= stop_at:
        break
    driver.get(year_url)
    # get list of race urls
    # links starting at index 1 because the first link displays summary for all races of the season
    race_urls.extend([el.get_attribute('href') for el in driver.find_elements(By.CSS_SELECTOR, r"a[data-name='meetingKey']")][1:])

race_results = []
scraped_races = 0

for race_url in race_urls:
    # stop parsing if we've reached the limit
    if limit and scraped_races == stop_at:
        break
    
    race_results.extend(parse_race(race_url))
    scraped_races += 1

# close the window after we're done scraping
driver.close()

print(f'Total races scraped: {scraped_races}')

pd.DataFrame(race_results).to_csv(args.output_path, index=False)

print(f'Output saved at {args.output_path}')
