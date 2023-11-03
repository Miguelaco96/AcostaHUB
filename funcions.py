# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 18:12:20 2023

@author: tester
"""

import requests
import yfinance as yf
import pandas as pd
import time


def search_ticker(cik,item,headers):
    
    response = requests.get("https://data.sec.gov/api/xbrl/companyfacts/{}.json".format(cik), headers=headers)
    time.sleep(0.5)
    try:
        
        if item  == "EarningsPerShareBasic" or item =="EarningsPerShareDiluted":
            data = pd.json_normalize(response.json()["facts"]["us-gaap"][item]["units"]["USD/shares"]).dropna()
            return data[["val", "frame"]]
        else:
            data = pd.json_normalize(response.json()["facts"]["us-gaap"][item]["units"]["USD"]).dropna()
            return data[["val", "frame"]]
    except KeyError:
        
        data = None
      
    
def search_cik(name, df_names):
        
    cik = df_names[df_names["Name"] == name]['cik'].values[0]
    
    return str(cik)



def history_data(ticker, period_item, interval_item):
    data = yf.Ticker(ticker)
    
        
    hist = data.history(period=period_item, interval=interval_item)
    
    
    
    return hist.reset_index()


def yf_ticker(ticker):
    
    data = yf.Ticker(ticker)
    
    return data

def cash_flow_data(ticker):
    
    dft= yf_ticker(ticker).cash_flow
        
    
    return dft.T

def earn_data(ticker):
    
   earn = yf_ticker(ticker).earnings_dates
   
   date_list=[]
   
   for date in earn.index:
       
       date_list.append(date.date())
             
   earn["Date"] = date_list    
   earn = earn.set_index("Date")
   earn = earn.dropna(how = "all")
   return earn.iloc[1:]



def divs_data(ticker):
    
   divs = yf_ticker(ticker).actions
   
   date_list=[]
   
   for date in divs.index:
       
       date_list.append(date.date())
             
   divs["Date"] = date_list    
   
   divs = divs.set_index("Date")
   
   divs = divs.dropna(how = "all")
   
   return divs["Dividends"].iloc[-15:]





def ebit_data(ticker):
    
    ebit = yf_ticker(ticker).financials
    
    
    ebit_data = ebit.loc[["Normalized EBITDA", "EBITDA","EBIT"]]
    
    return ebit_data.T



def ticker_selector(name, df_names): 
    
    
    ticker = df_names[df_names["Name"] == name]['SYMBOL'].values[0]
    
    return ticker
