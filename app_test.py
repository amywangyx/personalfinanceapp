# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:20:35 2020

@author: Amy
"""

import streamlit as st
import numpy as np
import pandas as pd

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
    @st.cache
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
        dt = st.date_input('Enter today date',key = i)
        ty = st.text_input('Expense / Income :',key = i)
        at = st.number_input('how much  ',key = i)
        cg = st.text_input('specific ones  ',key = i)
        df1 = pd.DataFrame(data = [[dt,ty,at,cg]],columns = ['Date','Type','Amount','Category'])
        df = pd.concat([df,df1],axis=0).drop_duplicates()
    df
    
    df.to_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')

def run_the_analysis():
    @st.cache
    def load_metadata(): 
        return pd.read_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv')
    stabledf= load_metadata()
    stabledf['Date'] = pd.to_datetime(stabledf['Date'])
    stabledf = stabledf.set_index('Date')
    stabledf= stabledf.sort_index()
    stabledf
    
    category_filter = st.selectbox('Which ones to include?',stabledf['Category'])
    filterdata = stabledf.loc[stabledf['Category']==category_filter]
    st.subheader('alldatamap')
    st.line_chart(stabledf.groupby(['Category']).mean())
    st.subheader('selected')
    st.bar_chart(filterdata['Amount'])

def run_to_budget():
    st.subheader('per month')
    @st.cache
    def read_and_clean_data():
        try: 
            df = pd.read_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv')
            st.write('read the file')
        except:
            
            df = pd.DataFrame(columns = ['StartingDate','Type','Category','Amount'])
            st.write('file is empty')
        return df
    df = read_and_clean_data()
    newdata = int(st.number_input('Enter the number of new budget lines today:'))
    for i in range(newdata):
        dt = st.date_input('Enter this budget starting date',key = i)
        ty = st.text_input('Expense / Income :',key = i)
        cg = st.text_input('specific ones  ',key = i)
        at = st.number_input('how much  ',key = i)
        df1 = pd.DataFrame(data = [[dt,ty,at,cg]],columns = ['StartingDate','Type','Category','Amount'])
        df = pd.concat([df,df1],axis=0).drop_duplicates()
    df.to_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')
    
if __name__ == "__main__":
    main()