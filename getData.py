import pandas as pd
import requests
import json
import re
import ast
import datetime
import time
import pprint
import bs4
from urllib import request


def Condition_load(FILENAME):
    DF = pd.DataFrame()
    DF = pd.read_table(FILENAME)
    DF.reset_index
    return DF


def MakeURL(COMP, YEAR):
    url = "https://soccer-db.net/contents/{}_{}_newcomers.php".format(
        YEAR, COMP)
    print(url)
    return url


def convDataFrame(df1, df2):
    aaa = dict()
    aaa["Youth Team"] = df2.iat[0, 2]
    aaa["College"] = df1.iat[0, 3]
    df = pd.DataFrame.from_dict(aaa, orient='index').T
    return df


def getDataFlame(COMP, YEAR):
    url = MakeURL(COMP, YEAR)
    soup = bs4.BeautifulSoup(request.urlopen(
        url), 'html.parser')
    dfs = pd.read_html(url)
    playername = [
        n for n in soup.select("div.group_title")]
    teamname = [n.get_text()
                for n in soup.select("div.cp_middletitle")]

    dff = pd.DataFrame()
    for n in playername:
        df = pd.DataFrame([1])
        df["name"] = n.find(
            class_='gt_j').get_text(strip=True)
        a = n.next_sibling.next_sibling
        clubs_name = [b.previous_element.previous_element.previous_element.get_text(strip=True) for b in a.find_all(
            class_="w4 leftline")]
        clubs_link = [re.search(r'te=(\d+)', b.previous_element.previous_element.previous_element.previous_element.find("a").get("href")).group(1) for b in a.find_all(
            class_="w4 leftline")]

        clubs_name = list(dict.fromkeys(clubs_name))
        clubs_link = list(dict.fromkeys(clubs_link))

        for count, a in enumerate(clubs_name):
            df[f"club{count}_name"] = a
            df[f"club{count}_id"] = clubs_link[count]
        df.drop([0], axis=1, inplace=True)
        dff = pd.concat([dff, df])
    dff["year"] = YEAR
    dff["competition"] = COMP
    dff.reset_index(inplace=True, drop=True)
    return dff


yearIDFile = "year.txt"

compIDKey = ["j", "j2", "j3"]
yearIDKey = Condition_load(yearIDFile)


countComp, countYear = 0, 0

countAccess = 0
df = pd.DataFrame()
while countYear < len(yearIDKey):
    countComp = 0
    while countComp < len(compIDKey):
        comp = compIDKey[countComp]
        year = yearIDKey.iat[countYear, 1]
        dfz = getDataFlame(comp, year)
        print(dfz)
        df = pd.concat([df, dfz])
        countAccess += 1
        if countAccess >= 5:
            df.reset_index(drop=True, inplace=True)
            df.to_pickle('./raw_playlog.pkl')
            df.to_csv('./raw_playlog.txt')
            print('5リクエストを超えるため、30秒間停止')
            time.sleep(30.1)
            countAccess = 0
        countComp += 1
    countYear += 1

# df.reset_index(drop=True, inplace=True)
# df.to_pickle('./raw_newComerlog.pkl')
# df.to_csv('./raw_newComerlog.txt')

# comp = compIDKey.iat[1,1]
# year = yearIDKey.iat[0,1]
# team = teamIDKey.iat[1,1]

# df = getDataFlame(comp,year,team)
# print(df)

# comp = compIDKey.iat[1,1]
# year = yearIDKey.iat[1,1]
# team = teamIDKey.iat[1,1]

# df2 = getDataFlame(comp,year,team)

# print(df2)

# df = pd.concat([df,df2])
# print(df)
