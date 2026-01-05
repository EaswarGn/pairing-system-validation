from Player import Player
from Team import Team
import math
import json


class Section():
    def __init__(self, obj):
        self.dict = obj
        self.name = obj['Section name']
        self.type = obj['Type']
        self.num_players = obj['Number of players']
        self.num_teams = obj['Number of teams']
        self.rounds_paired = obj['Rounds paired']
        self.rounds_played = obj['Rounds played']
        self.regular = obj['Regular']
        self.rapid = obj['Rapid']
        self.blitz = obj['Blitz']
        self.acceleration = obj['Acceleration']
        self.use_team_pairings = obj['Use team pairings']

        self.players = [Player(player) for player in obj['Players']]
        self.playerDict = {player.getPairNumber(): player for player in self.players}

        self.teams = [Team(team, obj["Team cut"]) for team in obj['Teams']]
        self.teamDict = {team.getDict()['Team code']: team for team in self.teams}

        self.byes = obj['Byes']
        self.withdrawals = obj['Withdrawals']

        # Generate teams
        for player in self.players:
            if "Team" in player.getDict().keys():
                self.teamDict[player.getDict()["Team"]].addPlayer(player)

        self.score_groups = dict()
    
    def getSectionName(self):
        return self.name
    

    # Helper Methods for checking functions
    def make_score_groups(self, round_num):
        for player in self.players:
            if player.getScore(round_num) in self.score_groups:
                self.score_groups[player.getScore(round_num)].append(player)
            else:
                self.score_groups[player.getScore(round_num)] = [player]

    # Round Validation Methods
    # TODO: Implement Exceptions for rules
    def checkLastRound(self, solution) -> list:
        round_num = self.rounds_paired
        # print(self.rounds_paired)

        if not self.checkByesAndWithdrawals(round_num):
            return [False, "Pairings did not properly implement given Byes/Withdrawals"]
        if not self.checkErroneousPairings(round_num):
            return [False, "Pairings have one or more player playing more than one opponent in last round"]

        x = self.checkDoublePairings(round_num)
        y = solution.checkDoublePairings(round_num)
        if len(x) > len(y):
            return [False, 'Double Pairings']
        elif len(x) < len(y):
            return [True, 'Solution outpaired correct number of double pairings']
        else:
            # 1 - Double 
            x = self.checkEqualScoresMatched(round_num)
            y = solution.checkEqualScoresMatched(round_num)
            if len(x) > len(y):
                return [False, 'Equal Scores Matched']
            elif len(x) < len(y):
                return [True, 'Solution outpaired correct number of equal scores matched']
            else:
                # Rule 2 passed, check rule 3
                x = self.checkTopVsBottomHalf(round_num)
                y = solution.checkTopVsBottomHalf(round_num)
                if len(x) > len(y):
                    return [False, 'Top vs Bottom Half']
                elif len(x) < len(y):
                    return [True, 'Solution outpaired correct number of top vs bottom half']
                else:
                    # Rule 3 passed, check rule 4
                    x = self.checkMatchedAgainstTeammate(round_num)
                    y = solution.checkMatchedAgainstTeammate(round_num)
                    if len(x) > len(y):
                        return [False, 'Equalized Colors']
                    elif len(x) < len(y):
                        return [True, 'Solution outpaired correct number of teammates matched']
                    else:
                        # Rule 4 passed, check rule 5
                        x = self.checkThreeColors(round_num)
                        y = solution.checkThreeColors(round_num)
                        if len(x) > len(y):
                            return [False, 'Three Colors']
                        elif len(x) < len(y):
                            return [True, 'Solution outpaired correct number of three colors']
                        else:
                            # Rule 5 passed, check rule 6
                            x = self.checkEqualizedColors(round_num)
                            y = solution.checkEqualizedColors(round_num)
                            if len(x) > len(y):
                                return [False, 'Equalized Colors']
                            elif len(x) < len(y):
                                return [True, 'Solution outpaired correct number of equalized colors']
                            else:
                                # Rule 6 passed, check rule 7
                                x = self.checkAlternatingColors(round_num)
                                y = solution.checkAlternatingColors(round_num)
                                if len(x) > len(y):
                                    return [False, 'Alternating Colors']
                                elif len(x) < len(y):
                                    return [True, 'Solution outpaired correct number of alternating colors']
                                else:
                                    # Rule 6 passed
                                    return [True, 'All Rules Passed']
                                

    def checkByesAndWithdrawals(self, round_num):
        bye_violations = []
        for bye in self.byes:
            if bye['Round'] <= round_num:  
                res = self.playerDict[bye['Pair number']].getResults(round_num)[bye["Round"] - 1]
                if bye['Points'] == 1 and not (res[0] == 'B' and (res[1] in ['-1', '0']) and res[2] == '-'):
                    bye_violations.append(bye, res)
                    # return False
                elif bye['Points'] == 0.5 and not (res[0] == 'H' and (res[1] in ['-1', '0']) and res[2] == '-'):
                    bye_violations.append(bye, res)
                    # return False
        
        withdrawal_violations = []
        for withdrawal in self.withdrawals:
            for round in withdrawal['Rounds withdrawn']:
                if round <= round_num:
                    res = self.playerDict[withdrawal['Pair number']].getResults(round_num)[round - 1]
                    if not (";".join(res) in ["U;0;-", "U;-1;-"] or res[0] == 'F'):
                        withdrawal_violations.append([withdrawal, res])
                        # return False
        
        if len(bye_violations) > 0 or len(withdrawal_violations) > 0:
            print("Byes Violations", bye_violations)
            print("Withdrawal Violations", withdrawal_violations)
            return False
        
        return True
    
    def checkErroneousPairings(self, round_num):
        players = []
        exempt_players = []
        for player in self.players:
            if player.getOpponents(round_num)[-1] < 1:
                exempt_players.append(player.getPairNumber())
            else:
                players.append(player.getOpponents(round_num)[-1])
        if len(set(players)) + len(exempt_players) != len(self.players):
            return False
        return True


    def checkDoublePairings(self, round_num):
        players_violated = []
        for player in self.players:
            if player.getOpponents(round_num).count(player.getOpponents(round_num)[-1]) > 1 and player.getOpponents(round_num)[-1] > 0:
                players_violated.append(player.getPairNumber())
        return players_violated
    

    def checkEqualScoresMatched(self, round_num):
        players_violated = []
        for player in self.players:
            if player.getOpponents(round_num)[-1] > 0: # in case of a bye
                if player.getScore(round_num - 1) != self.playerDict[player.getOpponents(round_num)[-1]].getScore(round_num - 1):
                    players_violated.append(player.getPairNumber())
                    print(player.getPairNumber(), self.playerDict[player.getOpponents(round_num)[-1]].getPairNumber(), player.getScore(round_num - 1), self.playerDict[player.getOpponents(round_num)[-1]].getScore(round_num - 1))
        return players_violated

    def checkTopVsBottomHalf(self, round_num):
        players_violated = []
        self.make_score_groups(round_num - 1)
        # Make Top and Bottom Half based on who is playing within the score group
        getPairNumber = lambda player: player.getPairNumber()
        for score in self.score_groups.keys():
            players_in_group = []
            for player in self.score_groups[score]:
                if player.getOpponents(round_num)[-1] > 0:
                    if player.getScore(round_num - 1) == self.playerDict[player.getOpponents(round_num)[-1]].getScore(round_num - 1):
                        players_in_group.append(player)
            players_in_group.sort(key=getPairNumber)
            top_half = players_in_group[0:len(players_in_group) // 2]
            bottom_half = players_in_group[len(players_in_group) // 2:]
            
            # Check who in a group is playing someone in their own group
            for player in players_in_group:
                if (player in top_half and self.playerDict[player.getOpponents(round_num)[-1]] not in bottom_half) \
                    or (player in bottom_half and self.playerDict[player.getOpponents(round_num)[-1]] not in top_half):
                    players_violated.append(player.getPairNumber())

        return players_violated
    

    def checkTopVsBottomHalfTest(self, round_num):
        players_violated = []
        self.score_groups = dict()
        self.make_score_groups(round_num - 1)
        # Make Top and Bottom Half based on who is playing within the score group
        getPairNumber = lambda player: player.getPairNumber()
        for score in self.score_groups.keys():
            print('###########', score, '################\nScore Group:')
            for x in (player.getPairNumber() for player in self.score_groups[score]):
                print(x, end = " ")
            print("\n")
            players_in_group = []
            for player in self.score_groups[score]:
                if player.getOpponents(round_num)[-1] > 0:
                    if player.getScore(round_num - 1) == self.playerDict[player.getOpponents(round_num)[-1]].getScore(round_num - 1):
                        players_in_group.append(player)
                    else:
                        print(player.getPairNumber(), self.playerDict[player.getOpponents(round_num)[-1]].getPairNumber(), player.getScore(round_num - 1), self.playerDict[player.getOpponents(round_num)[-1]].getScore(round_num - 1))
            players_in_group.sort(key=getPairNumber)
            top_half = players_in_group[0:len(players_in_group) // 2]
            bottom_half = players_in_group[len(players_in_group) // 2:]

            #Testing purposes
            print("Top")
            for item in list(player.getPairNumber() for player in top_half):
                print(item, end = " ")
            print("\nBottom")
            for item in list(player.getPairNumber() for player in bottom_half):
                print(item, end = " ")
            print("\n")
            
            # Check who in a group is playing someone in their own group
            for player in players_in_group:
                if (player in top_half and self.playerDict[player.getOpponents(round_num)[-1]] not in bottom_half) \
                    or (player in bottom_half and self.playerDict[player.getOpponents(round_num)[-1]] not in top_half):
                    players_violated.append(player.getPairNumber())
                    print(player.getPairNumber(), self.playerDict[player.getOpponents(round_num)[-1]].getPairNumber())

        return players_violated
                
    def checkEqualizedColors(self, round_num):
        players_violated = []
        for player in self.players:
            if player.getColors(round_num)[-1] in ['W', 'B']:
                if abs(player.getColors(round_num).count('W') - player.getColors(round_num).count('B')) > 1:
                    players_violated.append(player.getPairNumber())
        return players_violated

    
    def checkThreeColors(self, round_num):
        players_violated = []
        for player in self.players:
            white = 0
            black = 0
            for color in player.getColors(round_num):
                if color == 'W':
                    white += 1
                    black = 0
                elif color == 'B':
                    black += 1
                    white = 0
                if white == 3 or black == 3:
                    players_violated.append(player.getPairNumber())
                    break
        return players_violated

    def checkAlternatingColors(self, round_num):
        players_violated = []
        for player in self.players:
            colors = [i for i in player.getColors(round_num) if i == 'W' or i == 'B']
            if len(colors) > 1:
                if colors[-1] == colors[-2]:
                    players_violated.append(player.getPairNumber()) 
            '''
                for i in range(1, len(colors)):
                    if colors[i] == colors[i - 1]:
                        players_violated.append(player.getPairNumber())
                        break
                        
            This is for overall alternating color chechking. Comment the above if statement
            and replace it with this for loop and if statement if changing to it. But since
            currently only checking the last round breaking rules, I left it as checking
            alteration of colors just for the last two valid color rounds
            '''
        return players_violated
    
    def checkMatchedAgainstTeammate(self, round_num):
        players_violated = []
        for player in self.players:
            if player.getOpponents(round_num)[-1] > 0:
                if "Team" in player.getDict().keys() and "Team" in self.playerDict[player.getOpponents(round_num)[round_num - 1]].getDict().keys():
                    if self.playerDict[player.getOpponents(round_num)[round_num - 1]].getDict()["Team"] == player.getDict()["Team"]:
                        players_violated.append(player.getPairNumber())
        return players_violated
    
    def getPlayers(self):
        return self.players

    def getTeams(self):
        return self.teams
    
    # To String of the object essentially
    def getDict(self):
        return self.dict

