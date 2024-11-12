class Match:
    def __init__(self,team1,team2,time,odd1,odd2,oddX):
        self.team1=team1
        self.team2=team2
        self.time=time
        self.odd1=odd1
        self.odd2=odd2
        self.oddX=oddX
    def __str__(self):
        return f'{self.team1} {self.time} {self.team2}\n{self.odd1} {self.oddX} {self.odd2}\n'