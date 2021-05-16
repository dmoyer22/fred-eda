import pandas as pd 
import streamlit as st 
from fredapi import Fred 
import datetime
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
from dataprep.eda import create_report
from pandas_profiling import ProfileReport
import webbrowser

api_key  = '<your api key here>'

st.set_page_config(page_title='FRED EDA App', page_icon=None, layout='centered', initial_sidebar_state='auto')

st.header("Fred Data and EDA App")

task_dropdown = st.sidebar.selectbox(
"What would like to do? ",
('Quick Review of Fred Data' , 'Full EDA', 'Save EDA Reports', 'Create a .csv file'))

if st.sidebar.button('Visit fred.stlouisfed.org'):
    url = 'https://fred.stlouisfed.org/'
    webbrowser.open(url,new=2)


def get_date_range():
    today = datetime.date.today()
    year_ago = today - datetime.timedelta(days=365)
    start_date = st.date_input('Start date', year_ago)
    end_date = st.date_input('End date', today)
    if start_date > end_date or start_date > today :
        st.error('Error: End date must fall after start date.')
    return start_date, end_date

def get_fred_details():
    fred = Fred(api_key=api_key)
    x = pd.DataFrame()

    x = fred.search('SP500', limit=1)
    SP500_details = pd.DataFrame(x)
    
    x = fred.search('LRUN64TTUSM156S', limit=1)
    UR_Details = pd.DataFrame(x)

    x = fred.search('USACPIALLMINMEI', limit=1)
    CPI_details =  pd.DataFrame(x)
    
    x = fred.search('VIXCLS', limit=1)
    VIX_details = pd.DataFrame(x)

    x = fred.search('UMCSENT', limit=1)
    UMCS_Details = pd.DataFrame(x)

    return SP500_details, UR_Details, CPI_details, VIX_details, UMCS_Details

def format_descriptions(df):
    
    title = df['title']
    frequency = df['frequency']
    units = df['units']
    notes = df['notes']
        
    st.write(title)
    st.write(frequency)
    st.write(units)
    st.write(notes)
        

def get_fred_data(start,end):

    data = {}
    fred = Fred(api_key=api_key)
    sp500 = fred.get_series('SP500', observation_start = start_date, observation_end = end_date)
    data['SP500'] = fred.get_series('SP500', observation_start = start_date, observation_end = end_date)
        
    unemployment = fred.get_series('LRUN64TTUSM156S', observation_start = start_date, observation_end = end_date)
    data['UnemploymentRate'] = fred.get_series('LRUN64TTUSM156S', observation_start = start_date, observation_end = end_date)
    
    cpi = fred.get_series('USACPIALLMINMEI', observation_start = start_date, observation_end = end_date)
    data['ConsumerPriceIndex'] = fred.get_series('USACPIALLMINMEI', observation_start = start_date, observation_end = end_date)
    
    vix = fred.get_series('VIXCLS', observation_start = start_date, observation_end = end_date)
    data['VIX'] = fred.get_series('VIXCLS', observation_start = start_date, observation_end = end_date)
   

    umcs = fred.get_series('UMCSENT', observation_start = start_date, observation_end = end_date)
    data['ConsumerSentiment'] = fred.get_series('UMCSENT', observation_start = start_date, observation_end = end_date)
    
    datadf = pd.DataFrame(data) 

    return sp500, unemployment, cpi, vix, umcs, datadf


if task_dropdown == 'Quick Review of Fred Data':

    st.write('What is your date range?')
    start_date, end_date = get_date_range()

    sp500, unemployment, cpi, vix, umcs, datadf = get_fred_data(start_date,end_date)
    
     
    if st.checkbox("Show Descriptions"):
        SP500_Details, UR_Details, CPI_Details, VIX_Details, UMCS_Details = get_fred_details()

        st.subheader('S & P 500')
        format_descriptions(SP500_Details)
        st.line_chart(sp500)
        
        #Unemployment Rate: Aged 15-64: All Persons for the United States (LRUN64TTUSM156S)
        st.subheader('Unemployment Rate: Aged 15-64')
        format_descriptions(UR_Details)
        st.line_chart(unemployment)

        #Consumer Price Index: All Items for the United States (USACPIALLMINMEI)
        st.subheader('Consumer Price Index')
        format_descriptions(CPI_Details)
        st.line_chart(cpi)

        #CBOE Volatility Index: VIX (VIXCLS)
        st.subheader('Volatility Index - VIX')
        format_descriptions(VIX_Details)
        st.line_chart(vix)

        #University of Michigan: Consumer Sentiment (UMCSENT)
        st.subheader('Univ of Michigan Monthly Consumer Sentiment')
        format_descriptions(UMCS_Details)
        st.line_chart(umcs)

    else:
        st.subheader('S & P 500')
        st.line_chart(sp500)

        #Unemployment Rate: Aged 15-64: All Persons for the United States (LRUN64TTUSM156S)
        st.subheader('Unemployment Rate: Aged 15-64')
        st.line_chart(unemployment)

        #Consumer Price Index: All Items for the United States (USACPIALLMINMEI)
        st.subheader('Consumer Price Index')
        st.line_chart(cpi)

        #CBOE Volatility Index: VIX (VIXCLS)
        st.subheader('Volatility Index - VIX')
        st.line_chart(vix)

        #University of Michigan: Consumer Sentiment (UMCSENT)
        st.subheader('Univ of Michigan Monthly Consumer Sentiment')
        st.line_chart(umcs)

    

if task_dropdown == 'Full EDA':
    st.subheader('EDA')

    st.write('What is your date range?')
    start_date, end_date = get_date_range()
    sp500, unemployment, cpi, vix, umcs, datadf = get_fred_data(start_date,end_date)

    st.write('Two new tabs will open with your EDA results')
    create_report(datadf).show_browser()
       
    profile = ProfileReport(datadf, title="Fred Data Pandas Profiling Report", explorative=True)
    profile.to_file(f"Fred_Pandas_Profile_{start_date}_{end_date}.html")
    url = f"Fred_Pandas_Profile_{start_date}_{end_date}.html"
    webbrowser.open(url,new=2)

if task_dropdown == 'Save EDA Reports':
    st.subheader('Save a copy of your EDA Reports')

    st.write('What is your date range?')
    start_date, end_date = get_date_range()
    sp500, unemployment, cpi, vix, umcs, datadf = get_fred_data(start_date,end_date)
 
    if st.button('Submit'):
        st.subheader('Creating your EDA reports...')
        profile = ProfileReport(datadf, title="Fred Data Pandas Profiling Report", explorative=True)
        filename = f"Fred_Pandas_Profile_{start_date}_{end_date}.html"
        profile.to_file(filename)
        st.success(f"Your Pandas Profile Report has been saved: {filename}")
   
        filename = f"Fred_Dataprep_Report_{start_date}_{end_date}"
        report = create_report(datadf)
        report.save(filename)
        st.success(f"Your Fred dataprep Report has been saved: {filename}")


if task_dropdown == 'Create a .csv file':
    st.write('What is your date range?')
    start_date, end_date = get_date_range()

    sp500, unemployment, cpi, vix, umcs, datadf = get_fred_data(start_date,end_date)

    if st.button('Submit'):
        st.subheader('Creating an output dataset: .csv format')
        filename = f"fred_data_{start_date}_{end_date}.csv"
        datadf.to_csv(filename)
        st.success(f"Your file has been created: {filename}")
    