from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd

limit = True

source = request.urlopen('https://www.formula1.com/en/results.html/1990/drivers.html').read()
soup = BS(source,'lxml')
table = soup.find_all('table')[0] 
df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
df.drop(["Unnamed: 0","Unnamed: 6"],axis=1, inplace=True)
df.head()
df.plot.bar(x="Driver", y="PTS");


source = request.urlopen(f"https://www.formula1.com/en/results.html/1990/races/64/united-states/race-result.html").read()
soup = BS(source,'lxml')

table = soup.find_all('table')[0] 
df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
df.head()


def get_race_urls(year):
    YEAR = str(year)
    race_urls = []
    source = request.urlopen(f"https://www.formula1.com/en/results.html/{YEAR}/"f"races.html").read()
    soup = BS(source,'lxml')
    
    for url in soup.find_all('a'):
        if YEAR in str(url.get('href')) and 'race-result' in str(url.get('href')) and url.get('href') not in race_urls:
            race_urls.append(url.get('href'))
    return race_urls

def seasons_results(race_urls, year):
    df_f = pd.DataFrame()

    for n, race in enumerate(race_urls):

        results_page = request.urlopen(f"https://www.formula1.com{race}").read()
        race_results = BS(results_page,'lxml')

        try:
          table = race_results.find_all('table')[0] 
        except IndexError:
          continue
        df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
        df.drop(["Unnamed: 0","Unnamed: 8"], axis=1, inplace=True)
        df.set_index('No', inplace=True)
        
        div = race_results.find('div', attrs={'class': 'resultsarchive-content-header group'})
        s = div.text
        l = s.split('\n')
        

        df['SEASON'] = year
        df['RACE_NAME'] = race.split('/')[6].replace('-', ' ').upper()
        df['FULL_RACE_NAME'] = l[7][7:]
        if year > 2010:
          df['RACE_DATE'] = l[32]
          df['RACE_LOCATION'] = l[33]
        else:
          df['RACE_DATE'] = l[31]
          df['RACE_LOCATION'] = l[32]

        #establish season results df on first race information
        if n == 0:
          df_f = df
        else:
          df_f = df_f.append(df, ignore_index = True)
    
    return df_f

scraped_races = 0

for i in range(1950, 2023):
  if limit and scraped_races >= 100:
    break
  race_urls = get_race_urls(i)
  season_results_df = seasons_results(race_urls, i)

  if i == 1950:
    df = season_results_df
  else:
    df = df.append(season_results_df, ignore_index = True)
  
  scraped_races += len(race_urls)

df.to_csv('race_results.csv', index=False)
