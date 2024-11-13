import matplotlib.pyplot as plt
import yfinance as yf
from indicators import calculate_roc,calculate_rsi,calculate_bollinger_bands
import pandas as pd
from plot import plot_graph


tickers = ['TSLA', 'NVDA', 'MSFT', 'AMZN']  # Adjusted for fewer tickers
plot = False

def main():
    # List of tickers for the big tech companies, forming the MAMAA group

    ticker_data_frames = []
    stats = {}

    for ticker in tickers:
        # Download historical data for the ticker
        data = yf.download(ticker, period="1y", interval="1d")

        # Calculate the daily percentage change
        close = data['Close']
        upper, lower = calculate_bollinger_bands(close, window=14, num_of_std=2)
        width = upper - lower
        rsi = calculate_rsi(close, window=14)
        roc = calculate_roc(close, periods=14)
        volume = data['Volume']
        diff = data['Close'].diff(1)
        percent_change_close = data['Close'].pct_change() * 100

        # Create a DataFrame for the current ticker and append it to the list
        ticker_df = pd.DataFrame({
            ticker + '_close': close.squeeze(),
            ticker + '_width': width.squeeze(),
            ticker + '_rsi': rsi.squeeze(),
            ticker + '_roc': roc.squeeze(),
            ticker + '_volume': volume.squeeze(),
            ticker + '_diff': diff.squeeze(),
            ticker + '_percent_change_close': percent_change_close.squeeze(),
        })

        MEAN = ticker_df.mean()
        STD = ticker_df.std()

        # Keep track of mean and std
        for column in MEAN.index:
            stats[f"{column}_mean"] = MEAN[column]
            stats[f"{column}_std"] = STD[column]

        # Normalize the training features
        ticker_df = (ticker_df - MEAN) / STD

        ticker_data_frames.append(ticker_df)

    # Combine all the ticker DataFrames into a single DataFrame
    combined_df = pd.concat(ticker_data_frames, axis=1)

    # Convert the dictionary containing feature statistics to a DataFrame
    stats_df = pd.DataFrame([stats], index=['Statistics'])

    # Display the statistics DataFrame
    print("\nFeature Statistics:")
    print(stats_df)

    if plot:
        plot_graph(tickers,combined_df)



if __name__ == "__main__":
    main()
