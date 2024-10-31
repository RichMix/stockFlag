# stock flag python scripts


# Load the stock log file to examine abnormal stock price fluctuations and identify any unusual behavior.
# Displaying first few lines to understand structure for analysis

file_path = '/mnt/data/stocks.log'
with open(file_path, 'r') as file:
    stock_log_sample = [next(file) for _ in range(10)]  # Read first few lines for structure inspection

stock_log_sample

['| Time       | Ticker | Price   | Change |\n',
 '|------------|--------|---------|--------|\n',
 '\n',
 '| 10:00:01 | FZGB | 97.40 | -1.6 |\n',
 '| 10:00:02 | DWSU | 92.35 | 1.35 |\n',
 '| 10:00:03 | ZAKY | 98.30 | 0.3 |\n',
 '| 10:00:04 | UDXC | 90.05 | 0.05 |\n',
 '| 10:00:05 | UPUU | 101.55 | 1.55 |\n',
 '| 10:00:06 | VHUQ | 98.85 | -1.15 |\n',
 '| 10:00:07 | JNPQ | 100.50 | 0.5 |\n']


# The stock log file contains the following columns:
# Time: Time of each entry.
# Ticker: Stock ticker symbol.
# Price: Stock price at that moment.
# Change: Price change compared to a previous entry, which might indicate volatility.
# To detect abnormal behavior, analyze the file by:

# Identifying tickers with extreme price fluctuations.
# Checking for any unusually high frequency of changes in either price or change rate.

import pandas as pd

# Load the entire log into a DataFrame, skipping any irrelevant lines such as headers and blank lines
stock_data = pd.read_csv(file_path, delimiter="|", skiprows=3, skipinitialspace=True, names=["Time", "Ticker", "Price", "Change"])

# Cleaning up extra whitespace and converting data types for analysis
stock_data['Time'] = stock_data['Time'].str.strip()
stock_data['Ticker'] = stock_data['Ticker'].str.strip()
stock_data['Price'] = pd.to_numeric(stock_data['Price'], errors='coerce')
stock_data['Change'] = pd.to_numeric(stock_data['Change'], errors='coerce')

# Calculating metrics to identify abnormal behavior
# Identifying tickers with the largest absolute change values as a primary indicator of abnormal behavior
abnormal_tickers = stock_data.groupby('Ticker')['Change'].agg(['mean', 'std', 'max', 'min', 'count'])
abnormal_tickers['abs_max_change'] = abnormal_tickers[['max', 'min']].abs().max(axis=1)

# Identify the ticker with the maximum absolute change as a strong indicator of unusual activity
abnormal_ticker = abnormal_tickers['abs_max_change'].idxmax()
abnormal_ticker, abnormal_tickers.loc[abnormal_ticker]