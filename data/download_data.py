import yfinance as yf
import pandas as pd

ticker = "BTC-USD"

df = yf.download(ticker, period="6mo", interval="1d")

df = df.dropna()
df.columns = df.columns.get_level_values(0)
df.columns = df.columns.str.lower()

df = df[['open', 'high', 'low', 'close', 'volume']]

df.reset_index(inplace=True)
df.rename(columns={"Date": "date"}, inplace=True)

df.to_csv("ohlc_clean.csv", index=False)

print("Data saved successfully!")
