import pandas as pd
import numpy as np
from yahoo_historical import Fetcher
import time
from datetime import datetime

# Fetch list of equity symbols from NASDAQ
url1 = "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
data1 = pd.read_csv(url1)

# Fetch list of equity symbols from NYSE
url2 = "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
data2 = pd.read_csv(url2)

# Combine NASDAQ and NYSE symbols and remove duplicates
Symbols = pd.concat([data1['Symbol'], data2['Symbol']]).drop_duplicates().tolist()

# Get today's date
today = datetime.today()
today_date = [today.year, today.month, today.day]

# Specify a start date (example: 2 months before today)
start_date = datetime(today.year, today.month - 2, today.day)
start_date_list = [start_date.year, start_date.month, start_date.day]

# Calculate time for the run
t0 = time.time()

# Create an empty list to store individual DataFrames
data_frames = []

# Loop through each ticker and download the data
for symbol in Symbols:  
    print(symbol, end=', ', flush=True)  
    try:
        # Fetch historical stock data from start_date to today
        data = Fetcher(symbol, start_date_list, today_date)
        stock = data.getHistorical()
        
        # Check if the DataFrame is not empty
        if not stock.empty:
            stock['Name'] = symbol
            data_frames.append(stock)
        else:
            print(f"No data for {symbol}.")
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Concatenate all the DataFrames in the list
if data_frames:
    stock_final = pd.concat(data_frames, ignore_index=True, sort=False)
else:
    stock_final = pd.DataFrame()  # In case all requests failed

# Calculate total time taken
t1 = time.time()
total_time = t1 - t0

print(f"\nTotal time taken: {total_time:.2f} seconds")
