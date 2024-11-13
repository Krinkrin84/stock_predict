import matplotlib.pyplot as plt

def plot_graph(tickers,combined_df):
    # Create a grid layout dynamically based on the number of tickers
    num_tickers = len(tickers)
    rows = (num_tickers + 1) // 2  # Dynamically decide the number of rows
    cols = 2  # 2 columns for subplots

    fig, axes = plt.subplots(rows, cols, figsize=(14, 6 * rows))

    # Flatten the axes array for easier iteration
    axes = axes.flatten()

    # Plot each stock's closing prices on separate subplots
    for i, ticker in enumerate(tickers):
        column_name = ticker + '_close'
        if column_name in combined_df.columns:
            axes[i].plot(combined_df.index, combined_df[column_name], label=ticker + ' Close')
            axes[i].set_title(f'{ticker} Closing Price')
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel('Normalized Stock Price')
            axes[i].grid(True)
            axes[i].legend()

    # Remove extra subplots if the number of tickers is less than the number of subplots
    if num_tickers < len(axes):
        for j in range(num_tickers, len(axes)):
            fig.delaxes(axes[j])

    # Adjust layout to prevent overlapping subplots
    plt.tight_layout()

    # Display the plot
    plt.show()
