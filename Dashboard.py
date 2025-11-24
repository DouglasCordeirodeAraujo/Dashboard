import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

st.set_page_config(page_title="Meu Dashboard", layout="wide")

@st.cache_resource
def carregar_e_treinar():
    df = pd.read_csv('NSE-TATAGLOBAL11.csv', sep=',')

    data = df.sort_index(ascending=True)

    new_data = pd.DataFrame({'Date': data['Date'], 'Close': data['Close']})
    new_data.index = pd.to_datetime(new_data['Date'])
    new_data = new_data.drop(columns=['Date'])

    dataset = new_data.values
    train = dataset[0:987]
    valid = dataset[987:]

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60, len(train)):
        x_train.append(scaled_data[i-60:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=0)

    # Preparar dados de teste
    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(60, inputs.shape[0]):
        X_test.append(inputs[i-60:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    return new_data, closing_price

with st.spinner("Treinando modelo LSTM..."):
    new_data, closing_price = carregar_e_treinar()

# Exibir resultados
train = new_data[:987].copy()
valid = new_data[987:].copy()
valid['Predictions'] = closing_price
train['date'] = train.index
valid['date'] = valid.index

st.title("📈 Meu Primeiro Dashboard com LSTM")
st.write("""
Abaixo veremos os próximos passos
""")
st.write("""
 Previsão de Ações
""")

stocks_train = alt.Chart(train).mark_line().encode(
    x='date',
    y='Close'
)
stocks_valid = alt.Chart(valid).mark_line(color="green").encode(
    x='date',
    y='Close'
)
stocks_pred = alt.Chart(valid).mark_line(color="red").encode(
    x='date',
    y='Predictions'
)

st.altair_chart(stocks_train.interactive() + stocks_valid.interactive() + stocks_pred.interactive(), use_container_width=True)

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(train['date'], train['Close'], label='Treino')
ax.plot(valid['date'], valid['Close'], label='Validação')
ax.plot(valid['date'], valid['Predictions'], label='Previsão LSTM')
ax.legend()
st.pyplot(fig)
