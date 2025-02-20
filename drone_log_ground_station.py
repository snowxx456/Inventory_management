import requests
import base64
import time
import os
import pandas as pd

# Replace with your repository details
owner = 'snowxx456'
repo = 'Inventory_management'
file_path = 'data.csv'

# Replace with your actual access token
token = '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' 

# Set up authentication headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to get file contents from GitHub
def get_file_contents(repo_url):
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return content
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Function to save data to a local file
def save_to_local_file(data):
    with open('local_data.csv', 'w') as file:
        file.write(data)

# Construct the URL for file operations
file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
def natural_sort_key(s):
    parts = s.split()
    if len(parts) == 2 and parts[0] == 'Bin':
        return (int(parts[1]),)  # Convert the number part to integer for sorting
    else:
        return (0,)  # Handle other cases by placing them at the end

while True:
    # Get current file content
    file_info = get_file_contents(file_url)

    if file_info:
        existing_content = base64.b64decode(file_info['content']).decode()
        
        # Save data to local file
        save_to_local_file(existing_content)
        print("Data saved to local_data.csv")

        # Read the CSV file into a DataFrame
        data_for_sort = pd.read_csv('local_data.csv')

        # Convert the 'Bin NO' column to numeric type
        data_for_sort['Bin NO'] = data_for_sort['Bin NO'].str.extract('(\d+)').astype(int)

        # Sort the data based on the 'Bin NO' column as integers
        sorted_data = data_for_sort.sort_values(by='Bin NO')

        # Save the sorted data back to a CSV file
        sorted_data.to_csv('local_data.csv', index=False)

    else:
        print("Failed to retrieve file contents.")
    
    # Change this value as needed
