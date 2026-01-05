import os
import json

def rename_files_in_directory(directory_path):
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename == "rename.py" or filename == "sample_tournament-Rd0A.json":
            continue

        # Read the JSON object from the file
        with open(filename, 'r') as file:
            data = json.load(file)
        
        #Modify last player round
        for section in data['Sections']:
            for player in section['Players']:
                new_res = list(player['Results'][-1])
                if new_res[0] in ["+", "-", "="]:
                    new_res[0] = '~'
                rew_res = "".join(new_res)
                player['Results'][-1] = rew_res

        output_file = list(filename)
        output_file[21] = 'A'
        output_file = "".join(output_file)
        
        # Save the modified JSON object to the new file
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f'Modified JSON saved to: {output_file}')


# Usage
directory_path = "./"  # Replace with your directory path
rename_files_in_directory(directory_path)
