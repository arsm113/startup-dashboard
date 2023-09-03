import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide', page_title='Startup Analysis')
df =pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year


def load_overall_analysis():
    st.title('Overall Analysis')
    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #avg ticket size
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    #total funded startups
    num_startups = df['startup'].nunique()
    col1, col2,col3,col4 =st.columns(4)
    with col1:
        st.metric('Total', str(total)+' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups', str(num_startups))

    st.header('MOM Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':

        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['year'].astype('str') + '-' + temp_df['month'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investors')
    st.dataframe(last5_df)
    col1, col2 = st.columns(2)
    with col1:

        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        # st.dataframe(big_df)
        fig, ax =plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        # st.dataframe(big_df)
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY investment')
    # st.dataframe(big_df)
    fig2, ax2 = plt.subplots()
    ax1.plot(year_series.index,year_series.values)
    st.pyplot(fig2)
# df['Investors Name']= df['Investors Name'].fillna('Undisclosed')
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option=='Overall Analysis':
    load_overall_analysis()
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
