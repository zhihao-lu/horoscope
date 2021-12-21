from bs4 import BeautifulSoup
import requests
import pandas as pd
from date2horoscope import *
import json


def get_SP500(url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {
        'class': 'wikitable sortable'}).tbody  # find anything w both table and class:wiki, then in that, take out
    # things under the tbody tag

    rows = table.find_all('tr')  # find all things that are under a 'tr' tag in table

    columns = [v.text.replace('\n', '') for v in rows[0].find_all(
        'th')]  # for loop: turning each header (row[0]) into a column, repeating until all headers become own column

    df = pd.DataFrame(columns=columns)  # turn columns into dataframe

    for i in range(1, len(rows)):  # len(rows) = gets number of rows
        tds = rows[i].find_all('td')  # td = tag for company names and info

        if len(tds) == 8:  # counting how many td tag there is under each company
            values = [tds[0].text, tds[1].text.replace('\n', ''), tds[2].text, tds[3].text, tds[4].text, tds[5].text,
                      tds[6].text, tds[8].text, tds[9].text.replace('\n', '')]  # ERROR list index out of range
        else:
            values = [td.text for td in tds]

        df = df.append(pd.Series(values, index=columns),
                       ignore_index=True)  # adding the company names to the df everytime the loop is played
        df = df.replace(r'\n', '', regex=True)  # taking out the \n

    df['Date first added'] = pd.to_datetime(df['Date first added'], format='%Y-%m-%d',
                                            errors='coerce')  # changing dates from string to datetime format
    df['month'] = df['Date first added'].dt.month
    df['date'] = df['Date first added'].dt.day

    df = df.dropna(subset=['date', 'month'])
    df['stockbday'] = df.apply(lambda x: horoscope(x['date'], x['month']), axis=1)
    return df


def horoscopebday(day, month, df):
    userbday = horoscope(day, month)
    c_bday = compatibility[userbday]
    array = c_bday[:2]
    stock1 = df.loc[df['stockbday'].isin(array)]
    stock2 = stock1.Security.to_list()
    stock3 = stock1.stockbday.to_list()
    stock4 = list(zip(stock2, stock3))
    stock4 = [stock + " (" + bday + ")" for stock, bday in stock4]

    with open('horoscope_text.json') as f:
        d = json.load(f)
        text = d[userbday]

    return stock4, text

