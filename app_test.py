# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:20:35 2020

@author: Amy
"""

import streamlit as st
import numpy as np
import pandas as pd
import re
import json
import urllib.request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from currency_converter import CurrencyConverter
c = CurrencyConverter()

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    
    st.title('Personal Finance app')
    
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox('choose the app mode',["add new data","budgeting","run analysis"])
    if app_mode == "add new data":
        run_to_add_data()
    elif app_mode=='budgeting':
        run_to_budget()
    else:
        run_the_analysis()
#everytime hit clear cache and rerun to check the dataframe for new input
    
def run_to_add_data():
    @st.cache(allow_output_mutation=True)
    def read_and_clean_data():
        try: 
            df = pd.read_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv')
            st.write('read the file')
    
        except:
            
            df = pd.DataFrame(columns = ['Date','Type','Amount','Category'])
            st.write('file is empty')
        return df
    
    df = read_and_clean_data()
    


    newdata = int(st.number_input('Enter the number of new records today:'))

    
    for i in range(newdata):
        dt = st.date_input('Enter the date',key = i)
        ty = st.selectbox('Expense / Income :',['Expense','Income'],key = i)
        currency = st.selectbox('currency',['USD','RMB'],key=i)
        if currency =='RMB':
            
            at1 = st.number_input('how much  ',key = i)
            at = c.convert(at1,'CNY','USD')  #needs to be updated = 2019/12/10
        
            
        else:    
            at = st.number_input('how much  ',key = i)
        
        category = st.selectbox('Big Category',['Food','Transportation','daily goods', 'shopping'])
        cg = st.text_input('specific ones  ',key = i)
        
        rollover = st.selectbox('do you want to split this one into different month',['yes','no'],key=i)
        if (rollover == 'no'):
            df1 = pd.DataFrame(data = [[dt,ty,at,category,cg]],columns = ['Date','Type','Amount','Category','Description'])
        else: 
            df4 = pd.DataFrame(columns = ['Date','Type','Amount','Category','Description'])
            monthsnum = st.selectbox('how many months?',[2,3,4,5,6,12])
            df2 = pd.DataFrame(data= [[dt,ty,at/monthsnum,category,cg]],columns = ['Date','Type','Amount','Category','Description'])
            for i in range(1,monthsnum):
                df3 = pd.DataFrame(data= [[dt+relativedelta(months=+i),ty,at/monthsnum,category,cg]],columns = ['Date','Type','Amount','Category','Description'])
                
                df4 = pd.concat([df3,df4],axis=0).drop_duplicates()
            df1 = pd.concat([df4,df2],axis=0).drop_duplicates()
           
        df = pd.concat([df,df1],axis=0).drop_duplicates()
    df
    
    df.to_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')

def run_the_analysis():
    def load_metadata(): 
        return pd.read_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv')
    stabledf= load_metadata()
    stabledf['Date'] = pd.to_datetime(stabledf['Date'])
    stabledf = stabledf.set_index('Date')
    stabledf= stabledf.sort_index()
    stabledf
    
    
    monthtoview = st.selectbox('which month to view?',stabledf.index.month.drop_duplicates())
    
    st.subheader('What you have spent this month?')
    

    thismonthdf=stabledf.loc[stabledf.index.month ==monthtoview].groupby(['Category']).sum()
    thismonthdf
    st.write('In total is ', thismonthdf.sum()[0])
    
#    #------
#    print(thismonthdf[thismonthdf.index=='Food'].values)
#    comparison_labels = ['Food','daily goods','Transportaion']
#    comparison_values = [thismonthdf[thismonthdf.index==comparison_labels[0]].values,thismonthdf[thismonthdf.index==comparison_labels[1]].values,thismonthdf[thismonthdf.index==comparison_labels[2]].values]
#    comparison_values[0]
#    fig = go.Figure(data=[go.Pie(labels=['Food','daily goods','Transportaion'], values=[32,24,35])])
#    st.plotly_chart(fig) 
#    
    
    import plotly.express as px
    fig = px.pie(thismonthdf,values = 'Amount',names = thismonthdf.index)
    st.plotly_chart(fig)
    
    
    category_filter = st.selectbox('Which category to look deeper into?',stabledf['Category'].drop_duplicates())
    filterdata = stabledf.loc[(stabledf.index.month ==monthtoview) &(stabledf['Category']==category_filter)]
    st.subheader('selected')
    st.bar_chart(filterdata['Amount'])

def run_to_budget():
    st.subheader('per month')
    @st.cache(allow_output_mutation=True)
    def read_and_clean_data2():
        try: 
            bdf = pd.read_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv')
            st.write('read the file')
        except:
            
            bdf = pd.DataFrame(columns = ['StartingDate','Type','Category','Amount'])
            st.write('file is empty')
        return bdf
    bdf = read_and_clean_data2()
    newdata = int(st.number_input('Enter the number of new budget lines today:'))
    for i in range(newdata):
        dt = st.date_input('Enter this budget starting date',key = i)
        ty = st.text_input('Expense / Income :',key = i)
        cg = st.text_input('specific ones  ',key = i)
        at = st.number_input('how much  ',key = i)
        df1 = pd.DataFrame(data = [[dt,ty,at,cg]],columns = ['StartingDate','Type','Category','Amount'])
        bdf = pd.concat([bdf,df1],axis=0).drop_duplicates()
    
    bdf.to_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')
    bdf
    
if __name__ == "__main__":
    main()