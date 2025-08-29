import altair as alt
import pandas as pd
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import numpy as np
import datetime
from datetime import date, timedelta
import io
import matplotlib.pyplot as plt  
from auth_utils import require_auth, get_user_info

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


st.set_page_config(page_title="Charts", page_icon="📈")

if require_auth("Your Page Title"):
    # Your protected page content goes here
    user_info = get_user_info()
    
    st.title("Chart Maker")
    
    
    PaymentOption = st.selectbox(
        'What Payment Method Would You Like to See',
        (['card & bank','card', 'bank']))
    
    PaymentCard = st.selectbox(
        'What Payment Card Type Would You Like to See',
        (['all cards', 'amex', 'visa', 'mastercard', 'discover']))
    
    PaymentStatus = st.selectbox(
        'What Payment Status  Would You Like to See',
        ('charge & refund','charge', 'refund'))
    
    today = datetime.datetime.now()
    days180 = date.today() - timedelta(days=180)
    
    StartDate = st.date_input("Start Date (Default 180 Days Prior)", days180)
    EndDate = st.date_input("End Date", datetime.datetime.now())
    
    df = st.file_uploader("Select Your Local Transactions CSV (default provided)")
    if df is not None:
        df = pd.read_csv(df)
    else:
        st.stop()
    
    df2 = df[df['created_at'].str.split(expand=True)[1].isna() == False]
    dfbaddates = df[df['created_at'].str.split(expand=True)[1].isna() == True].copy()
    dfbaddates['created_at'] = dfbaddates['created_at'].apply(lambda x: datetime.datetime(1900, 1, 1, 0, 0, 0) + datetime.timedelta(days=float(x)))
    dfbaddates['created_at'] = pd.to_datetime(dfbaddates['created_at'])
    dfbaddates['created_at'] = dfbaddates['created_at'].dt.strftime('%m/%d/%y')
    df.loc[df['created_at'].str.split(expand=True)[1].isna() == False, 'created_at'] = df2['created_at'].str.split(expand=True)[0].str.strip()
    newdf = pd.concat([df2, dfbaddates])
    newdf['created_at'] = pd.to_datetime(newdf['created_at']).dt.date
    newdf2 = newdf.query("success == 1")
    df3 = newdf2.query("payment_method == 'card' | payment_method == 'bank'")
    df4 = df3.loc[:,['type', 'created_at', 'total', 'payment_person_name', 'customer_firstname', 'customer_lastname',\
                'payment_last_four', 'last_four', 'payment_method', 'channel', 'memo', 'payment_note', 'reference', \
                'payment_card_type', 'payment_card_exp', 'payment_bank_name', 'payment_bank_type',\
                'payment_bank_holder_type', 'billing_address_1', 'billing_address_2','billing_address_city', \
                'billing_address_state', 'billing_address_zip', 'customer_company','customer_email', 'customer_phone', \
                'customer_address_1','customer_address_2', 'customer_address_city', 'customer_address_state', \
                'customer_address_zip', 'customer_notes', 'customer_reference', 'customer_created_at', \
                'customer_updated_at', 'customer_deleted_at', 'gateway_id', 'gateway_name', 'gateway_type', \
                'gateway_created_at', 'gateway_deleted_at', 'user_name', 'system_admin', 'user_created_at',\
                'user_updated_at', 'user_deleted_at']]
    
    newdf4 = df4.copy()  # Make a copy of df4 to avoid modifying the original DataFrame
    newdf4['created_at'] = pd.to_datetime(newdf4['created_at'])
    newdf4['int_created_date'] = newdf4['created_at'].dt.year * 100 + newdf4['created_at'].dt.month
    
    if PaymentOption == 'card':
        newdf4 = newdf4[newdf4['payment_method'] == 'card']
    elif PaymentOption == 'bank':
        newdf4 = newdf4[newdf4['payment_method'] == 'bank']
    else:
        pass
    
    if PaymentCard == 'amex':
        newdf4 = newdf4[newdf4['payment_card_type'] == 'amex']
    elif PaymentCard == 'visa':
        newdf4 = newdf4[newdf4['payment_card_type'] == 'visa']
    elif PaymentCard == 'mastercard':
        newdf4 = newdf4[newdf4['payment_card_type'] == 'mastercard']
    elif PaymentCard == 'discover':
        newdf4 = newdf4[newdf4['payment_card_type'] == 'discover']
    else:
        pass
    
    
    #This is Working
    if PaymentStatus == 'charge':
        newdf4 = newdf4[newdf4['type'] == 'charge']
    elif PaymentStatus == 'refund':
        newdf4 = newdf4[newdf4['type'] == 'refund']
    else:
        pass
    
    
    StartDate = pd.to_datetime(StartDate)
    EndDate = pd.to_datetime(EndDate)
    
    newdf4 = newdf4[(newdf4['created_at'] >= StartDate) & (newdf4['created_at'] <= EndDate)]
    
    
    
    
    
    chart1 = alt.Chart(newdf4).mark_bar().encode(
        alt.X("total:Q", bin=True),
        y='count()',
    ).properties(
        title={
          "text": ["Count of Transactions"], 
          "subtitle": [f"Payment Option: {PaymentOption}", f"Payment Card: {PaymentCard}", f"Payment Status: {PaymentStatus}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
        },
        width=800,
        height=500
    )
    
    chart2 = alt.Chart(newdf4).mark_boxplot(extent='min-max').encode(
        x='int_created_date:O',
        y='total:Q'
    ).properties(
        title={
          "text": ["Box & Whisker By Month"], 
          "subtitle": [f"Payment Option: {PaymentOption}", f"Payment Card: {PaymentCard}", f"Payment Status: {PaymentStatus}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
        },
        width=800,
        height=500
    )
    
    
    #chart3 = alt.Chart(newdf4).mark_bar().encode(
    #    x='int_created_date:O',
    #    y='total:Q'
    #)
    
    
    #Need to work on grouping and such
    
    
    #Mean with months would be interesting visual
    #https://altair-viz.github.io/gallery/bar_chart_with_mean_line.html
    
    
    
    #cards/bank filter needed
    
    #payment_card_type
    #payment_method
    
    boxplot1 = newdf4.groupby(['int_created_date', 'type', 'payment_card_type', 'payment_method'])['total'].sum().reset_index()
    
    bar3 = alt.Chart(boxplot1).mark_bar().encode(
        x=alt.X('int_created_date:O', title='Date'),
        y=alt.Y('sum(total):Q', title='Total'),
        color=alt.Color('type:N', title='Payment Type')
    )
    
    #rule3 = alt.Chart(boxplot1).mark_rule(color='red').encode(
    #    y=alt.Y('mean(total):Q', title='Mean Total')
    #)
    
    #chart3 = (bar3 + rule3).properties(
    chart3 = (bar3).properties(
        title={
            "text": ["Box Plot Mean Transaction Per Month"], 
            "subtitle": [f"Payment Option: {PaymentOption}", f"Payment Card: {PaymentCard}", f"Payment Status: {PaymentStatus}", f"Start Date: {StartDate}", f"End Date: {EndDate}"],
        },
        width=800,
        height=500
    )
    
    #Bug with this atm I think its under y=alt.Y and should be a count() essentially
    
    #boxplot2 = newdf4.groupby(['int_created_date', 'type', 'payment_card_type', 'payment_method'])['total'].count().reset_index()
    
    bar4 = alt.Chart(newdf4).mark_bar().encode(
        x=alt.X('int_created_date:O', title='Date'),
        y=alt.Y('count(total):Q', title='Count'),
        color=alt.Color('type:N', title='Payment Type')
    )
    
    #bug here need to find the count mean
    #rule4 = alt.Chart(boxplot2).mark_rule(color='red').encode(
    #    y='mean(count(total)):Q'
    #)
    
    chart4 = (bar4).properties(
        title={
          "text": ["Box Plot Transaction Count Per Month"], 
          "subtitle": [f"Payment Option: {PaymentOption}", f"Payment Card: {PaymentCard}", f"Payment Status: {PaymentStatus}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
        },
        width=800,
        height=500
    )
    
    #MAYBE? It's by card type
    #chart3 = alt.Chart(newdf4).mark_bar(opacity=0.7).encode(
    #    x='int_created_date:O',
    #    y=alt.Y('total:Q').stack(None),
    #    color="payment_card_type",
    #)
    
    
    
    #Plot with Counts
    #plot with Totals
    
    tab1, tab2, tab3, tab4 = st.tabs(["Histogram", "Box and Whiskers", "Box Plot Sum", "Box Plot Count"])
    
    
    with tab1:
        st.altair_chart(chart1, use_container_width=True)
    with tab2:
        st.altair_chart(chart2, use_container_width=True)
    with tab3:
        st.altair_chart(chart3, use_container_width=True)
    with tab4:
        st.altair_chart(chart4, use_container_width=True)
    
    
    #https://altair-viz.github.io/gallery/bar_with_rolling_mean.html 
    #Look at this through lifetime + 180 Days?
    
    
    #https://altair-viz.github.io/gallery/distributions_and_medians_of_likert_scale_ratings.html
    
    
    #https://altair-viz.github.io/gallery/waterfall_chart.html
    
    
    #https://altair-viz.github.io/gallery/heat_lane.html
    
    
    
    
    
    
    
    
    
    
    
    
    #alt_chart = (
    #    alt.Chart(transactions, title="Scatterplot of Palmer's Penguins")
    #    .mark_circle()
    #    .encode(
    #        x=selected_x_var,
    #        y=selected_y_var,
    #        color="species",
    #    )
    #    .interactive()
    #)
    
    #st.altair_chart(alt_chart, use_container_width=True)
