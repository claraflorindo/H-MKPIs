from sqlalchemy import create_engine, engine, text
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import requests

from pathlib import Path
import streamlit_authenticator as stauth



    
user = "root"
passw = "123456"
host = "34.175.38.220"
database = "main"

server_url="https://api-dot-careful-ensign-377008.oa.r.appspot.com/"

#Conexion à la base de datos
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    #connect_args = {'connect_timeout': 10}
    )
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

conn = connect()

#Funcion Load data
#@st.cache_data
def load_data(_query):
    
    data = pd.json_normalize(_query, 'result')
    
    return data 

customers= load_data(requests.get(f'{server_url}api/v1/customers').json())
articles= load_data(requests.get(f'{server_url}/api/v1/articles').json())
transactions= load_data(requests.get(f'{server_url}/api/v1/transactions').json())



#Implementación de filtros
st.sidebar.write("FILTERS")
status_df=customers["club_member_status"].unique()
status_df=status_df[status_df!=np.array(None)]
status_lst = status_df.tolist()


status_filtered_lst = st.sidebar.multiselect(
    label = "STATUS",
    options = status_lst,
    default = status_lst,
    key = "multiselect_status"
)    





age_filtered_lst = st.sidebar.slider(
    'Select a range of ages',
    0, 100, (20, 80))

st.sidebar.write('Ages range selected:', age_filtered_lst)

customer_filtered= customers[customers['club_member_status'].isin(status_filtered_lst)]
customer_filtered=customer_filtered[(customer_filtered['age']>=age_filtered_lst[0]) & (customer_filtered['age']<=age_filtered_lst[1])]

st.dataframe(customer_filtered)

#KPI 1: What has each customer spent?
st.title('What has each customer spent?')
customer_spent = transactions.groupby(["customer_id"])["price"].sum()
st.bar_chart(transactions.groupby(["customer_id"])['price'].sum())

#KPI 2: How many purchases has each customer made
st.title('How many purchases has each customer made?')
purchases_per_customer=transactions.groupby(["customer_id"])["article_id"].count()
st.bar_chart(transactions.groupby(["customer_id"])["article_id"].count())

#KPI 3: Total earnings per colour
st.title('Total earnings per colour')
merge_df = pd.merge(articles, transactions, on='article_id', how='inner')

st.bar_chart(merge_df.groupby(['colour_group_name'])['price'].sum())
earnings_per_colour=merge_df.groupby(['colour_group_name'])['price'].sum()

#KPI 4: Total earnings per Club member status
st.title('Total earnings per Club member status')
merge_df2 = pd.merge(customer_filtered, transactions, on='customer_id', how='inner')
merge_df2=merge_df2.groupby(['club_member_status'])['price'].sum()
fig_colour = px.pie(merge_df2, values='price', names=merge_df2.index, title='Earnings per Club member status')
st.plotly_chart(fig_colour, use_container_width=True)





kpi1, kpi2, kpi3 = st.columns(3)

customer_spent2=customer_spent.mean()

kpi1.metric(
    label = "Average amount spent by customers",
    value = customer_spent2,
    delta = customer_spent2,
)

purchases_per_customer2=purchases_per_customer.mean()
kpi2.metric(
    label = "Average number of purchases for each customer",
    value = purchases_per_customer2,
    delta = purchases_per_customer2,
)


earnings_per_colour2=earnings_per_colour.max()
max_earnings_colour = earnings_per_colour[earnings_per_colour==earnings_per_colour2].index[0]

kpi3.metric(
    label = f"Max earnings colour : {max_earnings_colour}",
    value = earnings_per_colour2,
    delta = earnings_per_colour2,
)

