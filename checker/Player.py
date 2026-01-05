class Player:
    def __init__(self, obj):
        self.dict = obj
        self.name = obj['Name']
        self.pair_number = obj['Pair number']
        self.rating = obj['Rating']
        self.results = [result.split(';')[0:3] for result in obj['Results']]

    def getPairNumber(self):
        return self.pair_number
    
    def getOpponents(self, round_num):
        return [int(result[1]) for result in self.results[:round_num]]
    
    def getResults(self, round_num):
        return self.results[:round_num]
    
    def getRating(self):
        if self.rating == "unr.":
            return 0
        return self.rating
    
    def getPoint(self, char):
        if char == "+":
            return 1
        elif char == "-":
            return 0
        elif char == "=":
            return 0.5
        elif char == "~":
            return 0
        elif char == "B":
            return 1
        elif char == "H":
            return 0.5
        elif char == "X":
            return 1
        elif char == "F":
            return 0
        else:
            return 0
        
    def getScore(self, round_num):
        #print(sum([(self.getPoints(result[0])) for result in self.results[0:round_num]]))
        s1 = [result[0] for result in self.results[:round_num]]
        for x in range(len(s1)):
            s1[x] = self.getPoint(s1[x])
        return sum(s1)
    
    def getTeam(self):
        if "Team" in self.dict.keys():
            return self.dict['Team']
        else:
            return None

    def getDict(self):
        return self.dict
    
    def getColors(self, round_num):
        return [result[2] if result[0] not in ['F', 'X'] else '-' for result in self.results[:round_num]]
    
    # For test file creation
    def getPlayerDictUpToRound(self, round_num):
        modified_dict = self.dict.copy()
        modified_dict['Results'] = modified_dict['Results'][:round_num]
        return modified_dict
    
    def getPlayerPairingsSolution(self, round_num):
        modified_dict = self.dict.copy()
        modified_dict['Results'] = modified_dict["Results"][:round_num]
        if modified_dict["Results"][round_num - 1][0] not in ['B', 'H', "U"]:
            modified_dict["Results"][round_num - 1] = str("~" + modified_dict["Results"][round_num - 1][1:])
        return modified_dict


############################ TESTING PURPOSES ############################
JSON = {"Pair number": 1,
          "Name": "Carlsen, Magnus",
          "ID": "15218438",
          "Rating": 2914,
          "Rating2": 2875,
          "Exp1": "7/31/2013",
          "Current result": " ",
          "Note": "Result coding is Result; Op.; Clr; Brd; Logical ops. 1 & 2; Game pnts",
          "Results": [
            "-;5;B;1;5;5;0",
            "+;2;W;3;2;2;0",
            "+;8;W;2;8;8;0"
          ]} 

p1 = Player(JSON)
# print(p1.getPlayerPairingsSolution(1))
