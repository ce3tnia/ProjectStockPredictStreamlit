import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils import *
import yfinance as yf

st.set_page_config(
    page_title='Apple Stock Prediction',
    page_icon='📈',
    layout='centered')

st.title('Apple Inc Stock Prediction based on Historical Data')

# sidebar #
st.sidebar.write('Data as on [Yahoo Finance](https://finance.yahoo.com) exchange in USD')
option = st.sidebar.selectbox('What would you like to predicted?',('AAPL', 'APC.F', 'AAPL.MX'), key = 'tick')
st.sidebar.write('You selected:', st.session_state.tick)
today = date.today()
before = today - timedelta(days=4500)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
predict = st.sidebar.button('Predict')
st.sidebar.info('''This Project is used for only learning and development process. I don't encourage anyone 
to invest in stock based on any data represented here.😊👩🏻‍🎓👩🏻‍💻''')

# proccess #
rates = ['MXNUSD=X', 'EURUSD=X']
tickers = yf.Tickers(' '.join(rates))

low = 0
open = 1
close = 2
high = -1

exchange_low = []
for i in tickers.tickers:
    exchange_low.append(tickers.tickers[i].history(start=start_date, end=end_date).Low)
exchange_open = []
for i in tickers.tickers:
    exchange_open.append(tickers.tickers[i].history(start=start_date, end=end_date).Open)
exchange_close = []
for i in tickers.tickers:
    exchange_close.append(tickers.tickers[i].history(start=start_date, end=end_date).Close)
exchange_high = []
for i in tickers.tickers:
    exchange_high.append(tickers.tickers[i].history(start=start_date, end=end_date).High)
    
try:
    if predict:
        if start_date < end_date:
            if option == 'AAPL':    
                # get data
                stock_aapl = yf.download(option, start_date, end_date)
                stock_aapl.reset_index(inplace=True)

                # show data
                data_act()
                st.write(stock_aapl)

                # visualizations
                visual_data()
                plot_actual_data(stock_aapl['Date'], stock_aapl, option)

                # Extract price
                data_aapl = stock_aapl.filter(['Low','Open','Close','High','Volume'])
                dataset_aapl = data_aapl.values

                # Proccess prediction
                proccess(dataset_aapl, stock_aapl, option)

            elif option == 'APC.F':
                #Convert Low price
                exlow_df = pd.DataFrame(exchange_low).T
                exlow_df.columns = rates
                low_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Low.to_frame()
                data['ticker'] = option
                data['rating'] = exlow_df['EURUSD=X']
                data['Low'] = data['Low'] * data['rating'] 
                low_df = pd.concat([low_df, data], axis=0)

                #Convert Open price
                exop_df = pd.DataFrame(exchange_open).T
                exop_df.columns = rates
                open_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Open.to_frame()
                data['ticker'] = option
                data['rating'] = exop_df['EURUSD=X']
                data['Open'] = data['Open'] * data['rating'] 
                open_df = pd.concat([open_df, data], axis=0)

                #Convert Close price
                excl_df = pd.DataFrame(exchange_close).T
                excl_df.columns = rates
                close_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Close.to_frame()
                data['ticker'] = option
                data['rating'] = excl_df['EURUSD=X']
                data['Close'] = data['Close'] * data['rating']
                close_df = pd.concat([close_df, data], axis=0)

                #Convert High price
                exhigh_df = pd.DataFrame(exchange_high).T
                exhigh_df.columns = rates
                high_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).High.to_frame()
                data['ticker'] = option
                data['rating'] = exhigh_df['EURUSD=X']
                data['High'] = data['High'] * data['rating'] 
                high_df = pd.concat([high_df, data], axis=0)

                #Volume
                volume_df = pd.DataFrame()
                data = yf.download(option, start=start_date, end=end_date, progress=False).Volume.to_frame()
                data['ticker'] = option
                volume_df = pd.concat([volume_df, data], axis=0)

                #concat
                stock_f = pd.DataFrame()
                stock_f = pd.concat([stock_f, low_df['ticker'], low_df['Low'], open_df['Open'], close_df['Close'], high_df['High'], volume_df['Volume']], axis=1)
                stock_f = stock_f.ffill()
                stock_f.reset_index(inplace=True)

                # show data
                data_act()
                st.write(stock_f)

                # visualizations
                visual_data()
                plot_actual_data(stock_f['index'], stock_f, option)

                # Extract price
                data_f = stock_f.filter(['Low','Open','Close','High','Volume'])
                dataset_f = data_f.values

                # Proccess prediction
                proccess(dataset_f, stock_f, option)

            else:
                #Convert Low price
                exlow_df = pd.DataFrame(exchange_low).T
                exlow_df.columns = rates
                low_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Low.to_frame()
                data['ticker'] = option
                data['rating'] = exlow_df['MXNUSD=X']
                data['Low'] = data['Low'] * data['rating'] 
                low_df = pd.concat([low_df, data], axis=0)

                #Convert Open price
                exop_df = pd.DataFrame(exchange_open).T
                exop_df.columns = rates
                open_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Open.to_frame()
                data['ticker'] = option
                data['rating'] = exop_df['MXNUSD=X']
                data['Open'] = data['Open'] * data['rating'] 
                open_df = pd.concat([open_df, data], axis=0)

                #Convert Close price
                excl_df = pd.DataFrame(exchange_close).T
                excl_df.columns = rates
                close_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).Close.to_frame()
                data['ticker'] = option
                data['rating'] = excl_df['MXNUSD=X']
                data['Close'] = data['Close'] * data['rating']
                close_df = pd.concat([close_df, data], axis=0)

                #Convert High price
                exhigh_df = pd.DataFrame(exchange_high).T
                exhigh_df.columns = rates
                high_df = pd.DataFrame()

                data = yf.download(option, start=start_date, end=end_date, progress=False).High.to_frame()
                data['ticker'] = option
                data['rating'] = exhigh_df['MXNUSD=X']
                data['High'] = data['High'] * data['rating'] 
                high_df = pd.concat([high_df, data], axis=0)

                #Volume
                volume_df = pd.DataFrame()
                data = yf.download(option, start=start_date, end=end_date, progress=False).Volume.to_frame()
                data['ticker'] = option
                volume_df = pd.concat([volume_df, data], axis=0)

                #concat
                stock_mx = pd.DataFrame()
                stock_mx = pd.concat([stock_mx, low_df['ticker'], low_df['Low'], open_df['Open'], close_df['Close'], high_df['High'], volume_df['Volume']], axis=1)
                stock_mx = stock_mx.ffill()
                stock_mx.reset_index(inplace=True)

                # show data
                data_act()
                st.write(stock_mx)

                # visualizations
                visual_data()
                plot_actual_data(stock_mx['index'], stock_mx, option)

                # Extract price
                data_mx = stock_mx.filter(['Low','Open','Close','High','Volume'])
                dataset_mx = data_mx.values

                # Proccess prediction
                proccess(dataset_mx, stock_mx, option)
        else:
            st.info('Please, end date must fall after start date🙏🏻')
    else:
        st.info('Please, choose the available options then click predict button🙏🏻')
except:
    st.error('Unable process data to prediction because it does not match system requirements, please choose again with more data the available options then click predict button🙏🏻')
