from source.handlers.file_handler import write_file, load_file


class WeaponFactory:
    def __init__(self, filename):
        self.filename = filename
        self.weapons = {}
        self.load_weapons()

    def get_weapon(self, name):
        if name in self.weapons.keys():
            return self.weapons[name]

    def get_all_weapons(self):
        return self.weapons

    def save_weapons__(self):# unused
        write_file(self.filename, self.weapons)

    def load_weapons(self):
        self.weapons = load_file(self.filename, "config")["weapons"]


weapon_factory = WeaponFactory("buildings.json")
