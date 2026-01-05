from Player import Player
from Team import Team
from Section import Section
import math
import json
from convert import *
import os

with open('sample_tournament-Rd1A.json') as f:
     JSON1 = json.loads(f.read())

sec1 = build_sections_from_SwissSys(JSON1)
sec2 = build_sections_from_SwissSys(JSON1)

# RUN SOME TESTS
def test_checkLastRound():
     # Test case 1:
     # Expected output: True
     # print(sec1[0].checkLastRound(sec2[0]))
     print("Now passing individiual tests.")
     round_num = sec2[0].rounds_paired
     print("Rule 1", sec2[0].checkAlternatingColors(round_num))
     print("Rule 2",sec2[0].checkEqualizedColors(round_num))
     print("Rule 3",sec2[0].checkTopVsBottomHalf(round_num))
     print("Rule 4",sec2[0].checkEqualScoresMatched(round_num))
     print("Rule 5",sec2[0].checkDoublePairings(round_num))
     print("Teamate",sec2[0].checkMatchedAgainstTeammate(round_num))
     print("Byes",sec2[0].checkByesAndWithdrawals(round_num))
     print("Erroneous",sec2[0].checkErroneousPairings(round_num))
     print(len(sec2[0].score_groups[0]))


test_checkLastRound()


'''
from app import resolve_index, resolve_testcase

for x in range(1, 415):
    tc = resolve_index(x)
    tc_name = tc.split(".")[0]
    sf = resolve_testcase(tc_name)
    print(x, tc, tc_name, sf)
'''
