from traveller.gen_ct import roll_stats, enlist


class CTCharacter:
    def __init__(self):
        self.stats = roll_stats()
        self.skills = {}
        self.service = ""
        self.commission = False
        self.rank = 0
        self.age = 18
        self.history = []

    def choose_service(self, service_name: str):
        enlisted = enlist(self.stats, service_name)
        if enlisted:
            self.history.append("Enlisted in the {ser}.".format(ser=service_name))
            self.service = service_name
        else:
            self.get_drafted()

    def get_drafted(self):
        pass
