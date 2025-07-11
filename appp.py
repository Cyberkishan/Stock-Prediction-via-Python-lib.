import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import streamlit as st

# Cache data loading
@st.cache_data
def load_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

st.title('Stock Trend Prediction')

# User inputs
user_input = st.text_input('Enter Stock Ticker', 'VEDL.NS')
start_date = '2014-01-01'
end_date = '2024-12-31'

# Load data
df = load_data(user_input, start_date, end_date)

# Basic Visualizations
st.subheader('Data Overview (2014-2024)')
st.write(df.describe())

st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

# Feature Engineering
df['MA_50'] = df['Close'].rolling(50).mean()
df['MA_200'] = df['Close'].rolling(200).mean()
df['Daily_Return'] = df['Close'].pct_change()
df['Volatility'] = df['Close'].rolling(30).std()

# Drop NA values
df = df.dropna()

# Prepare data for ML
X = df[['MA_50', 'MA_200', 'Daily_Return', 'Volatility']]
y = df['Close'].values

# Split data
split = int(0.8 * len(df))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Train Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Calculate error
mse = mean_squared_error(y_test, predictions)
st.write(f"Model Mean Squared Error: {mse:.2f}")

# Visualization of predictions
st.subheader('Random Forest Predictions vs Actual Prices')
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df.index[split:], y_test, 'b-', label='Actual Price')
ax.plot(df.index[split:], predictions, 'r--', label='Predicted Price')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
st.pyplot(fig)

# Feature Importance
st.subheader('Feature Importance')
importances = model.feature_importances_
features = list(X.columns)  # Explicit conversion to list of strings

fig, ax = plt.subplots(figsize=(10,5))
y_pos = np.arange(len(features))
ax.barh(y_pos, importances, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(features)
ax.invert_yaxis()  # Top feature at top
ax.set_xlabel('Importance Score')
ax.set_title('Feature Importance')
st.pyplot(fig)


#Box plot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Sample data structure — adjust as needed
summary_stats = pd.DataFrame({
    'Model_1': [130.7, 99.6, 21.5, 64.5, 91.9, 185.0, 504.6],
    'Model_2': [132.9, 101.1, 22.4, 65.7, 93.2, 188.6, 509.4],
    'Model_3': [128.6, 98.2, 20.4, 63.6, 90.2, 182.0, 498.8],
}, index=['Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'])

# Simulating predictions for visualization
import numpy as np
np.random.seed(42)
sample_preds = {
    model: np.random.normal(loc=summary_stats.loc['Mean', model],
                            scale=summary_stats.loc['Std', model],
                            size=2710)
    for model in summary_stats.columns
}

st.title("📈 Vedanta Stock Price Predictions (1-Week Forecast)")
st.write("Here’s a simple visual to understand how different models are forecasting Vedanta’s stock price.")

fig, ax = plt.subplots()
sns.boxplot(data=pd.DataFrame(sample_preds), ax=ax)
ax.set_title("Prediction Spread Across Models")
ax.set_ylabel("Predicted Stock Price")
st.pyplot(fig)


st.markdown("""
#### How to read this:

- 📍 **Each box shows where most predictions fall.** 
  The middle line is the median prediction.
  
- 📊 **Shorter boxes** mean the model is more confident.
  
- 🚩 **Longer whiskers or extreme dots** suggest the model sometimes predicts very different values — which could be worth investigating.
""")


reliability_scores = summary_stats.loc['Std'].sort_values()
best_model = reliability_scores.index[0]

st.success(f"✅ Based on the lowest standard deviation, **{best_model}** appears to offer the most consistent predictions.")

