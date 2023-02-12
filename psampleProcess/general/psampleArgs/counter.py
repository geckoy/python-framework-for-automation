
class counter:

    def setProperties(self):
        self._tester_counter = 0
        self._players = []
        self.tester_counter = 0 
        self.players = ["Player1", "Player2"]


    @property
    def tester_counter(self):
        return self._tester_counter

    @tester_counter.setter
    def tester_counter(self, a):
        self.set_process_ginfo("tester_counter", a)
        self._tester_counter = a
    
    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, a):
        self.set_process_ginfo("players", a)
        self._players = a