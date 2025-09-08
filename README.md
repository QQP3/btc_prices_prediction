# Bitcoin Price Scraper and Forecasting Documentation
**Author:** Farbod Moayedzadeh Rad  
**Date:** June 11, 2025

---

## Webscript

### Introduction
This project gathers historical Bitcoin price data from Yahoo Finance, extracts the date and final closing price, and saves the information into a CSV file named `btc_prices.csv`.

### Libraries Used
- **requests**: To send HTTP requests and download the web page.
- **BeautifulSoup (bs4)**: To parse and navigate the HTML content.
- **pandas**: To create a DataFrame and save the data into a CSV file.

### Steps
1. Send an HTTP GET request to [Yahoo Finance BTC-USD history](https://finance.yahoo.com/quote/BTC-USD/history) using the `requests` library.  
2. Parse the received HTML content using `BeautifulSoup`.  
3. Find all `<tr>` tags, each representing a table row of historical data.  
4. For each row:
   - Extract the first column (Date) and the fifth column (Final Price).
   - Store the data into a Python list.
5. Convert the collected data into a `pandas` DataFrame.  
6. Save the DataFrame to a CSV file using UTF-8 encoding without including the index.  

### Conclusion
The script successfully extracts Bitcoin's historical data and saves it in a structured format for further analysis.  
If Yahoo Finance changes their web page structure in the future, small adjustments might be necessary.

---

## Bitcoin Price Forecasting with ARIMA Model

### Objective
After collecting the historical Bitcoin prices and saving them into `btc_prices.csv`, the next goal is to predict future Bitcoin prices using a time series model.  
We chose the **ARIMA model** for this forecasting task, applied on Bitcoin's daily returns to capture its real volatility.

### Libraries Used
- **pandas**: For loading and preprocessing the CSV file.
- **statsmodels**: For building and fitting the ARIMA time series model.
- **matplotlib**: For plotting the actual and predicted price data.

### Data Preparation
The data from `btc_prices.csv` was preprocessed by:
- Converting the `Date` column into datetime objects.
- Removing commas from the `Final Price` column and converting the values into float numbers.
- Sorting the dataset based on dates (ascending).
- Setting the `Date` column as the DataFrame index.

### Model Building
An **ARIMA(10,3,3)** model was selected, where:  

The model was fitted on the historical daily returns using the `ARIMA` class from the `statsmodels` library.

### Forecasting and Saving Predictions
After fitting the model:
1. The next **40 daily returns** were forecasted using the trained ARIMA model.
2. These returns were used to reconstruct future Bitcoin prices starting from the last known real price.
3. A new DataFrame was created with future dates and predicted prices.
4. The forecasted results were saved into a CSV file named `btc_prices_predicted.csv`.

### Plotting Real and Predicted Data
Using `matplotlib`, a plot was created to visualize the actual and forecasted Bitcoin prices:
- The last **367 days** of real Bitcoin price data were plotted with **blue solid lines**.
- The next **40 days** of forecasted Bitcoin prices were plotted with **green dashed lines**.
- The plot was saved as an image file named `plot.png`.

### Conclusion
By modeling Bitcoin's **daily returns** rather than its absolute prices, the **ARIMA(10,3,3)** model captured realistic market volatility and produced dynamic price predictions.  

The forecast results provide valuable short-term price insights and demonstrate a reliable approach to time series forecasting in volatile financial markets.

---

