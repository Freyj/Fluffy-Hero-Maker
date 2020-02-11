# The Traveller game in all forms is owned by Far Future Enterprises. Copyright 1977 - 2008 Far Future Enterprises.
# (CF : http://www.farfuture.net/FFEFairUsePolicy2008.pdf)
from utils.dice_roller import sum_roll_dice, roll_die

from traveller.consts_trav import *



def roll_stats():
    """
        Rolls stats according to Classic Traveller's way
        and assigns them in order from Str to Dex to End
        to Int to Edu
        :return: an array of 6 results of 2d6 rolls
    """
    statistics = []
    for _ in range(6):
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


def get_noble_rank(stats: dict):
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


def survive(stats: dict, service_name: str):
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


def roll_skill(education, service_name, automatic=False):
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
    if not automatic:
        while (table not in ["1", "2", "3", "4"] and education > 7) or (table not in ["1", "2", "3"] and education < 8):
            table = input("Choose a Table to roll on, 1 for Personal Development, "
                          "2 for Service Skills, 3 for Advanced Skills{more}".format(more=more))
    else:
        if education > 7:
            table = str(roll_die(4) + 1)
        else:
            table = str(roll_die(3) + 1)
    roll = roll_die(6) - 1
    if table == "1":
        return pers_tab[roll]
    elif table == "2":
        return serv_skill_tab[roll]
    elif table == "3":
        return adv_skill_tab[roll]
    elif table == "4" and education > 7:
        return adv_edu_tab[roll]


def max_service_rank(service_name: str):
    if service_name == "Army":
        return len(ARMY_RANKS)
    elif service_name == "Navy":
        return len(NAVY_RANKS)
    elif service_name == "Marines":
        return len(MARINES_RANKS)
    elif service_name == "Merchants":
        return len(MERCHANTS_RANKS)
    else:
        return 0


def age_stats(age, stats, history):
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


def treat_benefits(stats, benefits_list, history, automatic=False):
    benefits = []
    for benefit in benefits_list:
        if benefit.startswith("+"):
            skill_benefits = benefit[1:].split()
            stats[skill_benefits[1]] += int(skill_benefits[0])
            history.append("Improved {skill} by {am} as a muster-out benefit.".format(skill=skill_benefits[1],
                                                                                      am=skill_benefits[0]))
        elif benefit.startswith("Blade"):
            if not automatic:
                print(BLADE_CBT_CASC)
                blade = input("Choose a type of blade to receive.\n")
                while blade not in BLADE_CBT_CASC:
                    blade = input("Choose a type of blade to receive.\n")
            else:
                blade_choice = roll_die(len(BLADE_CBT_CASC))
                blade = BLADE_CBT_CASC[blade_choice - 1]
            benefits.append(blade)
            history.append("Received a {blade} as a muster-out benefit.".format(blade=blade))
        elif benefit.startswith("Gun"):
            if not automatic:
                print(GUN_CBT_CASC)
                gun = input("Choose a type of gun to receive.\n")
                while gun not in GUN_CBT_CASC:
                    gun = input("Choose a type of gun to receive.\n")
            else:
                gun_choice = roll_die(len(GUN_CBT_CASC))
                gun = GUN_CBT_CASC[gun_choice - 1]
            benefits.append(gun)
            history.append("Received a {gun} as a muster-out benefit.".format(gun=gun))
        else:
            if benefit == "Travellers' Aid Society":
                if benefit not in benefits:
                    benefits.append(benefit)
                    history.append("Received a membership of the {ben} as a muster-out benefit.".format(ben=benefit))
            elif benefit not in ["High Passage", "Middle Passage", "Low Passage"]:
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
