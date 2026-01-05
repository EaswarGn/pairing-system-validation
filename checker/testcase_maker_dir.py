import pandas as pd
import numpy as np
from Player import Player
from Team import Team
import json
import convert
import os

def generateTestCases(file_path, input_file_path, solution_file_path, tournament_section_name):
    sheets = pd.read_excel(file_path, sheet_name=['Settings', 'Players', "Results"], engine='openpyxl')

    ss = sheets['Settings']
    ps = sheets['Players']
    rs = sheets['Results']

    player_count = ps.shape[0]
    player_list = []
    teamname_list = []
    team_list = []
    byes_list = []
    withdrawals_list = []
    withdrawn_players = []

    # Create players
    for i in range(player_count):
        row = ps.iloc[i]
        player_stats = dict() # ['Pair number', 'Name', 'Rating', 'Results'] (Team)
        player_stats['Pair number'] = i + 1
        player_stats['Name'] = row["NAME"]
        player_stats['Rating'] = int(row["RATING"])
        
        # Generate results with results sheet
        player_results = rs.iloc[i]
        num_rounds = int(ss["RDS_PRD"].iloc[0])
        
        results = []
        for j in range(1, num_rounds + 1):
            opp = player_results["OP" + str(j)]
            clr = player_results["CLR" + str(j)]
            res = player_results["RES_CH" + str(j)]

            # Resolve result
            if res == "W": #add "or res == "X" for forfeit
                res = "+"
            elif res == "L": # add "or res == "F" for forfeit
                res = "-"
            elif res == "D":
                res = "="
            # Now just for resolving Byes or Withdrawals
            elif res == "H":
                byes_list.append(dict({"Pair number": i + 1, "Round": j, "Points": 0.5}))
            elif res == "B":
                byes_list.append(dict({"Pair number": i + 1, "Round": j, "Points": 1}))
            elif res == "U":
                if (i + 1) not in withdrawn_players:
                    withdrawals_list.append(dict({"Pair number": i + 1, "Rounds withdrawn": [j]}))
                    withdrawn_players.append(i + 1)
                else:
                    for w in withdrawals_list:
                        if w["Pair number"] == i + 1:
                            w["Rounds withdrawn"].append(j)

            # Resolve color
            if clr > 0:
                clr = "W"
            elif clr < 0:
                clr = "B"
            else:
                clr = "-"
            # Add round to results
            results.append(";".join([str(res), str(opp), clr]))
        
        # add team if player in a team before results just for order of JSON
        if not pd.isna(ps.iloc[i]["TEAM"]):
            player_stats["Team"] = ps.iloc[i]["TEAM"]
            if ps.iloc[i]["TEAM"] not in teamname_list:
                teamname_list.append(ps.iloc[i]["TEAM"])
        # add results
        player_stats['Results'] = results
        

        # Create plater object and append it to list
        player_list.append(Player(player_stats))

    # Create teams
    for i in range(len(teamname_list)):
        obj = dict()
        obj['Pair number'] = i + 1
        obj["Full name"] = teamname_list[i]
        obj["Team code"] = teamname_list[i]
        team_list.append(Team(obj, 4))

    # Initiate wrapper:
    sections_list = dict({"Sections": []})

    # Set settings for tournament
    section = dict()
    section["Section name"] = ""
    section["Type"] = 0
    section["Number of players"] = player_count
    section["Number of teams"] = len(teamname_list)
    section["Rounds paired"] = 0
    section["Rounds played"] = 0
    section["Regular"] = True
    section["Rapid"] = False
    section["Blitz"] = False
    section["Acceleration"] = 0
    section["Use team pairings"] = True
    section["Team cut"] = 4
    section["Players"] = []
    section["Teams"] = [team.getDict() for team in team_list]
    section["Byes"] = byes_list
    section["Withdrawals"] = withdrawals_list

    # Generate files, Add num paired, num played, players
    for i in range(num_rounds):
        sect = section.copy()
        sect["Section name"] = tournament_section_name + str(i + 1)
        
        # make Input files
        sect["Rounds paired"] = i
        sect["Rounds played"] = i
        sect["Players"] = [player.getPlayerDictUpToRound(i) for player in player_list]
        sections_list["Sections"] = [sect]

        with open(input_file_path + tournament_section_name + str(i + 1) + ".json", 'w') as input_file:
            input_file.write(json.dumps(sections_list, indent=4))
        print("Generated input file: " + input_file_path + tournament_section_name + str(i + 1) + ".json")

        # Make Solution files
        sect["Rounds paired"] = i + 1
        sect["Rounds played"] = i
        sect["Players"] = [player.getPlayerPairingsSolution(i + 1) for player in player_list]
        sections_list["Sections"] = [sect]

        with open(solution_file_path + tournament_section_name + str(i + 1) + "_solution.json", 'w') as solution_file:
            solution_file.write(json.dumps(sections_list, indent=4))
        print("Generated solution file: " + solution_file_path + tournament_section_name + str(i + 1) + "_solution.json")


def read_csv_to_dataframe(file_path):
    try:
        # Read the CSV file into a DataFrame, skipping the first line
        df = pd.read_csv(file_path)
        
        # Display the contents of the DataFrame
        print(df)
        return df
    
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except pd.errors.ParserError:
        print("Error parsing the file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None




# Specify the path to your CSV file
tournament = ['t1','t2','t3','t4','t5']
tournament_names = ['2022 Chicago Open', '2022 World Open', '2023PAStateScholastics', '2024 PA State Scholastics', '2023 World Open']

tournament_index = 't1'
dir_to_make_files = '2022 Chicago Open'

csv_file_path = f'solutions/{tournament_index}/resolve.txt'
input_file_path = f'inputs/{tournament_index}/'
solution_file_path = f'solutions/{tournament_index}/'

df = read_csv_to_dataframe(csv_file_path)
for i in range(df.shape[0]):
    index = df.iloc[i]["index"]
    name = df.iloc[i]["section name"]
    num_rounds = int(df.iloc[i]["num_tests"])

    file_path = f'../tournament-files/{dir_to_make_files}/{name}.S{num_rounds}C.xlsx'
    tournament_section_name = f'{tournament_index}_s{index}_r'
    generateTestCases(file_path, input_file_path, solution_file_path, tournament_section_name)
    print(f"Generated test cases for {name} with {num_rounds} rounds.")

print("Done generating test cases.")