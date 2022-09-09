from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def scraper(webAddress):
    '''
    this function opens up a specified url from basketball-reference.com,
    and scrapes the data using BeautifulSoup
    
    returns: a panda dataframe
    '''
    
    year = 2021                                         # the NBA season we will be analyzing

    html = urlopen(webAddress.format(year))             # the webAddress we will be scraping 
    soup = BeautifulSoup(html, features="lxml")         # returns a BeautifulSoup object
    soup.findAll('tr', limit=2)                         # use findALL() to get the column headers
                                                        # getText()to extract the text we need into a list

    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]                               # exclude the first column, we don't need it
    rows = soup.findAll('tr')[1:]                       # exclude the first header row

    player_stats = [[td.getText() for td in rows[i].findAll('td')]
        for i in range(len(rows))]

    return pd.DataFrame(player_stats, columns = headers)