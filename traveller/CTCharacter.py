# The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 - 2008 Far Future Enterprises.
# (CF : http://www.farfuture.net/FFEFairUsePolicy2008.pdf)
import json

from sty import fg

from traveller.funcs_ct import roll_stats, enlist, survive, try_commission, max_service_rank, try_promotion, \
    get_noble_rank, age_stats, service_reenlistment, roll_skill, display_navy_skill_tables, \
    display_marines_skill_tables, display_scouts_skill_tables, display_merchants_skill_tables, \
    display_army_skill_tables, display_others_skill_tables, treat_benefits
from utils.dice_roller import roll_die
from traveller.consts_trav import *


class CTCharacter:
    """
        Class for Classic Traveller characters
    """
    def __init__(self):
        self.name = ""
        self.stats = roll_stats()
        self.skills = {}
        self.service = ""
        self.rank = 0
        self.age = 18
        self.history = []
        self.survived = True
        self.pension = 0
        self.terms = 0
        self.drafted = False
        self.skill_rolls = 0
        self.inventory = []
        self.cash = 0
        self.reenlisting = 0
        self.benefits = []

    def choose_service(self, service_name: str):
        """
            Selects the service, if enlistment fails, draft
            :param service_name:
        """
        self.history.append("Applied to enter the {ser}".format(ser=service_name))
        enlisted = enlist(self.stats, service_name)
        if enlisted:
            self.history.append("Enlisted in the {ser}.".format(ser=service_name))
            self.service = service_name
        else:
            self.history.append("Failed to enlist in the {ser}".format(ser=service_name))
            self.history.append("Submitted to the Draft.")
            self.get_drafted()
            self.drafted = True
        self.get_service_skills()

    def display_tables(self):
        """
            Displays the proper skill table for skill choices
        """
        if self.service == "Navy":
            display_navy_skill_tables(self.stats["Edu"])
        elif self.service == "Marines":
            display_marines_skill_tables(self.stats["Edu"])
        elif self.service == "Scouts":
            display_scouts_skill_tables(self.stats["Edu"])
        elif self.service == "Merchants":
            display_merchants_skill_tables(self.stats["Edu"])
        elif self.service == "Army":
            display_army_skill_tables(self.stats["Edu"])
        elif self.service == "Others":
            display_others_skill_tables(self.stats["Edu"])

    def get_drafted(self):
        """
            Rolls for the draft
        """
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
        self.history.append("Drafted in the {ser}.".format(ser=self.service))

    def can_commission(self):
        """
            Checks if the character can get a commission
            :return: a boolean
        """
        if self.drafted and self.age == 18:
            return False
        elif self.service not in ["Navy", "Marines", "Army", "Merchants"]:
            return False
        elif self.rank > 0:
            return False
        else:
            return True

    def get_service_skills(self):
        """
            Gives character the skills granted by service
        """
        if self.service == "Marines":
            self.add_skill("Blade Combat(Cutlass)")
        elif self.service == "Army":
            self.add_skill("Gun Combat(Rifle)")
        elif self.service == "Scouts":
            self.add_skill("Pilot")

    def get_promotion_skills(self):
        """
            Gives characters skills granted by promotion
        """
        if self.service == "Navy" and self.rank in [5, 6]:
            self.stats["Soc"] += 1
            self.history.append("Improved Soc by 1 from promotion.")
        elif self.service == "Merchants" and self.rank == 3:
            self.add_skill("Pilot")

    def get_commission_skills(self):
        """
            Gives characters skills granted by commission
        """
        if self.service == "Marines":
            self.add_skill("Gun Combat(Revolver)")
        elif self.service == "Army":
            self.add_skill("Gun Combat(SMG)")

    def term(self, automatic=False):
        """
            Goes through a term for the characters, if automatic then goes randomly
        """
        survived = survive(self.stats, self.service)
        if survived:
            self.history.append("Survived the term.")
            self.skill_rolls = 0
            if self.can_commission():
                got_commission = try_commission(self.stats, self.service)
                if got_commission:
                    self.rank = 1
                    self.history.append("Received a commission.")
                    self.history.append("\tBecame a {rank}.".format(rank=self.get_rank()))
                    self.skill_rolls += 1
                    self.get_commission_skills()

                else:
                    self.history.append("Failed to receive a commission.")
            if 0 < self.rank < max_service_rank(self.service):
                got_promoted = try_promotion(self.stats, self.service)
                if got_promoted:
                    self.history.append("Received a promotion")
                    self.rank += 1
                    self.history.append("\tBecame a {rank}".format(rank=self.get_rank()))
                    self.skill_rolls += 1
                    self.get_promotion_skills()
                else:
                    self.history.append("Failed to get promoted.")
            if self.age == 18 or self.service == "Scouts":
                self.skill_rolls += 2
            else:
                self.skill_rolls += 1
            print(self.skill_rolls)
            self.age += 4
            self.terms += 1
            self.stats = age_stats(self.age, self.stats, self.history)
            if not automatic:
                self.display_tables()
            self.add_skills(automatic=automatic)
            self.reenlist()
        else:
            self.survived = False
            self.history.append("Died during the term.")

    def read_history(self):
        """
            Prints the character creation history
        """
        print("----------------------------------------")
        print("Character log:")
        for i in self.history:
            if i.startswith("Failed") or i.startswith("Forced"):
                res = fg.red + i + fg.rs
            elif i.startswith("Died"):
                res = fg.da_red + i + fg.rs
            elif i.startswith("Learned"):
                res = fg.green + i + fg.rs
            elif i.startswith("Improved"):
                res = fg.li_cyan + i + fg.rs
            elif i.startswith("Received"):
                res = fg.li_yellow + i + fg.rs
            elif i.startswith("Enlisted"):
                res = fg.blue + i + fg.rs
            else:
                res = i
            print(res)
        print("----------------------------------------")

    def add_skill(self, skill):
        """
            Adds one level of skill
            :param skill:
        """
        if skill in self.skills.keys():
            self.skills[skill] += 1
            self.history.append("Improved {sk} to {val}.".format(
                sk=skill,
                val=self.skills[skill]
            ))
            print("Improved {sk} to {val}.".format(
                sk=skill,
                val=self.skills[skill]
            ))
        else:
            self.skills[skill] = 1
            self.history.append("Learned {sk}.".format(sk=skill))
            print("Learned {sk}.".format(sk=skill))

    def char_details(self):
        """
            Generates a descriptive string of details about the character
            with the UPP, service name and rank if present, skills, cash,
            benefits, pension
            :return: a str
        """
        result_str = "UPP: {upp}".format(upp=self.get_upp())
        rank = get_noble_rank(self.stats)
        if not rank == "":
            result_str += "\n" + rank
        if self.rank > 0:
            result_str += "\n{ser} ".format(ser=self.service) + self.get_rank()
        result_str += "\n" + str(self.age) + " years old"
        if not self.skills == {}:
            result_str += "\n" + json.dumps(self.skills)
        if self.cash > 0:
            result_str += "\n{c} Credits".format(c=self.cash)
        if len(self.benefits) > 0:
            result_str += "\n"
            for i in self.benefits:
                result_str += "{i}, ".format(i=i)
            result_str = result_str[:-2]
        if self.pension > 0:
            result_str += "\nPension of {p} Credits".format(p=self.pension)
        return result_str

    def reenlist(self):
        """
            Checks for re enlisting
        """
        self.reenlisting = service_reenlistment(self.service)
        if self.reenlisting == 1:
            self.history.append("Forced to re-enlist in the {ser}.".format(ser=self.service))
        elif self.reenlisting == 0:
            self.history.append("Offered opportunity to re-enlist in the {ser}.".format(ser=self.service))
        else:
            self.history.append("Forced to leave the {ser}.".format(ser=self.service))

    def add_skills(self, automatic=False):
        """
            Rolls on tables for skills and checks for cascading skill choices
        """
        for _ in range(self.skill_rolls):
            skill = None
            while skill is None:
                if automatic:
                    skill = roll_skill(self.stats["Edu"], self.service, automatic=True)
                else:
                    skill = roll_skill(self.stats["Edu"], self.service)
                print("None encountered")
            if skill.startswith("1"):
                split_skills = skill.split()
                self.stats[split_skills[1]] += 1
                self.history.append("Improved {skill} by 1".format(skill=split_skills[1]))
                print("Improved {skill} by 1".format(skill=split_skills[1]))
            elif skill.startswith("-"):
                split_skills = skill[1:].split()
                self.stats[split_skills[1]] -= 1
                self.history.append("Decreased {skill} by 1".format(skill=split_skills[1]))
                print("Decreased {skill} by 1".format(skill=split_skills[1]))
            else:
                if skill in CASCADE_SKILLS:
                    if skill == "Blade Combat":
                        if not automatic:
                            print(BLADE_CBT_CASC)

                            spe_choice = input("Choose one specialty from above for Blade Combat\n")
                            while spe_choice not in BLADE_CBT_CASC:
                                spe_choice = input("Choose one specialty from above for Blade Combat\n")
                        else:
                            spe_choice_roll = roll_die(len(BLADE_CBT_CASC))
                            spe_choice = BLADE_CBT_CASC[spe_choice_roll - 1]
                        skill = "Blade Combat({spe})".format(spe=spe_choice)
                    elif skill == "Gun Combat":
                        if not automatic:
                            print(GUN_CBT_CASC)
                            spe_choice = input("Choose one specialty from above for Gun Combat\n")
                            while spe_choice not in GUN_CBT_CASC:
                                spe_choice = input("Choose one specialty from above for Gun Combat\n")
                        else:
                            spe_choice_roll = roll_die(len(GUN_CBT_CASC))
                            spe_choice = GUN_CBT_CASC[spe_choice_roll - 1]
                        skill = "Gun Combat({spe})".format(spe=spe_choice)
                    elif skill == "Vehicle":
                        if not automatic:
                            print(VEHICLE_CASC)
                            spe_choice = input("Choose one specialty from above for Vehicle\n")
                            while spe_choice not in VEHICLE_CASC:
                                spe_choice = input("Choose one specialty from above for Vehicle\n")
                        else:
                            spe_choice_roll = roll_die(len(VEHICLE_CASC))
                            spe_choice = VEHICLE_CASC[spe_choice_roll - 1]
                        if spe_choice in ["Aircraft", "Watercraft"]:
                            skill = spe_choice
                        else:
                            skill = "Vehicle({spe})".format(spe=spe_choice)
                    if skill == "Aircraft":
                        if not automatic:
                            print(AIRCRAFT_CASC)
                            spe_choice = input("Choose one specialty from above for Aircraft\n")
                            while spe_choice not in AIRCRAFT_CASC:
                                spe_choice = input("Choose one specialty from above for Aircraft\n")
                        else:
                            spe_choice_roll = roll_die(len(AIRCRAFT_CASC))
                            spe_choice = AIRCRAFT_CASC[spe_choice_roll - 1]
                        skill = "Aircraft({spe})".format(spe=spe_choice)
                    elif skill == "Watercraft":
                        if not automatic:
                            print(WATERCRAFT_CASC)
                            spe_choice = input("Choose one specialty from above for Watercraft\n")
                            while spe_choice not in WATERCRAFT_CASC:
                                spe_choice = input("Choose one specialty from above for Watercraft\n")
                        else:
                            spe_choice_roll = roll_die(len(WATERCRAFT_CASC))
                            spe_choice = WATERCRAFT_CASC[spe_choice_roll - 1]
                        skill = "Watercraft({spe})".format(spe=spe_choice)

                self.add_skill(skill)

    def calc_pension(self):
        """
            Calculates the yearly pension for the character
        """
        if self.terms < 5:
            self.pension = 0
        else:
            self.pension = 4000 + 2000 * (self.terms - 5)

    def roll_cash(self):
        """
            Rolls for cash benefits according to proper table
            and adds it to self.cash
        """
        table = []
        dm = 0
        if self.service == "Navy":
            table = NAVY_CASH
        elif self.service == "Marines":
            table = MARINES_CASH
        elif self.service == "Army":
            table = ARMY_CASH
        elif self.service == "Merchants":
            table = MERCHANTS_CASH
        elif self.service == "Scouts":
            table = SCOUTS_CASH
        elif self.service == "Others":
            table = OTHERS_CASH
        if self.service in ["Army", "Navy", "Marines", "Merchants"] and self.rank >= 5:
            dm += 1
        if "Gambling" in self.skills.keys():
            dm += 1
        roll = roll_die(6) + dm - 1  # offset for array
        self.cash += table[roll]
        self.history.append("Received {c} Credits as a muster-out benefit.".format(c=table[roll]))

    def get_rank(self):
        """
            Returns the string for the rank of the character
        """
        table = []
        if self.service == "Navy":
            table = NAVY_RANKS
        elif self.service == "Marines":
            table = MARINES_RANKS
        elif self.service == "Army":
            table = ARMY_RANKS
        elif self.service == "Merchants":
            table = MERCHANTS_RANKS
        if self.rank == 1:
            return table[0]
        elif self.rank == 2:
            return table[1]
        elif self.rank == 3:
            return table[2]
        elif self.rank == 4:
            return table[3]
        elif self.rank == 5:
            return table[4]
        elif self.rank == 6:
            return table[5]
        else:
            return ""

    def roll_benefit(self):
        """
            Rolls for benefits according to proper table
            :return: a list of benefits as str
        """
        table = []
        dm = 0
        if self.service == "Navy":
            table = NAVY_BENEFITS
        elif self.service == "Marines":
            table = MARINES_BENEFITS
        elif self.service == "Army":
            table = ARMY_BENEFITS
        elif self.service == "Merchants":
            table = MERCHANTS_BENEFITS
        elif self.service == "Scouts":
            table = SCOUTS_BENEFITS
        elif self.service == "Others":
            table = OTHERS_BENEFITS
        if self.service in ["Navy", "Marines", "Army", "Merchants"] and self.rank > 4:
            dm += 1
        roll = roll_die(6) + dm - 1  # offset for array
        if roll >= len(table):
            # for tables that are shorter
            roll = len(table) - 1
        benefit = table[roll]
        return benefit

    def calc_muster_out(self, automatic=False):
        """
            Calculates and asks for player choices on mustering out rolls
            Automatic sets all choices to random
        """
        total_rolls = self.terms
        bonus_ben = 0
        cash_max = 3
        benefits = []
        if 1 <= self.rank <= 2:
            bonus_ben = 1
        elif 3 <= self.rank <= 4:
            bonus_ben = 2
        elif 5 <= self.rank <= 6:
            bonus_ben = 3
        total_rolls += bonus_ben
        self.history.append("Mustering out benefits: {i}".format(i=total_rolls))
        if not automatic:
            while total_rolls > 0:
                if cash_max > 0:
                    x = input("Do you want cash or a benefit? You have {t} total rolls left (max {c} cash rolls). c for cash, "
                              "b for benefit\n".format(
                        c=cash_max,
                        t=total_rolls
                    ))
                    if x == "c":
                        cash_max -= 1
                        total_rolls -= 1
                        self.roll_cash()
                    elif x == "b":
                        total_rolls -= 1
                        benefit = self.roll_benefit()
                        benefits.append(benefit)
                        print(benefit)
                else:
                    total_rolls -= 1
                    benefits.append(self.roll_benefit())
        else:
            while total_rolls > 0:
                if cash_max > 0:
                    cash_or_benefit = roll_die(2)
                    if cash_or_benefit == 0:
                        cash_max -= 1
                        total_rolls -= 1
                        self.roll_cash()
                    else:
                        total_rolls -= 1
                        benefit = self.roll_benefit()
                        benefits.append(benefit)
                else:
                    total_rolls -= 1
                    benefits.append(self.roll_benefit())

        self.benefits = treat_benefits(self.stats, benefits, self.history, automatic=automatic)
        self.calc_pension()

    def save_character(self, name):
        """
            Saves the character log and stats to a file
        """
        with open(name, "w") as f:
            f.write("Character log:\n")
            for event in self.history:
                f.write(event + "\n")
            f.write("\nDetails\n")
            f.write(self.char_details())

    def get_upp(self):
        """
            Produces the Universal Personality Profile
            :return: a string of 6 characters with hexadecimal notation (in caps for letters) representing the UPP
        """
        upp = ""
        upp += hex(self.stats["Str"])[2:].upper()
        upp += hex(self.stats["Dex"])[2:].upper()
        upp += hex(self.stats["End"])[2:].upper()
        upp += hex(self.stats["Int"])[2:].upper()
        upp += hex(self.stats["Edu"])[2:].upper()
        upp += hex(self.stats["Soc"])[2:].upper()
        return upp

