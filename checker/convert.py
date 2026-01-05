from Player import Player
from Team import Team
from Section import Section
import math
import json

def validateJSONFormat(JSON):
    required_keys = ['Section name', 'Type', 'Number of players', 'Number of teams', 'Rounds paired', 'Rounds played', 'Team cut', 'Regular', 'Rapid', 'Blitz', 'Acceleration', 'Use team pairings', 'Players', 'Teams']
    required_keys_players = ['Pair number', 'Name', 'Rating', 'Results']
    required_keys_teams = ['Pair number', 'Full name', 'Team code']
    required_keys_byes = ['Pair number', 'Round', 'Points']
    required_keys_withdraws = ['Pair number', 'Rounds withdrawn']
    missing_keys = []

    # Check if all necessary info is present in JSON
    for section in JSON['Sections']:
        # Check if all necessary info is present in each section
        for key in required_keys:
            if key not in section.keys():
                missing_keys.append("missing section key: " + key)
        for player in section['Players']:
            for key in required_keys_players:
                if key not in player:
                    missing_keys.append("missing player key: " + key)
        for team in section['Teams']:
            for key in required_keys_teams:
                if key not in team:
                    missing_keys.append("missing team key: " + key)
        for bye in section['Byes']:
            for key in required_keys_byes:
                if key not in bye:
                    missing_keys.append("missing bye key: " + key)
        for withdraw in section['Withdrawals']:
            for key in required_keys_withdraws:
                if key not in withdraw:
                    missing_keys.append("missing withdraw key: " + key)
    # Print errors
    if len(missing_keys) > 0:
        print("Invalid JSON file:")
        for key in missing_keys:
            print("File missing key: " + str(key))
        return False
    return True

def validateCSVFormat(file):
    return False

def validateTRFFormat(file):
    return False

def build_sections_from_SwissSys(JSON):
    sections = []
    for section in JSON['Sections']:
        if section['Blitz'] == True:
            section['Regular'] = False
            section['Rapid'] = False
        else:
            section['Regular'] = True
            section['Rapid'] = False
        for player in section['Players']:
            if 'Rating' not in player.keys():
                player['Rating'] = 100
        section['Byes'] = []
        section['Withdrawals'] = []
        sections.append(Section(section))
    return sections

def build_sections_from_JSON(file):
    sections = []
    for section in file['Sections']:
        sections.append(Section(section))
    return sections

def build_sections_from_CSV(file):
    pass

def build_sections_from_TRF(file):
    pass
