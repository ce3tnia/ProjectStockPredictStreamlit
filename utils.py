import streamlit as st
from plotly import graph_objs as go 
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import base64

low = 0
open = 1
close = 2
high = -1

def plot_actual_data(x_stock, stock, option):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_stock, y=stock['Low'], name='Low'))
    fig.add_trace(go.Scatter(x=x_stock, y=stock['High'], name='High'))
    fig.add_trace(go.Scatter(x=x_stock, y=stock['Open'], name='Open'))
    fig.add_trace(go.Scatter(x=x_stock, y=stock['Close'], name='Close'))
    fig.layout.update(title_text=option, xaxis_rangeslider_visible=True, hovermode = 'x')
    figv = go.Figure()
    figv.add_trace(go.Scatter(x=x_stock, y=stock['Volume']))
    figv.layout.update(title_text='Volume', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    st.plotly_chart(figv)
    
def plot_predict_data(dates_used, unscaled_y, y_pred):
    figl = go.Figure()
    figo = go.Figure()
    figc = go.Figure()
    figh = go.Figure()

    figl.layout.update(title_text=('Actual and Predicted on Low Price'), xaxis_rangeslider_visible=True, hovermode = 'x')
    figl.add_trace(go.Scatter(x=dates_used, y=unscaled_y[:,low], name='Actual Low Price'))
    figl.add_trace(go.Scatter(x=dates_used, y=y_pred[:,low], name='Predicted Low Price'))
    figo.layout.update(title_text=('Actual and Predicted on Open Price'), xaxis_rangeslider_visible=True, hovermode = 'x')
    figo.add_trace(go.Scatter(x=dates_used, y=unscaled_y[:,open], name='Actual Open Price'))
    figo.add_trace(go.Scatter(x=dates_used, y=y_pred[:,open], name='Predicted Open Price'))
    figc.layout.update(title_text=('Actual and Predicted on Close Price'), xaxis_rangeslider_visible=True, hovermode = 'x')
    figc.add_trace(go.Scatter(x=dates_used, y=unscaled_y[:,close], name='Actual Close Price'))
    figc.add_trace(go.Scatter(x=dates_used, y=y_pred[:,close], name='Predicted Close Price'))
    figh.layout.update(title_text=('Actual and Predicted on High Price'), xaxis_rangeslider_visible=True, hovermode = 'x')
    figh.add_trace(go.Scatter(x=dates_used, y=unscaled_y[:,high], name='Actual High Price'))
    figh.add_trace(go.Scatter(x=dates_used, y=y_pred[:,high], name='Predicted High Price'))
    
    st.plotly_chart(figl)
    st.plotly_chart(figo)
    st.plotly_chart(figc)
    st.plotly_chart(figh)

def convert_df(df):
    return df.to_csv()
    
def csvdata(option, stock, y_pred):
    datapred = pd.DataFrame(y_pred)
    datapred.rename(columns = {0:'Low',1:'Open',2:'Close',3:'High'}, inplace = True)
    data = pd.concat([stock,datapred], axis=1)
    csv = convert_df(data)
    b64 = base64.b64encode(csv.encode('utf-8')).decode()
    file_name = 'Data_{}.csv'.format(option)
	# st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download data actual and prediction as CSV</a>'
    st.markdown(href,unsafe_allow_html=True)

def evaluation(unscaled_y, y_pred, indexc, len_data):
    mae = mean_absolute_error(unscaled_y[:,indexc], y_pred[:,indexc])
    rmse = math.sqrt(mean_squared_error(unscaled_y[:,indexc], y_pred[:,indexc]))
    mape = mean(abs((unscaled_y[:,indexc] - y_pred[:,indexc])/unscaled_y[:,indexc]))*100

    prermspe = ((y_pred[:,indexc] - unscaled_y[:,indexc])/unscaled_y[:,indexc])
    rmspe_data = array([None]*len(len_data))
    for i in range(len(len_data)):
        rmspe_data[i] = math.pow(prermspe[i],2)
    rmspe = math.sqrt(mean(rmspe_data))*100
    st.write('MAE:', mae, '  \nRMSE:', rmse, '  \nMAPE:', mape, '  \nRMSPE:', rmspe)

def forcast(model, normalizedData, num_data, y_normaliser):
    data_pred = normalizedData[num_data-200:,:5].reshape(5,40,5)
    ylow,yopen,yclose,yhigh = model.predict(data_pred[[4]])
    yhat = ylow,yopen,yclose,yhigh
    nextday_pred = hstack((yhat))
    nextday_pred = y_normaliser.inverse_transform(nextday_pred)
    nextday_pred = {'Low':nextday_pred[0][0], 'Open':nextday_pred[0][1], 'Close':nextday_pred[0][2], 'High':nextday_pred[0][3]}
    st.write('🙌🏻Next day stock price forecast:', nextday_pred)

def write_low():
    st.write('Evaluation of low price')
def write_open():
    st.write('Evaluation of open price')
def write_close():
    st.write('Evaluation of close price')
def write_high():
    st.write('Evaluation of high price')
def data_act():
    st.subheader('Data Actual')
def visual_data():
    st.subheader('Visualizations Data')
def visual_actpred_data():
    st.subheader('Visualizations Actual and Prediction Data')
def write_evaluation():
    st.subheader('Evaluation')
    
def proccess(dataset, stock, option):
    # Preprocess the data
    num_days_used = 40
    normalizer = MinMaxScaler(feature_range=(0,1)) # instantiate scaler
    normalizedData = normalizer.fit_transform(dataset) # values between 0,1

    # Storing the number of data points in the array
    num_data = len(normalizedData)
    data_used = np.array([normalizedData[i : i + num_days_used].copy() for i in range(num_data - num_days_used)])
    dates_used = stock.index[num_days_used:num_data]
    y_normaliser = MinMaxScaler()
    y_normaliser.fit(stock[['Low', 'Open', 'Close', 'High']].to_numpy()[num_days_used:])

    # Splitting the dataset up into train and test sets
    X_test = data_used[0:, :, :]
    unscaled_y = stock[['Low', 'Open', 'Close', 'High']].to_numpy()[(num_days_used):][0:, :]
    
    # load model
    if option == 'AAPL':
        model = load_model('modelaapl.h5')
    elif option == 'APC.F': 
        model = load_model('modelf.h5')
    else:
        model = load_model('modelmx.h5')

    # modelpredict
    y_low_pred, y_open_pred, y_close_pred, y_high_pred = model.predict(X_test)
    testpreds_arr = hstack((y_low_pred, y_high_pred, y_open_pred, y_close_pred))
    y_pred = y_normaliser.inverse_transform(testpreds_arr)

    visual_actpred_data()
    plot_predict_data(dates_used, unscaled_y, y_pred)
        
    # data to csv
    csvdata(option, stock, y_pred)
    st.info('✍🏻Note: The amount of data is not the same because there are 40 initial data used as model input.👌🏻')
    
    #evaluation
    write_evaluation()
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        write_low()
        evaluation(unscaled_y, y_pred, low, data_used)
    with col2:
        write_open()
        evaluation(unscaled_y, y_pred, open, data_used)
    with col3:
        write_close()
        evaluation(unscaled_y, y_pred, close, data_used)
    with col4:    
        write_high()
        evaluation(unscaled_y, y_pred, high, data_used)
    
    #forcasting
    forcast(model, normalizedData, num_data, y_normaliser)
