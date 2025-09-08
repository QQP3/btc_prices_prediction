import requests
from bs4 import BeautifulSoup
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Step 1: Download the HTML
url = "https://finance.yahoo.com/quote/BTC-USD/history/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error: Failed to download HTML. Status code: {response.status_code}")
    exit()

# Step 2: Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Find all <tr> rows
rows = soup.find_all('tr')

# Step 4: Collect data into lists
data = []

for idx, row in enumerate(rows):
    cells = row.find_all('td')
    if len(cells) >= 5:
        date = cells[0].text.strip()
        final_price = cells[4].text.strip()
        data.append((date, final_price))

# Step 5: Create a pandas DataFrame
df = pd.DataFrame(data, columns=['Date', 'Final Price'])

# Step 6: Save to CSV
df.to_csv('btc_prices.csv', index=False, encoding='utf-8')

print("Success: Data has been saved to btc_prices.csv!")

# Load the historical data
df = pd.read_csv('btc_prices.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Final Price'] = df['Final Price'].str.replace(',', '')
df['Final Price'] = df['Final Price'].astype(float)
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# Build and fit ARIMA model
model = ARIMA(df['Final Price'], order=(10, 3, 3))
model_fit = model.fit()

# Forecast 20 days ahead
forecast = model_fit.forecast(steps=40)

# Create future dates
last_date = df.index[-1]
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=40)

# Create DataFrame for predictions
predicted_df = pd.DataFrame({
    'Date': future_dates,
    'Predicted Final Price': forecast
})

predicted_df.to_csv('btc_prices_predicted.csv', index=False, encoding='utf-8')
print("Success: forecast saved to btc_prices_predicted.csv")

# Select the last 120 days of real data
recent_real_data = df.iloc[-400:] if len(df) >= 400 else df

# Plot
plt.figure(figsize=(12,6))
plt.plot(recent_real_data.index, recent_real_data['Final Price'], color='blue', label='Last 367 Days Real Data')
plt.plot(predicted_df['Date'], predicted_df['Predicted Final Price'], color='green', linestyle='--', label='40 Days Predicted Data')
plt.title('Bitcoin Price Forecast: Last 367 Days + 40 Days Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('plot.png')

# (Optional) Display the plot
plt.show()

print("Success: Plot saved to plot.png!")
