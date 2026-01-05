class Team:
    def __init__(self, obj, team_cut):
        self.dict = obj
        self.name = obj['Full name']
        self.pair_number = obj['Pair number']
        self.Team_code = obj['Team code']
        self.players = []
        self.score = 0
        self.team_cut = team_cut

    def addPlayer(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players
    
    def calculateScore(self):
        for player in self.players:
            self.score += player.getScore()
        return self.score
    
    def getScore(self):
        self.calculateScore()
        return self.score
    
    def getDict(self):
        return self.dict