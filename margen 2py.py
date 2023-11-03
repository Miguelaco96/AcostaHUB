# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:10 2023

@author: tester
"""
import pandas as pd


df1 = pd.read_csv('df_final.csv')
df1.add({"SYMBOL":"AAPL" , "DESCRIPTION" : "APPLE INC", "ticker":"AAPL", "cik":"CIK0000320193"})

df_names = pd.read_csv('sp500-nasdaq.csv', sep=";", encoding='latin1')


df_names.add({"SYMBOL":"AAPL" , "Name" : "Apple Inc", "Market":"NASDAQ-100"})

df_names["SYMBOL"] = df_names["Symbol"]




merged_df = df_names.merge(df1[['SYMBOL', 'cik']], on='SYMBOL', how='left')




merged_df.iloc[44] = {"Symbol":"AAPL" , "Name" : "Apple Inc", "Market":"S&P500","SYMBOL":"AAPL","cik":"CIK0000320193"}
merged_df.iloc[513] = {"Symbol":"AAPL" , "Name" : "Apple Inc", "Market":"NASDAQ-100","SYMBOL":"AAPL","cik":"CIK0000320193"}
#marg.append()

merged_df.to_csv("SPNasdaq.csv")
