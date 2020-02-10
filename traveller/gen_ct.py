# The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 - 2008 Far Future Enterprises.
# (CF : http://www.farfuture.net/FFEFairUsePolicy2008.pdf)
from utils.dice_roller import sum_roll_dice, roll_die
from sty import fg
from traveller.consts_trav import *
import json

# BOOOOO GLOBALS
history = []
alive = True


def roll_stats():
    """
        Rolls stats according to Classic Traveller's way
        and assigns them in order from Str to Dex to End
        to Int to Edu
        :return: an array of 6 results of 2d6 rolls
    """
    statistics = []
    for i in range(6):
        statistics.append(sum_roll_dice(6, 2))
    dict_stats = {
        "Str": statistics[0],
        "Dex": statistics[1],
        "End": statistics[2],
        "Int": statistics[3],
        "Edu": statistics[4],
        "Soc": statistics[5]
    }
    return dict_stats


def roll_cash(ranks: dict, service: str, skills: dict):
    """
        Rolls for cash benefits according to proper table
        :param ranks: a dictionary with services as keys and int as values
        :param service: the name of the service the character joined
        :param skills: the skills of the character because Gambling affects the roll
        :return: a cash roll as int of the credits won
    """
    table = []
    dm = 0
    if service == "Navy":
        table = NAVY_CASH
    elif service == "Marines":
        table = MARINES_CASH
    elif service == "Army":
        table = ARMY_CASH
    elif service == "Merchants":
        table = MERCHANTS_CASH
    elif service == "Scouts":
        table = SCOUTS_CASH
    elif service == "Others":
        table = OTHERS_CASH
    if service in ["Army", "Navy", "Marines", "Merchants"] and ranks[service] >= 5:
        dm += 1
    if "Gambling" in skills.keys():
        dm += 1
    roll = roll_die(6) + dm - 1  # offset for array
    return table[roll]


def roll_benefit(ranks: dict, service: str):
    """
        Rolls for benefits according to proper table
        :param ranks: a dictionary with services as keys and int as values
        :param service: the name of the service the character joined
        :return: a list of benefits as str
    """
    table = []
    dm = 0
    if service == "Navy":
        table = NAVY_BENEFITS
    elif service == "Marines":
        table = MARINES_BENEFITS
    elif service == "Army":
        table = ARMY_BENEFITS
    elif service == "Merchants":
        table = MERCHANTS_BENEFITS
    elif service == "Scouts":
        table = SCOUTS_BENEFITS
    elif service == "Others":
        table = OTHERS_BENEFITS
    if service in ["Navy", "Marines", "Army", "Merchants"] and ranks[service] > 4:
        dm += 1
    roll = roll_die(6) + dm - 1  # offset for array
    if roll >= len(table):
        # for tables that are shorter
        roll = len(table) - 1
    benefit = table[roll]
    return benefit


def get_rank(rank, service):
    table = []
    if service == "Navy":
        table = NAVY_RANKS
    elif service == "Marines":
        table = MARINES_RANKS
    elif service == "Army":
        table = ARMY_RANKS
    elif service == "Merchants":
        table = MERCHANTS_RANKS
    if rank == 1:
        return table[0]
    elif rank == 2:
        return table[1]
    elif rank == 3:
        return table[2]
    elif rank == 4:
        return table[3]
    elif rank == 5:
        return table[4]
    elif rank == 6:
        return table[5]
    else:
        return ""


def get_upp(dict_stats):
    """
        Produces the Universal Personality Profile
        :param dict_stats: the dict of stats from the character with Str, Dex, End, Int, Edu, Soc
        :return: a string of 6 characters with hexadecimal notation (in caps for letters) representing the UPP
    """
    upp = ""
    upp += hex(dict_stats["Str"])[2:].upper()
    upp += hex(dict_stats["Dex"])[2:].upper()
    upp += hex(dict_stats["End"])[2:].upper()
    upp += hex(dict_stats["Int"])[2:].upper()
    upp += hex(dict_stats["Edu"])[2:].upper()
    upp += hex(dict_stats["Soc"])[2:].upper()
    return upp


def get_noble_rank(stats):
    soc = stats["Soc"]
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


def enlist(stats, service_name: str):
    dm = 0
    limit = 0
    if service_name == "Army":
        if stats["Dex"] > 5:
            dm += 1
        if stats["End"] > 4:
            dm += 2
        limit = 4
    elif service_name == "Marines":
        if stats["Int"] > 7:
            dm += 1
        if stats["Str"] > 7:
            dm += 2
        limit = 8
    elif service_name == "Navy":
        if stats["Int"] > 7:
            dm += 1
        if stats["Edu"] > 8:
            dm += 2
        limit = 7
    elif service_name == "Merchants":
        if stats["Str"] > 6:
            dm += 1
        if stats["Int"] > 5:
            dm += 2
        limit = 6
    elif service_name == "Scouts":
        if stats["Int"] > 5:
            dm += 1
        if stats["Str"] > 7:
            dm += 2
        limit = 6
    elif service_name == "Others":
        limit = 2
    enlist_roll = sum_roll_dice(6, 2) + dm
    if enlist_roll > limit:
        return True
    else:
        return False


def survive(stats, service_name: str):
    dm = 0
    limit = 0
    if service_name == "Army":
        if stats["Edu"] > 6:
            dm += 2
        limit = 4
    elif service_name == "Marines":
        if stats["End"] > 7:
            dm += 2
        limit = 5
    elif service_name == "Navy" or service_name == "Merchants":
        if stats["Int"] > 6:
            dm += 2
        limit = 4
    elif service_name == "Scouts":
        if stats["End"] > 8:
            dm += 2
        limit = 6
    elif service_name == "Others":
        if stats["Int"] > 8:
            dm += 2
        limit = 4
    survival_roll = sum_roll_dice(6, 2) + dm
    if survival_roll > limit:
        return True
    else:
        return False


def try_commission(stats, service_name: str):
    dm = 0
    limit = 0
    if service_name == "Army":
        if stats["End"] > 6:
            dm = 1
        limit = 4
    elif service_name == "Marines":
        if stats["Edu"] > 6:
            dm = 1
        limit = 8
    elif service_name == "Navy":
        if stats["Soc"] > 8:
            dm = 1
        limit = 9
    elif service_name == "Merchants":
        if stats["Int"] > 5:
            dm = 1
        limit = 3
    commission_roll = sum_roll_dice(6, 2) + dm
    if commission_roll > limit:
        return True
    else:
        return False


def try_promotion(stats, service_name: str):
    dm = 0
    limit = 0
    if service_name == "Army":
        limit = 5
        if stats["Edu"] > 5:
            dm += 1
    elif service_name == "Marines":
        limit = 8
        if stats["Soc"] > 7:
            dm += 1
    elif service_name == "Navy":
        limit = 7
        if stats["Edu"] > 7:
            dm += 1
    elif service_name == "Merchants":
        limit = 9
        if stats["Int"] > 8:
            dm += 1
    promotion_roll = sum_roll_dice(6, 2) + dm
    if promotion_roll > limit:
        return True
    else:
        return False


def service_reenlistment(service_name: str):
    """
        Determines if character can, has to or cannot reenlist
        :return: 1 : has to reenlist (nat 12)
                 0 : can reenlist
                -1 : cannot reenlist
    """
    limit = 0
    if service_name == "Army":
        limit = 6
    elif service_name == "Marines" or service_name == "Navy":
        limit = 5
    elif service_name == "Merchants":
        limit = 3
    elif service_name == "Scouts":
        limit = 2
    elif service_name == "Others":
        limit = 4
    reenlist_roll = sum_roll_dice(6, 2)
    if reenlist_roll == 12:
        return 1
    elif reenlist_roll > limit:
        return 0
    else:
        return -1


def calc_muster_out_benefits(ranks, terms, service, skills):
    total_ben = terms
    bonus_ben = 0
    cash = 0
    benefits = []
    for i in ranks:
        if 1 <= ranks[i] <= 2:
            bonus_ben = 1
        elif 3 <= ranks[i] <= 4:
            bonus_ben = 2
        elif 5 <= ranks[i] <= 6:
            bonus_ben = 3
    total_ben += bonus_ben
    history.append("Mustering out benefits: {i}".format(i=total_ben))
    cash_max = 3
    while total_ben > 0:
        if cash_max > 0:
            x = input("Do you want cash or a benefit? You have {t} total rolls left (max {c} cash rolls). c for cash, "
                      "b for benefit\n".format(
                c=cash_max,
                t=total_ben
            ))
            if x == "c":
                cash_max -= 1
                total_ben -= 1
                cash += roll_cash(ranks, service, skills)
                print(cash)
            elif x == "b":
                total_ben -= 1
                benefit = roll_benefit(ranks, service)
                benefits.append(benefit)
                print(benefit)
        else:
            total_ben -= 1
            benefits.append(roll_benefit(ranks, service))
    return cash, benefits


def display_navy_skill_tables(education):
    print("Navy Personal Development Table | Navy Service Skills Table   | Navy Advanced Skills Table")
    print("--------------------------------|-----------------------------|---------------------------")
    print("1 {nav}                         | 1 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[0],
        ser=NAVY_SKILLS_SERVICE[0],
        spa="               ",
        adv=NAVY_SKILLS_ADV[0]))
    print("2 {nav}                         | 2 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[1],
        ser=NAVY_SKILLS_SERVICE[1],
        spa="                 ",
        adv=NAVY_SKILLS_ADV[1]))
    print("3 {nav}                         | 3 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[2],
        ser=NAVY_SKILLS_SERVICE[2],
        spa="          ",
        adv=NAVY_SKILLS_ADV[2]))
    print("4 {nav}                         | 4 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[3],
        ser=NAVY_SKILLS_SERVICE[3],
        spa="                   ",
        adv=NAVY_SKILLS_ADV[3]))
    print("5 {nav}                         | 5 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[4],
        ser=NAVY_SKILLS_SERVICE[4],
        spa="              ",
        adv=NAVY_SKILLS_ADV[4]))
    print("6 {nav}                         | 6 {ser}{spa}| 1 {adv}".format(
        nav=NAVY_SKILLS_PERSONAL_DEV[5],
        ser=NAVY_SKILLS_SERVICE[5],
        spa="                ",
        adv=NAVY_SKILLS_ADV[5]))

    if education > 7:
        print("Navy Advanced Education Skills Table")
        print("------------------------------------")
        print("1 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=NAVY_SKILLS_ADV_EDU[5]))


def display_marines_skill_tables(education):
    print("Marines Personal Development Table | Marines Service Skills Table   | Marines Advanced Skills Table")
    print("-----------------------------------|--------------------------------|------------------------------")
    print("1 {nav}                            | 1 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[0],
        ser=MARINES_SKILLS_SERVICE[0],
        spa="                      ",
        adv=MARINES_SKILLS_ADV[0]))
    print("2 {nav}                            | 2 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[1],
        ser=MARINES_SKILLS_SERVICE[1],
        spa="                    ",
        adv=MARINES_SKILLS_ADV[1]))
    print("3 {nav}                            | 3 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[2],
        ser=MARINES_SKILLS_SERVICE[2],
        spa="                 ",
        adv=MARINES_SKILLS_ADV[2]))
    print("4 {nav}                         | 4 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[3],
        ser=MARINES_SKILLS_SERVICE[3],
        spa="                   ",
        adv=MARINES_SKILLS_ADV[3]))
    print("5 {nav}                         | 5 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[4],
        ser=MARINES_SKILLS_SERVICE[4],
        spa="                 ",
        adv=MARINES_SKILLS_ADV[4]))
    print("6 {nav}                     | 6 {ser}{spa}| 1 {adv}".format(
        nav=MARINES_SKILLS_PERSONAL_DEV[5],
        ser=MARINES_SKILLS_SERVICE[5],
        spa="                   ",
        adv=MARINES_SKILLS_ADV[5]))

    if education > 7:
        print("Marines Advanced Education Skills Table")
        print("------------------------------------")
        print("1 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=MARINES_SKILLS_ADV_EDU[5]))


def display_army_skill_tables(education):
    print("Army Personal Development Table | Army Service Skills Table   | Army Advanced Skills Table")
    print("--------------------------------|-----------------------------|---------------------------")
    print("1 {nav}                         | 1 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[0],
        ser=ARMY_SKILLS_SERVICE[0],
        spa="                   ",
        adv=ARMY_SKILLS_ADV[0]))
    print("2 {nav}                         | 2 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[1],
        ser=ARMY_SKILLS_SERVICE[1],
        spa="                   ",
        adv=ARMY_SKILLS_ADV[1]))
    print("3 {nav}                         | 3 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[2],
        ser=ARMY_SKILLS_SERVICE[2],
        spa="                ",
        adv=ARMY_SKILLS_ADV[2]))
    print("4 {nav}                      | 4 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[3],
        ser=ARMY_SKILLS_SERVICE[3],
        spa="          ",
        adv=ARMY_SKILLS_ADV[3]))
    print("5 {nav}                         | 5 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[4],
        ser=ARMY_SKILLS_SERVICE[4],
        spa="              ",
        adv=ARMY_SKILLS_ADV[4]))
    print("6 {nav}                      | 6 {ser}{spa}| 1 {adv}".format(
        nav=ARMY_SKILLS_PERSONAL_DEV[5],
        ser=ARMY_SKILLS_SERVICE[5],
        spa="                ",
        adv=ARMY_SKILLS_ADV[5]))

    if education > 7:
        print("Army Advanced Education Skills Table")
        print("------------------------------------")
        print("1 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=ARMY_SKILLS_ADV_EDU[5]))


def display_merchants_skill_tables(education):
    print("Merchants Personal Development Table | Merchants Service Skills Table   | Merchants Advanced Skills Table")
    print("-------------------------------------|----------------------------------|--------------------------------")
    print("1 {nav}                              | 1 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[0],
        ser=MERCHANTS_SKILLS_SERVICE[0],
        spa="                        ",
        adv=MERCHANTS_SKILLS_ADV[0]))
    print("2 {nav}                              | 2 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[1],
        ser=MERCHANTS_SKILLS_SERVICE[1],
        spa="                      ",
        adv=MERCHANTS_SKILLS_ADV[1]))
    print("3 {nav}                              | 3 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[2],
        ser=MERCHANTS_SKILLS_SERVICE[2],
        spa="                 ",
        adv=MERCHANTS_SKILLS_ADV[2]))
    print("4 {nav}                              | 4 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[3],
        ser=MERCHANTS_SKILLS_SERVICE[3],
        spa="                        ",
        adv=MERCHANTS_SKILLS_ADV[3]))
    print("5 {nav}                       | 5 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[4],
        ser=MERCHANTS_SKILLS_SERVICE[4],
        spa="                    ",
        adv=MERCHANTS_SKILLS_ADV[4]))
    print("6 {nav}                            | 6 {ser}{spa}| 1 {adv}".format(
        nav=MERCHANTS_SKILLS_PERSONAL_DEV[5],
        ser=MERCHANTS_SKILLS_SERVICE[5],
        spa="                     ",
        adv=MERCHANTS_SKILLS_ADV[5]))

    if education > 7:
        print("Merchants Advanced Education Skills Table")
        print("-----------------------------------------")
        print("1 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=MERCHANTS_SKILLS_ADV_EDU[5]))


def display_scouts_skill_tables(education):
    print("Scouts Personal Development Table | Scouts Service Skills Table   | Scouts Advanced Skills Table")
    print("----------------------------------|-------------------------------|-----------------------------")
    print("1 {nav}                           | 1 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[0],
        ser=SCOUTS_SKILLS_SERVICE[0],
        spa="                     ",
        adv=SCOUTS_SKILLS_ADV[0]))
    print("2 {nav}                           | 2 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[1],
        ser=SCOUTS_SKILLS_SERVICE[1],
        spa="                   ",
        adv=SCOUTS_SKILLS_ADV[1]))
    print("3 {nav}                           | 3 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[2],
        ser=SCOUTS_SKILLS_SERVICE[2],
        spa="                  ",
        adv=SCOUTS_SKILLS_ADV[2]))
    print("4 {nav}                           | 4 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[3],
        ser=SCOUTS_SKILLS_SERVICE[3],
        spa="                  ",
        adv=SCOUTS_SKILLS_ADV[3]))
    print("5 {nav}                           | 5 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[4],
        ser=SCOUTS_SKILLS_SERVICE[4],
        spa="                 ",
        adv=SCOUTS_SKILLS_ADV[4]))
    print("6 {nav}                      | 6 {ser}{spa}| 1 {adv}".format(
        nav=SCOUTS_SKILLS_PERSONAL_DEV[5],
        ser=SCOUTS_SKILLS_SERVICE[5],
        spa="              ",
        adv=SCOUTS_SKILLS_ADV[5]))

    if education > 7:
        print("Scouts Advanced Education Skills Table")
        print("--------------------------------------")
        print("1 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=SCOUTS_SKILLS_ADV_EDU[5]))


def display_others_skill_tables(education):
    print("Others Personal Development Table | Others Service Skills Table   | Others Advanced Skills Table")
    print("----------------------------------|-------------------------------|-----------------------------")
    print("1 {nav}                           | 1 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[0],
        ser=OTHERS_SKILLS_SERVICE[0],
        spa="                     ",
        adv=OTHERS_SKILLS_ADV[0]))
    print("2 {nav}                           | 2 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[1],
        ser=OTHERS_SKILLS_SERVICE[1],
        spa="                   ",
        adv=OTHERS_SKILLS_ADV[1]))
    print("3 {nav}                           | 3 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[2],
        ser=OTHERS_SKILLS_SERVICE[2],
        spa="                  ",
        adv=OTHERS_SKILLS_ADV[2]))
    print("4 {nav}                    | 4 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[3],
        ser=OTHERS_SKILLS_SERVICE[3],
        spa="                  ",
        adv=OTHERS_SKILLS_ADV[3]))
    print("5 {nav}                        | 5 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[4],
        ser=OTHERS_SKILLS_SERVICE[4],
        spa="                 ",
        adv=OTHERS_SKILLS_ADV[4]))
    print("6 {nav}                          | 6 {ser}{spa}| 1 {adv}".format(
        nav=OTHERS_SKILLS_PERSONAL_DEV[5],
        ser=OTHERS_SKILLS_SERVICE[5],
        spa="              ",
        adv=OTHERS_SKILLS_ADV[5]))

    if education > 7:
        print("Others Advanced Education Skills Table")
        print("--------------------------------------")
        print("1 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[0]))
        print("2 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[1]))
        print("3 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[2]))
        print("4 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[3]))
        print("5 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[4]))
        print("6 {nav}".format(nav=OTHERS_SKILLS_ADV_EDU[5]))


def roll_skill(education, service_name):
    pers_tab = []
    adv_skill_tab = []
    serv_skill_tab = []
    adv_edu_tab = []
    if service_name == "Navy":
        pers_tab = NAVY_SKILLS_PERSONAL_DEV
        adv_skill_tab = NAVY_SKILLS_ADV
        serv_skill_tab = NAVY_SKILLS_SERVICE
        adv_edu_tab = NAVY_SKILLS_ADV_EDU
    elif service_name == "Marines":
        pers_tab = MARINES_SKILLS_PERSONAL_DEV
        adv_skill_tab = MARINES_SKILLS_ADV
        serv_skill_tab = MARINES_SKILLS_SERVICE
        adv_edu_tab = MARINES_SKILLS_ADV_EDU
    elif service_name == "Army":
        pers_tab = ARMY_SKILLS_PERSONAL_DEV
        adv_skill_tab = ARMY_SKILLS_ADV
        serv_skill_tab = ARMY_SKILLS_SERVICE
        adv_edu_tab = ARMY_SKILLS_ADV_EDU
    elif service_name == "Merchants":
        pers_tab = MERCHANTS_SKILLS_PERSONAL_DEV
        adv_skill_tab = MERCHANTS_SKILLS_ADV
        serv_skill_tab = MERCHANTS_SKILLS_SERVICE
        adv_edu_tab = MERCHANTS_SKILLS_ADV_EDU
    elif service_name == "Scouts":
        pers_tab = SCOUTS_SKILLS_PERSONAL_DEV
        adv_skill_tab = SCOUTS_SKILLS_ADV
        serv_skill_tab = SCOUTS_SKILLS_SERVICE
        adv_edu_tab = SCOUTS_SKILLS_ADV_EDU
    elif service_name == "Others":
        pers_tab = OTHERS_SKILLS_PERSONAL_DEV
        adv_skill_tab = OTHERS_SKILLS_ADV
        serv_skill_tab = OTHERS_SKILLS_SERVICE
        adv_edu_tab = OTHERS_SKILLS_ADV_EDU
    if education > 7:
        more = ", 4 for Advanced Education\n"
    else:
        more = "\n"
    table = 0
    while int(table) not in [1, 2, 3, 4]:
        table = input("Choose a Table to roll on, 1 for Personal Development, "
                      "2 for Service Skills, 3 for Advanced Skills{more}".format(more=more))
    roll = roll_die(6) - 1
    if table == "1":
        return pers_tab[roll]
    elif table == "2":
        return serv_skill_tab[roll]
    elif table == "3":
        return adv_skill_tab[roll]
    elif table == "4" and education > 7:
        return adv_edu_tab[roll]


def add_skills(stats, skills, skill_rolls, service_name):
    for i in range(skill_rolls):
        skill = roll_skill(stats["Edu"], service_name)
        if skill.startswith("1"):
            split_skills = skill.split()
            stats[split_skills[1]] += 1
            history.append("Improved {skill} by 1".format(skill=split_skills[1]))
        elif skill.startswith("-"):
            split_skills = skill[1:].split()
            stats[split_skills[1]] -= 1
            history.append("Decreased {skill} by 1".format(skill=split_skills[1]))
        else:
            if skill in CASCADE_SKILLS:
                if skill == "Blade Combat":
                    print(BLADE_CBT_CASC)
                    spe_choice = input("Choose one specialty from above for Blade Combat\n")
                    while spe_choice not in BLADE_CBT_CASC:
                        spe_choice = input("Choose one specialty from above for Blade Combat\n")
                    skill = "Blade Combat({spe})".format(spe=spe_choice)
                elif skill == "Gun Combat":
                    print(GUN_CBT_CASC)
                    spe_choice = input("Choose one specialty from above for Gun Combat\n")
                    while spe_choice not in GUN_CBT_CASC:
                        spe_choice = input("Choose one specialty from above for Gun Combat\n")
                    skill = "Gun Combat({spe})".format(spe=spe_choice)
                elif skill == "Vehicle":
                    print(VEHICLE_CASC)
                    spe_choice = input("Choose one specialty from above for Vehicle\n")
                    while spe_choice not in VEHICLE_CASC:
                        spe_choice = input("Choose one specialty from above for Vehicle\n")
                    if spe_choice in ["Aircraft", "Watercraft"]:
                        skill = spe_choice
                    else:
                        skill = "Vehicle({spe})".format(spe=spe_choice)
                if skill == "Aircraft":
                    print(AIRCRAFT_CASC)
                    spe_choice = input("Choose one specialty from above for Aircraft\n")
                    while spe_choice not in AIRCRAFT_CASC:
                        spe_choice = input("Choose one specialty from above for Aircraft\n")
                    skill = "Aircraft({spe})".format(spe=spe_choice)
                elif skill == "Watercraft":
                    print(WATERCRAFT_CASC)
                    spe_choice = input("Choose one specialty from above for Watercraft\n")
                    while spe_choice not in WATERCRAFT_CASC:
                        spe_choice = input("Choose one specialty from above for Watercraft\n")
                    skill = "Watercraft({spe})".format(spe=spe_choice)

            if skill in skills:
                skills[skill] += 1
                history.append("Improved {skill} to {val}.".format(
                    skill=skill,
                    val=skills[skill]))
            else:
                history.append("Learned {skill}.".format(skill=skill))
                skills[skill] = 1

            print(skill)


def calc_navy_term(stats, ranks, commissions, age, skills, draft, term):
    survived = survive(stats, "Navy")
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        if ranks["Navy"] == 0:
            if not draft or term > 0:
                comm = try_commission(stats, "Navy")
                if comm:
                    history.append("Received a commission.")
                    ranks["Navy"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Navy"], "Navy")))
                    commissions["Navy"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Navy"] and ranks["Navy"] < 6:
            promoted = try_promotion(stats, "Navy")
            if promoted:
                history.append("Received a promotion.")
                ranks["Navy"] += 1
                history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Navy"], "Navy")))
                if ranks["Navy"] == 5:
                    stats["Soc"] += 1
                    history.append("Improved Soc by 1.")
                if ranks["Navy"] == 6:
                    stats["Soc"] += 1
                    history.append("Improved Soc by 1.")
                skill_rolls += 1
            else:
                history.append("Failed to get promoted.")
        if term == 0:
            skill_rolls += 2
        else:
            skill_rolls += 1

        display_navy_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Navy")
        return True

    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def calc_marines_term(stats, ranks, commissions, age, skills, draft, term):
    survived = survive(stats, "Marines")
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        # when drafted cannot get commission at first term
        if ranks["Marines"] == 0:
            if not draft or term > 0:
                comm = try_commission(stats, "Marines")
                if comm:
                    history.append("Received a commission.")
                    ranks["Marines"] = 1
                    skills["Gun Combat(Revolver)"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Marines"], "Marines")))
                    history.append("Learned Gun Combat(Revolver).")
                    commissions["Marines"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Marines"] and ranks["Marines"] < 7:
            promoted = try_promotion(stats, "Marines")
            if promoted:
                history.append("Received a promotion.")
                ranks["Marines"] += 1
                history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Marines"], "Marines")))
                skill_rolls += 1
            else:
                history.append("Failed to get promoted.")
        if term == 1:
            skill_rolls += 2
        else:
            skill_rolls += 1

        display_marines_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Marines")
        return True

    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def calc_army_term(stats, ranks, commissions, age, skills, draft, term):
    survived = survive(stats, "Army")
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        if ranks["Army"] == 0:
            if not draft or term > 0:
                comm = try_commission(stats, "Army")
                if comm:
                    history.append("Received a commission.")
                    ranks["Army"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Army"], "Army")))
                    skills["Gun Combat(SMG)"] = 1
                    history.append("Learned Gun Combat(SMG).")
                    commissions["Army"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Army"] and ranks["Army"] < 7:
            promoted = try_promotion(stats, "Army")
            if promoted:
                history.append("Received a promotion.")
                ranks["Army"] += 1
                history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Army"], "Army")))
                skill_rolls += 1
            else:
                history.append("Failed to get promoted.")
        if term == 0:
            skill_rolls += 2
        else:
            skill_rolls += 1

        display_army_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Army")
        return True

    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def calc_merchants_term(stats, ranks, commissions, age, skills, draft, term):
    survived = survive(stats, "Merchants")
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        if ranks["Merchants"] == 0:
            if not draft or term > 0:
                comm = try_commission(stats, "Merchants")
                if comm:
                    history.append("Received a commission.")
                    ranks["Merchants"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Merchants"], "Merchants")))
                    commissions["Merchants"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Merchants"] and ranks["Merchants"] < 6:
            promoted = try_promotion(stats, "Merchants")
            if promoted:
                history.append("Received a promotion.")
                ranks["Merchants"] += 1
                history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Merchants"], "Merchants")))
                skill_rolls += 1
                if ranks["Merchants"] == 3:
                    skills["Pilot"] = 1
                    history.append("Learned Pilot.")
            else:
                history.append("Failed to get promoted.")
        if term == 0:
            skill_rolls += 2
        else:
            skill_rolls += 1

        display_merchants_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Merchants")
        return True

    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def calc_scouts_term(stats, age, skills):
    survived = survive(stats, "Scouts")
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 2
        display_scouts_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Scouts")
        return True
    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def calc_others_term(stats, age, skills, term):
    survived = survive(stats, "Others")
    if survived:
        history.append("Survived the term.")
        age += 4
        if term == 0:
            skill_rolls = 2
        else:
            skill_rolls = 1
        display_others_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Others")
        return True
    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def read_history():
    print("----------------------------------------")
    print("Character log:")
    for i in history:
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
        else:
            res = i
        print(res)
    print("----------------------------------------")


def age_stats(age, stats):
    if age < 34:
        print("No age effect as of yet.")
        return stats
    elif age < 50:
        print("First rolls for age.")
        roll = sum_roll_dice(6, 2)
        if roll < 8:
            stats["Str"] -= 1
            history.append("Lost 1 Strength to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 7:
            stats["Dex"] -= 1
            history.append("Lost 1 Dexterity to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 8:
            stats["End"] -= 1
            history.append("Lost 1 Endurance to age.")
    elif age < 66:
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["Str"] -= 1
            history.append("Lost 1 Strength to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 8:
            stats["Dex"] -= 1
            history.append("Lost 1 Dexterity to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["End"] -= 1
            history.append("Lost 1 Endurance to age.")
    if age > 65:
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["Str"] -= 2
            history.append("Lost 2 Strength to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["Dex"] -= 2
            history.append("Lost 2 Dexterity to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["End"] -= 2
            history.append("Lost 2 Endurance to age.")
        roll = sum_roll_dice(6, 2)
        if roll < 9:
            stats["Int"] -= 1
            history.append("Lost 1 Intelligence to age.")
    return stats


def marines_career(term, stats, ranks, commissions, age, skills, draft):
    if draft:
        history.append("Drafted into the Marines.")
    else:
        history.append("Successfully enlisted in the Marines.")

    still_alive = True
    out_of_marines = False
    skills["Blade Combat(Cutlass)"] = 1
    history.append("Learned Blade Combat(Cutlass).")
    while still_alive and not out_of_marines:
        print("Term {i}".format(i=term))
        still_alive = calc_marines_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Marines")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Marines.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Marines.")
                else:
                    history.append("Chose to leave the Marines.")
                    out_of_marines = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Marines.")
                out_of_marines = True
    return term, still_alive, age


def navy_career(term, stats, ranks, commissions, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in the Navy.")
    else:
        history.append("Drafted in the Navy.")
    still_alive = True
    out_of_navy = False
    while still_alive and not out_of_navy:
        still_alive = calc_navy_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Navy")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Navy.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Navy.")
                else:
                    history.append("Chose to leave the Navy.")
                    out_of_navy = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Navy.")
                out_of_navy = True
    return term, still_alive, age


def army_career(term, stats, ranks, commissions, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in the Army.")
    else:
        history.append("Drafted in the Army.")
    still_alive = True
    out_of_army = False
    skills["Gun Combat(Rifle)"] = 1
    history.append("Learned Gun Combat(Rifle).")
    while still_alive and not out_of_army:
        still_alive = calc_army_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Army")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Army.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Army.")
                else:
                    history.append("Chose to leave the Army.")
                    out_of_army = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Army.")
                out_of_army = True
    return term, still_alive, age


def merchant_career(term, stats, ranks, commissions, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in the Merchants.")
    else:
        history.append("Drafted in the Merchants.")
    still_alive = True
    out_of_merchants = False
    while still_alive and not out_of_merchants:
        still_alive = calc_merchants_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Merchants")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Merchants.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Merchants.")
                else:
                    history.append("Chose to leave the Merchants.")
                    out_of_merchants = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Merchants.")
                out_of_merchants = True
    return term, still_alive, age


def scout_career(term, stats, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in the Scouts.")
    else:
        history.append("Drafted in the Scouts.")
    still_alive = True
    out_of_scouts = False
    skills["Pilot"] = 1
    history.append("Learned Pilot.")
    while still_alive and not out_of_scouts:
        still_alive = calc_scouts_term(stats, age, skills)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Scouts")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Scouts.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Scouts.")
                else:
                    history.append("Chose to leave the Scouts.")
                    out_of_scouts = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Scouts.")
                out_of_scouts = True
    return term, still_alive, age


def other_career(term, stats, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in Others.")
    else:
        history.append("Drafted in the Others.")
    still_alive = True
    out_of_others = False
    while still_alive and not out_of_others:
        still_alive = calc_others_term(stats, age, skills, term)
        term += 1
        age += 4
        if still_alive:
            stats = age_stats(age, stats)
            can_reenlist = service_reenlistment("Others")
            if can_reenlist == 1:
                history.append("Forced to re-enlist in the Others.")
                pass
            elif can_reenlist == 0:
                choice = input("Do you want to re-enlist? X to re-enlist\n")
                if choice == "X":
                    history.append("Chose to re-enlist in the Others.")
                else:
                    history.append("Chose to leave the Others.")
                    out_of_others = True
            elif can_reenlist == -1:
                history.append("Forced to leave the Others.")
                out_of_others = True
    return term, still_alive, age


def char_details(stats, commissions, skills, ranks, age, cash, inventory, pension=0):
    result_str = "UPP: {upp}".format(upp=get_upp(stats))
    rank = get_noble_rank(stats)
    if not rank == "":
        result_str += "\n" + rank
    if commissions["Navy"]:
        result_str += "\nNavy " + get_rank(ranks["Navy"], "Navy")
    elif commissions["Marines"]:
        result_str += "\nMarines " + get_rank(ranks["Marines"], "Marines")
    elif commissions["Army"]:
        result_str += "\nArmy " + get_rank(ranks["Army"], "Army")
    elif commissions["Merchants"]:
        result_str += "\nMerchants " + get_rank(ranks["Merchants"], "Merchants")
    result_str += "\n" + str(age) + " years old"
    if not skills == {}:
        result_str += "\n" + json.dumps(skills)
    if cash > 0:
        result_str += "\n{c} Credits".format(c=cash)
    if len(inventory) > 0:
        result_str += "\n"
        for i in inventory:
            result_str += "{i}, ".format(i=i)
        result_str = result_str[:-2]
    if pension > 0:
        result_str += "\nPension of {p} Credits".format(p=pension)
    return result_str


def treat_benefits(stats, benefits_list):
    benefits = []
    for benefit in benefits_list:
        if benefit.startswith("+"):
            skill_benefits = benefit[1:].split()
            stats[skill_benefits[1]] += int(skill_benefits[0])
            history.append("Improved {skill} by {am} as a muster-out benefit.".format(skill=skill_benefits[1],
                                                                                      am=skill_benefits[0]))
        elif benefit.startswith("Blade"):
            print(BLADE_CBT_CASC)
            blade = input("Choose a type of blade to receive.\n")
            while blade not in BLADE_CBT_CASC:
                blade = input("Choose a type of blade to receive.\n")
            benefits.append(blade)
            history.append("Received a {blade} as a muster-out benefit.".format(blade=blade))
        elif benefit.startswith("Gun"):
            print(GUN_CBT_CASC)
            gun = input("Choose a type of gun to receive.\n")
            while gun not in GUN_CBT_CASC:
                gun = input("Choose a type of gun to receive.\n")
            benefits.append(gun)
            history.append("Received a {gun} as a muster-out benefit.".format(gun=gun))
        else:
            if benefit == "Travellers' Aid Society":
                if benefit not in benefits:
                    benefits.append(benefit)
                    history.append("Received a membership of the {ben} as a muster-out benefit.".format(ben=benefit))
            elif benefit in ["High Passage", "Middle Passage", "Low Passage"]:
                pass
            else:
                benefits.append(benefit)
                history.append("Received a {ben} as a muster-out benefit.".format(ben=benefit))

    high_pass_nb = sum(map(lambda i: i == "High Passage", benefits_list))
    low_pass_nb = sum(map(lambda i: i == "Low Passage", benefits_list))
    mid_pass_nb = sum(map(lambda i: i == "Middle Passage", benefits_list))
    if high_pass_nb > 0:
        benefits.append("{i} High Passage(s)".format(i=high_pass_nb))
        history.append("Received {i} High Passage(s) as a muster-out benefit.".format(i=high_pass_nb))
    if mid_pass_nb > 0:
        benefits.append("{i} Middle Passage(s)".format(i=mid_pass_nb))
        history.append("Received {i} Middle Passage(s) as a muster-out benefit.".format(i=mid_pass_nb))
    if low_pass_nb > 0:
        benefits.append("{i} Low Passage(s)".format(i=low_pass_nb))
        history.append("Received {i} Low Passage(s) as a muster-out benefit.".format(i=low_pass_nb))

    return benefits


def check_retirement(terms: int):
    """
        Calculates the pension (minimum 5 terms to have a pension)
        :param terms: number of terms served
        :return: int: credits per year
    """
    if terms < 5:
        return 0
    else:
        return 4000 + 2000 * (terms - 5)


def save_character(details: str, filename: str):
    """
        Saves the character log and stats to a file
        The log is in a global variable called history
        TODO: change this
        :param details: the stats of the characters
        :param filename: resulting file name to save
    """
    with open(save, "w") as f:
        f.write("Character log:\n")
        for event in history:
            f.write(event + "\n")
        f.write("\nDetails\n")
        f.write(details_str)


if __name__ == "__main__":
    running = True
    while running:
        age = 18
        term = 0
        benefit_rolls = 0
        alive = True
        history = []
        enlisted = False
        stats = roll_stats()
        ranks = {
            "Navy": 0,
            "Marines": 0,
            "Army": 0,
            "Merchants": 0
        }
        commissions = {
            "Navy": False,
            "Marines": False,
            "Army": False,
            "Merchants": False,
        }
        skills = {}
        choice = input("Choose service to try for: (Navy, Marines, Army, Scouts, Merchants, Others)\n")
        if choice == "Navy":
            got_in_navy = enlist(stats, "Navy")
            if got_in_navy:
                enlisted = True
                term, alive, age = navy_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Navy.")
        elif choice == "Marines":
            got_in_marines = enlist(stats, "Marines")
            if got_in_marines:
                enlisted = True
                term, alive, age = marines_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Marines.")
        elif choice == "Army":
            got_in_army = enlist(stats, "Army")
            if got_in_army:
                enlisted = True
                term, alive, age = army_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Army.")
        elif choice == "Merchants":
            got_in_merchants = enlist(stats, "Merchants")
            if got_in_merchants:
                enlisted = True
                term, alive, age = merchant_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Merchants.")
        elif choice == "Scouts":
            got_in_scouts = enlist(stats, "Scouts")
            if got_in_scouts:
                enlisted = True
                term, alive, age = scout_career(term, stats, age, skills, False)
            else:
                history.append("Failed to enlist in the Scouts.")
        elif choice == "Others":
            got_in_others = enlist(stats, "Others")
            if got_in_others:
                enlisted = True
                term, alive, age = other_career(term, stats, age, skills, False)
            else:
                history.append("Failed to enlist in the Others.")
        elif choice == "Q":
            running = False
        if not enlisted:
            print("You're being drafted")
            history.append("Submitted to the Draft.")
            a = roll_die(6) - 1
            if a == 0:
                term, alive, age = marines_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Marines"
            elif a == 1:
                term, alive, age = navy_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Navy"
            elif a == 2:
                term, alive, age = army_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Army"
            elif a == 3:
                term, alive, age = merchant_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Merchants"
            elif a == 4:
                term, alive, age = scout_career(term, stats, age, skills, True)
                choice = "Scouts"
            elif a == 5:
                term, alive, age = other_career(term, stats, age, skills, True)
                choice = "Others"
        pension = 0
        if alive:
            pension = check_retirement(term)
            cash, benefits_list = calc_muster_out_benefits(ranks, term, choice, skills)
            inventory = treat_benefits(stats, benefits_list)
            if cash > 0:
                history.append("Received {c} Credits as a muster-out benefit.".format(c=cash))
        else:
            cash = 0
            inventory = []
        read_history()
        details_str= char_details(stats, commissions, skills, ranks, age, cash, inventory, pension=pension)
        print(details_str)
        save = input("Do you want to save file? Anything else than No will produce a file of this name\n")
        if save != "No":
            save_character(details_str, save)
