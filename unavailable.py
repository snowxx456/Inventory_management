import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'local_data.csv'
df = pd.read_csv(file_path)

# Create a DataFrame with all possible Bin NO values
all_bins = pd.DataFrame({'Bin NO': range(1, 31)})

# Merge to identify missing Bin NO values
missing_bins = all_bins.merge(df[['Bin NO']], on='Bin NO', how='left', indicator=True)

# Filter rows that are only in 'all_bins' (missing)
missing_data = missing_bins[missing_bins['_merge'] == 'left_only'].drop(columns=['_merge'])

# Fill in missing data
missing_data['Location Rack'] = ''
missing_data['Part No'] = ''
missing_data['Name'] = ''
missing_data['Date_Time'] = ''
missing_data['Availability'] = 'unavailable'
missing_data['Checked_by'] = ''

# Append missing data to the original DataFrame
df = pd.concat([df, missing_data]).sort_values('Bin NO').reset_index(drop=True)

# Overwrite the CSV file with the updated DataFrame
df.to_csv(file_path, index=False)
