
class counterparallel:

    def setProperties(self):
        self._mycounter = 0
        self._players = []
        self.mycounter = 0 
        self.players = ["Player1", "Player2"]


    @property
    def mycounter(self):
        return self._mycounter

    @mycounter.setter
    def mycounter(self, a):
        self.set_process_ginfo("mycounter", a)
        self._mycounter = a
    
    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, a):
        self.set_process_ginfo("players", a)
        self._players = a