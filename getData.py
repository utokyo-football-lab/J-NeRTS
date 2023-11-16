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


    dff = pd.DataFrame()
    for n in playername:
        df = pd.DataFrame([1])
        name=n.find(
            class_='gt_j').get_text(strip=True)
        df["name"] = name
        print(name)
        
        txt=""
        if n.find(class_='gt_j').find("a") is not None:
            url=n.find(class_='gt_j').find("a").get('href')
            txt=re.findall(r"pl=.*",url)
            txt=txt[0]
            print(txt)
            txt=txt[3:]
        df["player_id"]=txt
        dff = pd.concat([dff, df])
    dff.reset_index(inplace=True, drop=True)
    return dff


yearIDFile = "year.txt"

compIDKey = ["j", "j2", "j3"]
yearIDKey = ["2023","2022","2021","2020","2019","2018","2017"]


countComp, countYear = 0, 0

countAccess = 0
df = pd.DataFrame()
for year in yearIDKey:
    for comp in compIDKey:
        dfz = getDataFlame(comp, year)
        print(dfz)
        df = pd.concat([df, dfz])
        countAccess += 1
        if countAccess >= 15:
            df.reset_index(drop=True, inplace=True)
            df.to_pickle('./raw_playlog.pkl')
            df.to_csv('./raw_playlog.txt')
            print('15リクエストを超えるため、30秒間停止')
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
