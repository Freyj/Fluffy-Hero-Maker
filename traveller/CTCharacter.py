from traveller.gen_ct import roll_stats, enlist
from utils.dice_roller import roll_die


class CTCharacter:
    def __init__(self):
        self.stats = roll_stats()
        self.skills = {}
        self.service = ""
        self.commission = False
        self.rank = 0
        self.age = 18
        self.history = []
        self.survived = True
        self.pension = 0
        self.terms = 0
        self.drafted = False

    def choose_service(self, service_name: str):
        """

            :param service_name:
            :return:
        """
        enlisted = enlist(self.stats, service_name)
        if enlisted:
            self.history.append("Enlisted in the {ser}.".format(ser=service_name))
            self.service = service_name
        else:
            self.history.append("Submitted to the Draft.")
            self.get_drafted()
            self.drafted = True
        self.career()

    def get_drafted(self):
        a = roll_die(6) - 1
        if a == 0:
            self.service = "Marines"
        elif a == 1:
            self.service = "Navy"
        elif a == 2:
            self.service = "Army"
        elif a == 3:
            self.service = "Merchants"
        elif a == 4:
            self.service = "Scouts"
        elif a == 5:
            self.service = "Others"
