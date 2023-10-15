class Debugger:
    __slots__ = ("ships", "planets", "ufos", "collectable_items")#, "planet", "celestials", "items")
    def __init__(self):
        self.ships = False
        self.planets = False
        self.ufos = False
        self.collectable_items = False
        # self.planet = False
        # self.celestials = False
        # self.items = False



debugger = Debugger()

