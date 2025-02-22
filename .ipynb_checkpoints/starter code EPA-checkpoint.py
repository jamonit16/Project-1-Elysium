
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('EPA_API_KEY')



def fetch_aqi_data(year, api_key):
    url = 'https://aqs.epa.gov/data/api/annualData/byCBSA'
    params = {
        'email': 'massmediafan@gmail.com',
        'key': api_key,
        'param': '88101',  # Column for PM2.5
        'bdate': f'{year}0101',
        'edate': f'{year}1231',
        'cbsa': '35620'  # CBSA code for Tulsa, LA or NY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data['Data'])

# Range of years
years = range(2014, 2023)  # Adjust this range as needed

# Concatenate data for each year
all_data = pd.DataFrame()
for year in years:
    yearly_data = fetch_aqi_data(year, api_key)
    all_data = pd.concat([all_data, yearly_data])

# Reset the index
all_data.reset_index(drop=True, inplace=True)

# Convert first max datetime for dates
all_data['first_max_datetime'] = pd.to_datetime(all_data['first_max_datetime'])

# Set date column as the index
all_data.set_index('first_max_datetime', inplace=True)

# View DataFrame
print(all_data.head())
print(all_data.tail())