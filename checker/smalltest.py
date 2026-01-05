
from Player import Player
from Team import Team
from Section import Section
import math
import json
from convert import *
import os
#'''
tournaments = ['t1','t2','t3','t4','t5']
for tournament in tournaments:
    for file in os.listdir(f"solutions/{tournament}"):
        if file.endswith(".json"):
            with open(f"solutions/{tournament}/{file}") as f:
                JSON = json.loads(f.read())

            sec1 = build_sections_from_JSON(JSON)
            sec2 = build_sections_from_JSON(JSON)

            print("Checking section: " + file)
            print(sec1[0].checkByesAndWithdrawals(sec1[0].rounds_paired))

'''
# TESTING OF SAMPLE TOURNAMENT --- SUCCESSFULLY PASSED
round = 2
with open("solutions/t1/t1_s1_r2_solution.json") as f:
    JSON = json.loads(f.read())
sec = build_sections_from_SwissSys(JSON)
#print(sec[0].checkDoublePairings(round))
print(sec[0].checkEqualScoresMatched(round))
print(sec[0].checkTopVsBottomHalfTest(round))
#print(sec[0].checkEqualizedColors(round))
#print(sec[0].checkAlternatingColors(round));'''

