# The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 - 2008 Far Future Enterprises.
# (CF : http://www.farfuture.net/FFEFairUsePolicy2008.pdf)
import json
import re

from sty import fg

from traveller.funcs_ct import roll_stats, enlist, survive, try_commission, max_service_rank, try_promotion \
    , age_stats, service_reenlistment, roll_skill, display_navy_skill_tables, \
    display_marines_skill_tables, display_scouts_skill_tables, display_merchants_skill_tables, \
    display_army_skill_tables, display_others_skill_tables
from utils.dice_roller import roll_die
from traveller.consts_trav import *
from utils.utilities import CTEncoder


class CTCharacter:
    """
        Class for Classic Traveller characters
    """

    def __init__(self, name=None):
        if name is None:
            self.name = "Traveller"
        else:
            self.name = name
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

    def choose_service(self, service_name: str, automatic=False):
        """
            Selects the service, if enlistment fails, draft
            :param service_name:
            :param automatic False by default for autogen
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
        self.get_service_skills(automatic=automatic)

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

    def get_service_skills(self, automatic=False):
        """
            Gives character the skills granted by service
        """
        if self.service == "Marines":
            self.add_skill("Blade Combat(Cutlass)", automatic)
        elif self.service == "Army":
            self.add_skill("Gun Combat(Rifle)", automatic)
        elif self.service == "Scouts":
            self.add_skill("Pilot", automatic)

    def get_promotion_skills(self, automatic=False):
        """
            Gives characters skills granted by promotion
        """
        if self.service == "Navy" and self.rank in [5, 6]:
            self.stats["Soc"] += 1
            self.history.append("Improved Soc by 1 from promotion.")
        elif self.service == "Merchants" and self.rank == 3:
            self.add_skill("Pilot", automatic=automatic)

    def get_commission_skills(self, automatic=False):
        """
            Gives characters skills granted by commission
        """
        if self.service == "Marines":
            self.add_skill("Gun Combat(Revolver)", automatic=automatic)
        elif self.service == "Army":
            self.add_skill("Gun Combat(SMG)", automatic=automatic)

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
                    self.history.append("Became a {rank}.".format(rank=self.get_rank()))
                    self.skill_rolls += 1
                    self.get_commission_skills(automatic=automatic)

                else:
                    self.history.append("Failed to receive a commission.")
            if 0 < self.rank < max_service_rank(self.service):
                got_promoted = try_promotion(self.stats, self.service)
                if got_promoted:
                    self.history.append("Received a promotion")
                    self.rank += 1
                    self.history.append("Became a {rank}".format(rank=self.get_rank()))
                    self.skill_rolls += 1
                    self.get_promotion_skills(automatic=automatic)
                else:
                    self.history.append("Failed to get promoted.")
            if self.age == 18 or self.service == "Scouts":
                self.skill_rolls += 2
            else:
                self.skill_rolls += 1
            self.age += 4
            self.terms += 1
            self.stats = age_stats(self.age, self.stats, self.history, automatic=automatic)
            # check for too low values, decrements by 1 or 2, so can reach 0 or -1
            if 0 in self.stats.values() or -1 in self.stats.values():
                self.history.append("Stats lowered too much, died of old age.")
                self.survived = False
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
            elif i.startswith("Became"):
                res = "\t" + i
            else:
                res = i
            print(res)
        print("----------------------------------------")

    def add_skill(self, skill, automatic=False):
        """
            Adds one level of skill
            :param skill:
            :param automatic false by default to avoid unnecessary prints in auto gen
        """
        if skill in self.skills.keys():
            self.skills[skill] += 1
            self.history.append("Improved {sk} to {val}.".format(
                sk=skill,
                val=self.skills[skill]
            ))
            if not automatic:
                print("Improved {sk} to {val}.".format(
                    sk=skill,
                    val=self.skills[skill]
                ))
        else:
            self.skills[skill] = 1
            self.history.append("Learned {sk}.".format(sk=skill))
            if not automatic:
                print("Learned {sk}.".format(sk=skill))

    def char_details(self):
        """
            Generates a descriptive string of details about the character
            with the UPP, service name and rank if present, skills, cash,
            benefits, pension
            :return: a str
        """
        result_str = "UPP: {upp}".format(upp=self.get_upp())
        rank = self.get_noble_rank()
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
            if skill.startswith("1"):
                split_skills = skill.split()
                self.stats[split_skills[1]] += 1
                self.history.append("Improved {skill} by 1".format(skill=split_skills[1]))
                if not automatic:
                    print("Improved {skill} by 1".format(skill=split_skills[1]))
            elif skill.startswith("-"):
                split_skills = skill[1:].split()
                self.stats[split_skills[1]] -= 1
                self.history.append("Decreased {skill} by 1".format(skill=split_skills[1]))
                if not automatic:
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

                self.add_skill(skill, automatic=automatic)

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

    def get_noble_rank(self):
        soc = self.stats["Soc"]
        if soc < 11:
            return ""
        elif soc == 11:
            return "Knight, Knightess, Dame"
        elif soc == 12:
            return "Baron, Baronet, Baroness"
        elif soc == 13:
            return "Marquis, Marquesa, Marchioness"
        elif soc == 14:
            return "Count, Countess, Contessa"
        elif soc == 15:
            return "Duke, Duchess"

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
        if self.reenlisting == 0:
            self.history.append("Chose to leave the {ser}".format(ser=self.service))
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
                    x = input("Do you want cash or a benefit? You have {t} total rolls left (max {c} cash rolls)."
                              " c for cash, b for benefit\n".format(
                                c=cash_max,
                                t=total_rolls
                                )
                    )
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
                    if cash_or_benefit == 1:
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

        self.benefits = self.treat_benefits(benefits, automatic=automatic)
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

    def export_character_to_json(self):
        """
            Changes the character to a json
        """
        character = json.dumps(self, cls=CTEncoder)
        return character

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

    def treat_benefits(self, benefits_list, automatic=False):
        benefits = []
        received_weapon = ""
        for benefit in benefits_list:
            if benefit.startswith("+"):
                skill_benefits = benefit[1:].split()
                self.stats[skill_benefits[1]] += int(skill_benefits[0])
                self.history.append("Improved {skill} by {am} as a muster-out benefit.".format(
                    skill=skill_benefits[1],
                    am=skill_benefits[0]))
            elif benefit.startswith("Gun") or benefit.startswith("Blade"):
                if received_weapon == "":
                    received_weapon = self.benefit_weapon(benefit, automatic)
                    benefits.append(received_weapon)
                else:
                    self.improve_weapon_skill(received_weapon)
            else:
                if benefit == "Travellers' Aid Society":
                    if benefit not in benefits:
                        benefits.append(benefit)
                        self.history.append(
                            "Received a membership of the {ben} as a muster-out benefit.".format(ben=benefit))
                elif benefit not in ["High Passage", "Middle Passage", "Low Passage"]:
                    benefits.append(benefit)
                    self.history.append("Received a {ben} as a muster-out benefit.".format(ben=benefit))

        high_pass_nb = sum(map(lambda i: i == "High Passage", benefits_list))
        low_pass_nb = sum(map(lambda i: i == "Low Passage", benefits_list))
        mid_pass_nb = sum(map(lambda i: i == "Middle Passage", benefits_list))
        if high_pass_nb > 0:
            benefits.append("{i} High Passage(s)".format(i=high_pass_nb))
            self.history.append("Received {i} High Passage(s) as a muster-out benefit.".format(i=high_pass_nb))
        if mid_pass_nb > 0:
            benefits.append("{i} Middle Passage(s)".format(i=mid_pass_nb))
            self.history.append("Received {i} Middle Passage(s) as a muster-out benefit.".format(i=mid_pass_nb))
        if low_pass_nb > 0:
            benefits.append("{i} Low Passage(s)".format(i=low_pass_nb))
            self.history.append("Received {i} Low Passage(s) as a muster-out benefit.".format(i=low_pass_nb))
        return benefits

    def check_for_sub_skill(self, skill_group):
        """
            Checks if a skill type exists in the character skill set and returns the list of the sub skills
            :param skill_group: the skill set to check for
            :return: a list
        """
        matching_sub_skills = [x for x in self.skills if skill_group in x]
        res_matches = []
        for match in matching_sub_skills:
            match = re.sub(skill_group, "", match)
            match = match.replace(")", "")
            match = match.replace("(", "")
            res_matches.append(match)
        return res_matches

    def benefit_weapon(self, benefit, automatic=False):
        """
            If the benefit is a weapon, check for skills the character has and picks a weapon in this category if
            automatic, else just displays the information
            :param benefit: the weapon type
            :param automatic: if it's automatic or not
            :return: the weapon to add to the benefits
        """
        has_skill = self.check_for_sub_skill(benefit + " Combat")
        # print("Skills are: {h}".format(h=has_skill))
        if benefit == "Blade":
            table = BLADE_CBT_CASC
        else:
            table = GUN_CBT_CASC
        if not automatic:
            if len(has_skill) > 0:
                print("You have the following skills in {group}: {b}".format(
                    group=benefit,
                    b=has_skill
                ))
            print(table)
            weapon = input("Choose a type of {w} to receive.\n".format(
                w=benefit
            ))
            while weapon not in table:
                weapon = input("Choose a type of {w} to receive.\n".format(
                    w=benefit
                ))
            received_weapon = weapon
        else:
            if len(has_skill) > 0:
                received_weapon = has_skill[0]
            else:
                weapon_choice = roll_die(len(table))
                received_weapon = table[weapon_choice - 1]
        self.history.append("Received a {w} as a muster-out benefit.".format(w=received_weapon))
        return received_weapon

    def improve_weapon_skill(self, weapon):
        """
            Improves a weapon skill in case of double picks
            TODO:add choice if not automatic
            :param weapon:
            :return:
        """
        weapon_type = ""
        if weapon in BLADE_CBT_CASC:
            weapon_type = "Blade Combat"
        elif weapon in GUN_CBT_CASC:
            weapon_type = "Gun Combat"
        self.add_skill(weapon_type + "(" + weapon + ")")
