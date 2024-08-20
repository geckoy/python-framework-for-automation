
class assetsserverArgs:

    def setProperties(self):
        self._counter = 0
        self._players = []
        self.counter = 0 
        self.players = ["assetsserver1", "assetsserver2"]


    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, a):
        self.set_process_ginfo("counter", a)
        self._counter = a
    
    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, a):
        self.set_process_ginfo("players", a)
        self._players = a