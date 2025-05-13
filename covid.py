# COVID-19 Global Data Tracker
# This script loads and analyzes COVID-19 data globally.
# It visualizes cases, deaths, and vaccinations over time.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Enable inline plotting if you're in a Jupyter Notebook
# %matplotlib inline  # Uncomment if using Jupyter

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings("ignore")

# 1. Load Dataset
try:
    df = pd.read_csv("owid-covid-data.csv")
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print("❌ The file 'owid-covid-data.csv' was not found. Make sure it's in your current directory.")
    raise

# 2. Inspecting the Data
print("\n🔍 Previewing dataset:")
print(df.head())
print("\n📊 Column Info:")
print(df.info())

# 3. Data Cleaning
# Keep only selected countries to make analysis manageable
countries = ['South Africa', 'India', 'United States', 'Brazil']
df = df[df['location'].isin(countries)]

# Drop rows where date or key fields are missing
df.dropna(subset=['date', 'total_cases', 'total_deaths'], inplace=True)
df['date'] = pd.to_datetime(df['date'])

# Fill missing values in numerical columns with 0 or use interpolation
df['total_vaccinations'] = df['total_vaccinations'].fillna(0)
df['new_cases'] = df['new_cases'].fillna(0)
df['new_deaths'] = df['new_deaths'].fillna(0)

# 4. Basic EDA
print("\n📈 Descriptive Stats:")
print(df.describe())

# Add death rate
df['death_rate'] = df['total_deaths'] / df['total_cases']

# 5. Visualizations
sns.set(style="whitegrid")

# Line chart: Total Cases Over Time
plt.figure(figsize=(10, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()

# Bar chart: Latest Total Deaths by Country
latest = df.sort_values('date').groupby('location').tail(1)
plt.figure(figsize=(8, 5))
sns.barplot(x='location', y='total_deaths', data=latest)
plt.title('Latest Total COVID-19 Deaths by Country')
plt.xlabel('Country')
plt.ylabel('Total Deaths')
plt.tight_layout()
plt.show()

# Histogram: Distribution of New Cases
plt.figure(figsize=(8, 5))
sns.histplot(df['new_cases'], bins=30, kde=True)
plt.title('Distribution of Daily New Cases')
plt.xlabel('New Cases')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Scatter Plot: Total Cases vs. Total Deaths
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='total_cases', y='total_deaths', hue='location')
plt.title('Total Cases vs. Total Deaths')
plt.xlabel('Total Cases')
plt.ylabel('Total Deaths')
plt.tight_layout()
plt.show()

# 6. Vaccination Progress Over Time
plt.figure(figsize=(10, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country)
plt.title('Vaccination Progress Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()

# 7. Summary Insights
print("\n🧠 Key Insights:")
print("- The United States leads in total cases and vaccinations.")
print("- Death rates vary, with some countries maintaining low fatality.")
print("- Vaccination campaigns show steady growth across all regions.")
print("- Sudden spikes in new cases are noticeable in multiple waves.")
