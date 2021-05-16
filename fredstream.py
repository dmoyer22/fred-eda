import pandas as pd 
import streamlit as st 
from fredapi import Fred 
import datetime
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
from dataprep.eda import create_report
from pandas_profiling import ProfileReport
import webbrowser

st.header("Fred API")

task_dropdown = st.sidebar.selectbox(
"What would like to do? ",
('Quick Review of Fred Data' , 'Full EDA'))

def get_date_range():
    today = datetime.date.today()
    year_ago = today - datetime.timedelta(days=365)
    start_date = st.date_input('Start date', year_ago)
    end_date = st.date_input('End date', today)
    if start_date > end_date or start_date > today :
        st.error('Error: End date must fall after start date.')
    return start_date, end_date

def get_fred_data(start,end):

    data = {}
    fred = Fred(api_key='<your api key>')
    sp500 = fred.get_series('SP500', observation_start = start_date, observation_end = end_date)
    data['SP500'] = fred.get_series('SP500', observation_start = start_date, observation_end = end_date)

    fred = Fred(api_key='<your api key>')
    unemployment = fred.get_series('LRUN64TTUSM156S', observation_start = start_date, observation_end = end_date)
    data['UnemploymentRate'] = fred.get_series('LRUN64TTUSM156S', observation_start = start_date, observation_end = end_date)

    fred = Fred(api_key='<your api key>')
    cpi = fred.get_series('USACPIALLMINMEI', observation_start = start_date, observation_end = end_date)
    data['ConsumerPriceIndex'] = fred.get_series('USACPIALLMINMEI', observation_start = start_date, observation_end = end_date)

    fred = Fred(api_key='<your api key>')
    vix = fred.get_series('VIXCLS', observation_start = start_date, observation_end = end_date)
    data['VIX'] = fred.get_series('VIXCLS', observation_start = start_date, observation_end = end_date)

    fred = Fred(api_key='<your api key>')
    umcs = fred.get_series('UMCSENT', observation_start = start_date, observation_end = end_date)
    data['ConsumerSentiment'] = fred.get_series('UMCSENT', observation_start = start_date, observation_end = end_date)

    datadf = pd.DataFrame(data)
    

    return sp500, unemployment, cpi, vix, umcs, datadf


if task_dropdown == 'Quick Review of Fred Data':

    st.write('What is your date range?')
    start_date, end_date = get_date_range()

    sp500, unemployment, cpi, vix, umcs, datadf = get_fred_data(start_date,end_date)

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
    report = create_report(datadf)
    # add report write

    
    profile = ProfileReport(datadf, title="Fred Data Pandas Profiling Report", explorative=True)
    profile.to_file(f"Fred_Pandas_Profile_{start_date}_{end_date}.html")
    url = f"Fred_Pandas_Profile_{start_date}_{end_date}.html"
    webbrowser.open(url,new=2)
