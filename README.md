# Web Scraping and Social Media Scraping - Final project

Completed for the Web Scraping and Social Media Scraping course (2400-DS1WSMS) at the University of Warsaw, Faculty of Economic Sciences, MA in Data Science and Business Analytics program by:

- Vladimir Shargin (437981)
- Vadym Dudarenko (444820)
- Ivan Grakhovski (444422)

## Project description

The goal of the project is to scrape results for Formula 1 races for all of its history starting from the year 1950 until now. The data to be scraped includes basic information about the race itself (season, location, full name, date, track name), drivers’ finishing positions, team names, number of points gained, number of laps completed and time at finish.

Formula1.com is the official website for Formula 1, the starting page to be used in this project is the results archive: https://www.formula1.com/en/results/archive-1950-2016.html

## How to run the scrapers

### BeautifulSoup

`python beaгtifulsoup/parse.py`

### Selenium

`python selenium/parse.py [-h] [-l LIMIT] [--output-path OUTPUT_PATH]`

Optional arguments:
-   `-l LIMIT, --limit LIMIT`
                        Number of races to scrape, default is `100`. All races will be scraped if set to `-1`.
- `--output-path OUTPUT_PATH`
                        Output file name for race results.

### Scrapy

```
scrapy crawl years -o years.csv
scrapy crawl places -o places.csv
scrapy crawl data
```