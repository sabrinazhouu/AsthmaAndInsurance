import pandas as pd

# Assuming 'asthma_df' is your pandas DataFrame
asthma_df = pd.read_csv('population_data_1.csv')


asthma_df = asthma_df.drop(asthma_df.index[0])

new_columns = asthma_df.iloc[0]  # Get the top row
asthma_df = asthma_df[1:]  # Remove the top row from the DataFrame
asthma_df.set_axis(new_columns, axis=1, inplace=True)

print(asthma_df)
state_name_to_code = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
asthma_df['State Code'] = asthma_df['States'].map(state_name_to_code)

asthma_df = asthma_df.replace(',', '', regex=True)

asthma_df['Population'] = asthma_df['Population'].astype(int)
asthma_df['Adult Number'] = asthma_df['Adult Number'].astype(int)
asthma_df['Child Number'] = asthma_df['Child Number'].astype(int)

asthma_df.to_csv('clean_population_data.csv')