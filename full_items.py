# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:05:51 2023

@author: tester
"""

import requests
import pandas as pd

cik = "CIK0000789019"

url = "https://data.sec.gov/api/xbrl/companyfacts/{}.json".format(cik)

headers = {"User-Agent": "miguelacostaperdomo@gmai.com"}

var = {"EarningsPerShareBasic","DividendsStock"}

response = requests.get(url, headers=headers)

data = response.json()["facts"]["us-gaap"]
data_df = pd.DataFrame(data)

df_transposed = data_df.transpose().reset_index()

df_transposed_filter = df_transposed.drop("units", axis=1)

df_transposed_filter.to_csv("full_items.txt", sep="|")


    