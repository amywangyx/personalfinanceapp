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
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta

from forex_python.converter import CurrencyRates
c = CurrencyRates()
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def main():
    
    st.title('Personal Finance app')
    
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox('choose the app mode',["initialization","add new data","budgeting","run analysis"])
    if app_mode == "initialization":
        run_to_initialize()
    elif app_mode =='add new data':
        run_to_add_data()
    elif app_mode=='budgeting':
        run_to_budget()
    else:
        run_the_analysis()
#everytime hit clear cache and rerun to check the dataframe for new input
def run_to_initialize():
    st.subheader("please enter your bank account balance to make sure the budgeting tool is correctly functioned")
    if st.checkbox('Please be aware that all data are offline'):
        bankaccount = st.number_input('how much')
        bankdf = pd.DataFrame(data = [bankaccount],columns = ['initialamount'])
        bankdf.to_csv('C:\\Users\\Amy\\Desktop\\mybank.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')
    
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
            at = c.convert('CNY','USD',at1)  #needs to be updated = 2019/12/10
        
            
        else:    
            at = st.number_input('how much  ',key = i)
        
        category = st.selectbox('Big Category',['Food','Transportation','daily goods', 'shopping','n/a'],key=i)
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
    st.write('In total is $', round(thismonthdf.sum()[0],2))
    
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
    
    st.subheader('Compare with budgeting analysis')
    def load_metabudget(): 
        return pd.read_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv')
    budgetdf = load_metabudget()

    analysisdf = thismonthdf.merge(budgetdf,left_index =True, right_on = 'Category',suffixes = ('_spent','_budgeted'))
    analysisdf = analysisdf.set_index('Category')
    analysisdf
    
    st.subheader("how you've spent this month")
    fig2 = {
    'data': [go.Bar(x=analysisdf.index, y=analysisdf["Amount_budgeted"],name="Amount_budgeted"),
             go.Bar(x=analysisdf.index, y=analysisdf["Amount_spent"],name="Amount_spent")],
    'layout': go.Layout(barmode='overlay')
} 

    st.plotly_chart(fig2)
    
    st.subheader('Warning Section')
    currentyear = filterdata.index.year[0]

   
    for index,row in analysisdf.iterrows():
       
       last_date_of_month = datetime(currentyear, monthtoview, 1) + relativedelta(months=1, days=-1)
       delta = datetime.today() - datetime(currentyear,monthtoview,1)

       daysthismonth = last_date_of_month- datetime(currentyear,monthtoview,1)

       if delta/daysthismonth <= row['Amount_spent']/row['Amount_budgeted']:
           st.write('Category',index,'is over the proportion limit!!!')

def run_to_budget():
    st.subheader('per month')
    
    @st.cache(allow_output_mutation=True)
    def read_and_clean_data():
        try: 
            df = pd.read_csv('C:\\Users\\Amy\\Desktop\\myrecord.csv')
            st.write('read the file')
    
        except:
            
            df = pd.DataFrame(columns = ['Date','Type','Amount','Category'])
            st.write('file is empty')
        return df
    
    @st.cache(allow_output_mutation=True)
    def read_bank_statement():
        try: 
            df = pd.read_csv('C:\\Users\\Amy\\Desktop\\mybank.csv')
            st.write('read the file')
    
        except:
            
            df = pd.DataFrame(columns = ['initialamount'])
            st.write('file is empty')
        return df
    
    bdf = read_and_clean_data()
    bankdf = read_bank_statement()
    
    bdf['Date'] = pd.to_datetime(bdf['Date'])
    bdf = bdf.set_index('Date')
    bdf= bdf.sort_index()
    
    st.subheader('check the dataframe again')
    bdf
    
    st.subheader('Income subsection')
    incomedf = bdf.loc[bdf['Type']=='Income']
    incomedf
    
    monthtoview = st.selectbox('which month to view?',incomedf.index.month.drop_duplicates())
    thismonthbudget = incomedf.loc[incomedf.index.month ==monthtoview].sum()['Amount']
    st.write('This month you have budget of :',round(thismonthbudget,2))
    
    usebankaccount = st.selectbox('do you want to use a part of your bank saving?', ['yes','no'])
    if usebankaccount =='yes':
        trueamount = st.slider('by how much',0.,float(bankdf['initialamount'][0]),step = 1.0)
        thismonthbudgetfinal = trueamount + thismonthbudget
        st.write('This month final budget is :',round(thismonthbudgetfinal,2))
    else:
        thismonthbudgetfinal = thismonthbudget
        st.write('This month final budget is :',round(thismonthbudgetfinal,2))
    
    mybudgetdf = pd.DataFrame(columns = ['Category','Amount'])
    category1 = st.selectbox('For this category',bdf['Category'].drop_duplicates(),key =1)
    st.subheader('how do you want to split your budget')
    
    value1 = st.slider('Budget Range',0.,float(thismonthbudgetfinal),step = 1.0,key=1)

    df1= pd.DataFrame(data = [[category1,value1]],columns = ['Category','Amount'])
    mybudgetdf = pd.concat([mybudgetdf,df1],axis=0).drop_duplicates()
    
    category2 = st.selectbox('For this category',bdf['Category'].drop_duplicates(),key=2)
    st.subheader('how do you want to split your budget')
    value2 = st.slider('Budget Range',0.,float(thismonthbudgetfinal-value1),step = 1.0,key=2)

    df2= pd.DataFrame(data = [[category2,value2]],columns = ['Category','Amount'])
    mybudgetdf = pd.concat([mybudgetdf,df2],axis=0).drop_duplicates()
    
    category3 = st.selectbox('For this category',bdf['Category'].drop_duplicates(),key=3)
    st.subheader('how do you want to split your budget')
    value3 = st.slider('Budget Range',0.,float(thismonthbudgetfinal-value1-value2),step = 1.0,key=3)

    df3= pd.DataFrame(data = [[category3,value3]],columns = ['Category','Amount'])
    mybudgetdf = pd.concat([mybudgetdf,df3],axis=0).drop_duplicates()
    
    category4 = st.selectbox('For this category',bdf['Category'].drop_duplicates(),key=4)
    st.subheader('how do you want to split your budget')
    value4 = st.slider('Budget Range',0.,float(thismonthbudgetfinal-value1-value2-value3),step = 1.0,key=4)

    df4= pd.DataFrame(data = [[category4,value4]],columns = ['Category','Amount'])
    mybudgetdf = pd.concat([mybudgetdf,df4],axis=0).drop_duplicates()
    
    st.subheader('YOU LEFT WITH: ')
    st.write(round(thismonthbudgetfinal-value1-value2-value3-value4+bankdf['initialamount'][0]-trueamount))

    mybudgetdf.to_csv('C:\\Users\\Amy\\Desktop\\mybudget.csv',index=False)
    st.success('Save to file... Done!(using st.cache)')
    mybudgetdf
    
    
    
if __name__ == "__main__":
    main()