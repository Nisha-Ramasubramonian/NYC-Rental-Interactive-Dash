import pandas as pd
import numpy as np
from datetime import datetime
import numpy_financial as npf

# Generate date range
start_date = np.datetime64('2018-01-01')
end_date = np.datetime64('2022-12-31')
date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
dates = pd.DatetimeIndex(np.random.choice(date_range, size=10000, replace=True))

# Generate location column
locations = np.random.choice(['long_island', 'NYC'], size=10000)

# Import zip code data
zip_data = pd.read_excel('/Users/barbaratalagan/Desktop/zip_town_county.xlsx')

# Filter zip code data for long_island locations
long_island_zip = zip_data[zip_data['location'] == 'long_island']['zip_code']

# Generate zip code column
zip_codes = np.random.choice(long_island_zip, size=10000)

# Generate story and dummy variable columns
stories = np.random.choice([0, 1], size=10000)
dummy_variables = np.random.choice([0, 1], size=10000)

# Generate bed, bath, and sq_foot columns
bed = np.where((locations == 'long_island') & (stories == 0), 2, 3)
bath = np.ones(10000, dtype=int)
sq_foot = np.where((locations == 'long_island') & (stories == 0), 1100, 1300)

# Generate price_per_sq_foot column
price_per_sq_foot = np.zeros(10000)

for year in range(2018, 2023):
    # Calculate price_per_sq_foot for location == "long_island" and story == 0
    price_per_sq_foot[(locations == 'long_island') & (stories == 0) & (dates.year == year)] = np.random.uniform(350, 500)

    # Calculate price_per_sq_foot for location == "NYC" and story == 0
    price_per_sq_foot[(locations == 'NYC') & (stories == 0) & (dates.year == year)] = np.random.uniform(250, 350)

    # Calculate price_per_sq_foot for location == "long_island" and story == 1
    price_per_sq_foot[(locations == 'long_island') & (stories == 1) & (dates.year == year)] = np.random.uniform(250, 350)

    # Calculate price_per_sq_foot for location == "NYC" and story == 1
    price_per_sq_foot[(locations == 'NYC') & (stories == 1) & (dates.year == year)] = np.random.uniform(350, 500)

# Generate total_cost column
total_cost = sq_foot * price_per_sq_foot

# Generate interest_rate column
start_date_np = np.datetime64(start_date)
years = (dates - start_date_np) / np.timedelta64(1, 'D') / 365
interest_rate = np.interp(years, [0, 4.9], [0.03, 0.06])

# Generate down_pmt_percent column
down_pmt_percent = np.random.uniform(0.03, 0.2, size=10000)

# Generate down_pmt_amount column
down_pmt_amount = total_cost * down_pmt_percent

# Generate loan_amount column
loan_amount = total_cost - down_pmt_amount

# Generate loan_term column
loan_term = np.where(np.random.rand(10000) < 0.6, 30, np.where(np.random.rand(10000) < 0.9, 15, 10))

# Generate monthly_payment column
monthly_payment = np.where(locations == 'NYC', total_cost / 100, npf.pmt(interest_rate/12, loan_term * 12, -loan_amount))

# Create the dataframe
data = {
    'date': dates,
    'location': locations,
    'zip_code': zip_codes,
    'story': stories,
    'dummy_variable': dummy_variables,
    'bed': bed,
    'bath': bath,
    'sq_foot': sq_foot,
    'price_per_sq_foot': price_per_sq_foot,
    'total_cost': total_cost,
    'interest_rate': interest_rate,
    'down_pmt_percent': down_pmt_percent,
    'down_pmt_amount': down_pmt_amount,
    'loan_amount': loan_amount,
    'loan_term': loan_term,
    'monthly_payment': monthly_payment
}

df = pd.DataFrame(data)

# Replace values with NaN for location == "NYC"
df.loc[df['location'] == 'NYC', ['down_pmt_percent', 'down_pmt_amount', 'loan_amount', 'loan_term']] = np.nan

# Export DataFrame to Excel
df.to_excel('/Users/nisharamasubramonian/Desktop/output_data.xlsx', index=False)

# Display the dataframe
print(df)
