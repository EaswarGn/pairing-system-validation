import pandas as pd
import numpy as np
from Player import Player
from Team import Team
import json
import convert

file_path = 'tournament-files/2022 World Open/.SC.xlsx'
input_file_path = 'checker/inputs/t2/'
solution_file_path = 'checker/solutions/t2/'
tournament_section_name = 't3_s1_r'

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
        if res == "W" or res == "X": #add "or res == "X" for forfeit
            res = "+"
        elif res == "L" or res == "F": # add "or res == "F" for forfeit
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
                withdrawals_list.append(dict({"Pair number": i + 1, "Round": j}))
                withdrawn_players.append(i + 1)

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
