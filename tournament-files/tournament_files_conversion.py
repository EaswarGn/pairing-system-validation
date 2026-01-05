import os
import pandas as pd
import re
from extracting_sheets import extract_sheets
 
# Define the folder path
folder_path = 'tournament-files/2022 Chicago Open'
print(os.getcwd())
 
# List all files in the folder
files = os.listdir(folder_path)
 
# Define a pattern to match the filenames based on the provided structure
pattern = re.compile(r'.*\.(S\d+[A-Z])$')
 
# Function to convert old Excel files to .xlsx
def convert_to_xlsx(file_path, output_path):
    try:
        # Read the old Excel file
        df = pd.read_excel(file_path, engine='xlrd')
        # Save it as a new .xlsx file
        df.to_excel(output_path, index=False, engine='openpyxl')
        return f"Converted {file_path} to {output_path}"
    except Exception as e:
        return f"Failed to convert {file_path}: {e}"
 
# Loop through all files in the folder
conversion_results = []
for file in files:
    file_path = os.path.join(folder_path, file)
    if pattern.match(file):
        output_path = file_path + '.xlsx'
        result = convert_to_xlsx(file_path, output_path)
        conversion_results.append(result)
    else:
        conversion_results.append(f"Skipping non-Excel file: {file_path}")
 
# Print conversion results
for result in conversion_results:
    print(result)