import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Cleaned data is exported from py.notebook and is used
file = pd.read_csv('funding_clean.csv')
file['date']=pd.to_datetime(file['date'])
file['year']=file['date'].dt.year
file['month_year'] = pd.to_datetime(file['date'].dt.strftime('%B %Y'))
#Group by using two columns
file['month']=file['date'].dt.month

#Web page layout
st.set_page_config(layout='wide',page_title='Indian Starup Analysis')

#Analysis
#1. Investor Analysis
def load_investor(investor):
    st.subheader(investor)
    recent_inv = file[file['investor'].str.contains(investor)][['date','startup','sector','city','round','amount']].head()
    st.write('Recent Investments')
    st.dataframe(recent_inv)
    col1, col2 = st.columns(2)
    with col1:
 #Biggest Investment
       big_inv = file[file['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
       st.write('Biggest Investments')
       fig, ax = plt.subplots()
       ax.bar(big_inv.index,big_inv.values) # Since big_inv is a series.
       st.pyplot(fig)
    with col2:
 #sector wise distribution
       sector_inv = file[file['investor'].str.contains(investor)].groupby('sector')['amount'].sum()
       st.write('Sector wise Investment')
       fig1, ax1 = plt.subplots()
       ax1.pie(sector_inv,labels=sector_inv.index,autopct="%0.01f%%")
       st.pyplot(fig1)
#Year on Year Investment
    yoy_inv = file[file['investor'].str.contains(investor)].groupby('year')['amount'].sum()
    st.write('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(yoy_inv.index,yoy_inv.values)
    st.pyplot(fig2)

#2. Overall Analysis
def load_overall():
    st.subheader('Overall Analysis of Startup Funding')

    col3, col4,col5,col6,col7 = st.columns(5)
    #total Amount Funded
    with col3:
       a = round(file['amount'].sum())
       st.metric('Total Amount Funded(in Cr)',str(a)+' Cr')
    #total Number of Startups
    with col4:
       b = len(file['startup'].unique())
       st.metric('Total Startups',b)
    #Startup max. fund infused
    with col5:
        d = file.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).index[0]
        st.metric('Max funded Startup',d)
    #max amount infused in a startup
    with col6:
        c = file.groupby('startup')['amount'].sum().sort_values(ascending=False).max()
        st.metric('Max. fund Infused',str(c) + ' Cr')
    #Biggest Startup Investor
    with col7:
        e = file.groupby('investor')['amount'].sum().sort_values(ascending=False).idxmax()
        st.metric('Biggest Startup Investor',e)
    select = st.selectbox('select',['','amount','count'])
    if select == 'count':
        mom = file.groupby(['year','month'])['startup'].count().reset_index()
        mom['x_axis'] = mom['year'].astype('str') + '-' + mom['month'].astype('str')
        st.write('startup_count vs month')
        fig3, ax3 = plt.subplots()
        ax3.plot(mom['x_axis'], mom['startup'])
        st.pyplot(fig3)
    elif select == '':
        pass
    else:
        mom = file.groupby(['year','month'])['amount'].sum().reset_index()
        st.write('amount vs mount')
        mom['x_axis'] = mom['year'].astype('str') + '-' + mom['month'].astype('str')
        fig3, ax3 = plt.subplots()
        ax3.plot(mom['x_axis'], mom['amount'])
        st.pyplot(fig3)

    # mom['x_axis'] = mom['year'].astype('str') + '-' + mom['month'].astype('str')
    # fig3, ax3 = plt.subplots()
    # ax3.plot(mom['x_axis'], mom['amount'])
    # st.pyplot(fig3)


#Streamlit Code
st.title('Indian Startup Funding Data Analysis')
st.sidebar.title('Indian Startup_Funding')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    # bt0 = st.sidebar.button('Show overall analysis')
    # if bt0:
        load_overall()
elif option == 'Investor':
    inv = st.sidebar.selectbox('Select the Investor', sorted(set(file['investor'].str.split(',').sum()))) #Now,no 2names will be together
    st.header('Investor Details')
    bt1 = st.sidebar.button('See Details')
    if bt1:
        load_investor(inv)
elif option == 'Startup':
    s = st.sidebar.selectbox('Select The Company',sorted(file['startup'].unique().tolist()))
    bt1 = st.sidebar.button('See Details')
    st.header('Startup Details')
else:
   pass
