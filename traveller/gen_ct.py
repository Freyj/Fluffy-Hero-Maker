from utils.dice_roller import sum_roll_dice, roll_die
from sty import fg
from traveller.consts_trav import *

import json

history = []
alive = True


def roll_stats():
    stats = []
    for i in range(6):
        stats.append(sum_roll_dice(6,2))
    return stats


def assign_stats(stats):
    dict_stats = {
        "Str": stats[0],
        "Dex": stats[1],
        "End": stats[2],
        "Int": stats[3],
        "Edu": stats[4],
        "Soc": stats[5]
    }
    return dict_stats


def get_char_for_stat(stat):
    if stat < 10:
        return str(stat)
    else:
        if stat == 10:
            return 'A'
        if stat == 11:
            return 'B'
        if stat == 12:
            return 'C'
        if stat == 13:
            return 'D'
        if stat == 14:
            return 'E'
        if stat == 15:
            return 'F'

    print("Error should never get there")


def roll_cash(ranks, service):
    table = []
    rank = ranks[service]
    dm = 0
    if service == "Navy":
        table = NAVY_CASH
    elif service == "Marines":
        table = MARINES_CASH
    elif service == "Army":
        table = ARMY_CASH
    if rank >= 5:
        dm += 1
    roll = roll_die(6) + dm - 1  # offset for array
    cash = table[roll]
    return cash


def roll_benefit(ranks, service):
    table = []
    dm = 0
    if service == "Navy":
        table = NAVY_BENEFITS
    elif service == "Marines":
        table = MARINES_BENEFITS
    elif service == "Army":
        table = ARMY_BENEFITS
    if ranks[service] > 4:
        dm += 1
    roll = roll_die(6) + dm - 1  # offset for array
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
    if rank == 0:
        return ""
    elif rank == 1:
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


def get_upp(dict_stats):
    upp = ""
    upp += get_char_for_stat(dict_stats["Str"])
    upp += get_char_for_stat(dict_stats["Dex"])
    upp += get_char_for_stat(dict_stats["End"])
    upp += get_char_for_stat(dict_stats["Int"])
    upp += get_char_for_stat(dict_stats["Edu"])
    upp += get_char_for_stat(dict_stats["Soc"])
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


def enlist_navy(stats):
    dm = 0
    if stats["Int"] > 7:
        dm += 1
    if stats["Edu"] > 8:
        dm += 2
    enlist_roll = sum_roll_dice(6, 2) + dm
    if enlist_roll > 7:
        return True
    else:
        return False


def enlist_marines(stats):
    dm = 0
    if stats["Int"] > 7:
        dm += 1
    if stats["Str"] > 7:
        dm += 2
    enlist_roll = sum_roll_dice(6, 2) + dm
    if enlist_roll > 8:
        return True
    else:
        return False


def enlist_army(stats):
    dm = 0
    if stats["Dex"] > 5:
        dm += 1
    if stats["End"] > 4:
        dm += 2
    enlist_roll = sum_roll_dice(6, 2) + dm
    if enlist_roll > 4:
        return True
    else:
        return False


def survive_navy(stats):
    dm = 0
    if stats["Int"] > 6:
        dm += 2
    survival_roll = sum_roll_dice(6, 2) + dm
    if survival_roll > 4:
        return True
    else:
        return False


def survive_marines(stats):
    dm = 0
    if stats["End"] > 7:
        dm += 2
    survival_roll = sum_roll_dice(6, 2) + dm
    if survival_roll > 5:
        return True
    else:
        return False


def survive_army(stats):
    dm = 0
    if stats["Edu"] > 6:
        dm += 2
    survival_roll = sum_roll_dice(6, 2) + dm
    if survival_roll > 4:
        return True
    else:
        return False


def try_navy_commission(stats):
    dm = 0
    if stats["Soc"] > 8:
        dm = 1
    commission_roll = sum_roll_dice(6, 2) + dm
    if commission_roll > 9:
        return True
    else:
        return False


def try_marines_commission(stats):
    dm = 0
    if stats["Edu"] > 6:
        dm = 1
    commission_roll = sum_roll_dice(6, 2) + dm
    if commission_roll > 8:
        return True
    else:
        return False


def try_army_commission(stats):
    dm = 0
    if stats["End"] > 6:
        dm = 1
    commission_roll = sum_roll_dice(6, 2) + dm
    if commission_roll > 4:
        return True
    else:
        return False


def try_navy_promotion(stats):
    dm = 0
    if stats["Edu"] > 7:
        dm += 1
    promotion_roll = sum_roll_dice(6, 2) + dm
    if promotion_roll > 7:
        return True
    else:
        return False


def try_marines_promotion(stats):
    dm = 0
    if stats["Soc"] > 7:
        dm += 1
    promotion_roll = sum_roll_dice(6, 2) + dm
    if promotion_roll > 8:
        return True
    else:
        return False


def try_army_promotion(stats):
    dm = 0
    if stats["Edu"] > 5:
        dm += 1
    promotion_roll = sum_roll_dice(6, 2) + dm
    if promotion_roll > 5:
        return True
    else:
        return False


def navy_reenlistment():
    """
        Determines if character can, has to or cannot reenlist
        :return: 1 : has to reenlist (nat 12)
                 0 : can reenlist
                -1 : cannot reenlist
    """
    reenlist_roll = sum_roll_dice(6, 2)
    if reenlist_roll == 12:
        return 1
    elif reenlist_roll > 5:
        return 0
    else:
        return -1


def marines_reenlistment():
    """
        Determines if character can, has to or cannot reenlist
        :return: 1 : has to reenlist (nat 12)
                 0 : can reenlist
                -1 : cannot reenlist
    """
    reenlist_roll = sum_roll_dice(6, 2)
    if reenlist_roll == 12:
        return 1
    elif reenlist_roll > 5:
        return 0
    else:
        return -1


def army_reenlistment():
    """
        Determines if character can, has to or cannot reenlist
        :return: 1 : has to reenlist (nat 12)
                 0 : can reenlist
                -1 : cannot reenlist
    """
    reenlist_roll = sum_roll_dice(6, 2)
    if reenlist_roll == 12:
        return 1
    elif reenlist_roll > 6:
        return 0
    else:
        return -1


def calc_muster_out_benefits(ranks, terms, service):
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
            x = input("Do you want cash or a benefit? You have {c} cash rolls max and {t} total rolls left. c for cash, b for benefit\n".format(
                c=cash_max,
                t=total_ben
            ))
            if x is "c":
                cash_max -= 1
                total_ben -= 1
                cash += roll_cash(ranks, service)
                print(cash)
            elif x is "b":
                total_ben -= 1
                benefits.append(roll_benefit(ranks, service))

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
        adv_skill_tab = ARMY__SKILLS_ADV
        serv_skill_tab = ARMY_SKILLS_SERVICE
        adv_edu_tab = ARMY_SKILLS_ADV_EDU
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
    survived = survive_navy(stats)
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        if ranks["Navy"] == 0:
            if not draft or term > 0:
                comm = try_navy_commission(stats)
                if comm:
                    history.append("Received a commission.")
                    ranks["Navy"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Navy"], "Navy")))
                    commissions["Navy"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Navy"]:
            promoted = try_navy_promotion(stats)
            if promoted:
                history.append("Received a promotion.")
                ranks["Navy"] += 1
                history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Navy"], "Navy")))
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
    survived = survive_marines(stats)
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        # when drafted cannot get commission at first term
        if ranks["Marines"] == 0:
            if not draft or term > 0:
                comm = try_marines_commission(stats)
                if comm:
                    history.append("Received a commission.")
                    ranks["Marines"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Marines"], "Marines")))
                    commissions["Marines"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Marines"]:
            promoted = try_marines_promotion(stats)
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
    survived = survive_army(stats)
    if survived:
        history.append("Survived the term.")
        age += 4
        skill_rolls = 0
        if ranks["Army"] == 0:
            if not draft or term > 0:
                comm = try_army_commission(stats)
                if comm:
                    history.append("Received a commission.")
                    ranks["Army"] = 1
                    history.append("\tBecame a {rank}".format(rank=get_rank(ranks["Army"], "Army")))
                    commissions["Army"] = True
                    skill_rolls += 1
                else:
                    history.append("Failed to get a commission.")
        if commissions["Army"]:
            promoted = try_army_promotion(stats)
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

        display_navy_skill_tables(stats["Edu"])
        add_skills(stats, skills, skill_rolls, "Army")
        return True

    else:
        print("BOOM, YA DEAD")
        history.append("Died during the term.")
        return False


def read_history():
    print("--------------------")
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
    print("--------------------")


def marines_career(term, stats, ranks, commissions, age, skills, draft):
    if draft:
        history.append("Drafted into the Marines.")
    else:
        history.append("Successfully enlisted in the Marines.")

    still_alive = True
    out_of_marines = False
    while still_alive and not out_of_marines:
        print("Term {i}".format(i=term))
        still_alive = calc_marines_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        if still_alive:
            if age >= 34:
                # ageing
                pass
            can_reenlist = marines_reenlistment()
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
    return term, still_alive


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
        if still_alive:
            if age >= 34:
                # ageing
                pass
            can_reenlist = navy_reenlistment()
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
    return term, still_alive


def army_career(term, stats, ranks, commissions, age, skills, draft):
    if not draft:
        history.append("Successfully enlisted in the Army.")
    else:
        history.append("Drafted in the Army.")
    still_alive = True
    out_of_army = False
    while still_alive and not out_of_army:
        still_alive = calc_army_term(stats, ranks, commissions, age, skills, draft, term)
        term += 1
        if still_alive:
            if age >= 34:
                # ageing
                pass
            can_reenlist = army_reenlistment()
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
    return term, still_alive


def char_details(stats, commissions, skills, ranks, age, cash, benefits):
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
    result_str += "\n" + str(age) + " years old"
    if not skills == {}:
        result_str += "\n" + json.dumps(skills)
    if cash > 0:
        result_str += "\n{c} Credits".format(c=cash)
    if len(benefits) > 0:
        result_str += "\n"
        for i in benefits:
            result_str += "{b}, ".format(b=i)
        result_str = result_str[:-2]
    return result_str


def treat_benefits(stats, benefits_list):
    for benefit in benefits_list:
        pass


if __name__ == "__main__":
    running = True
    while running:
        age = 18
        term = 0
        benefit_rolls = 0
        alive = True
        history = []
        enlisted = False
        stats = assign_stats(roll_stats())
        ranks = {
            "Navy": 0,
            "Marines": 0,
            "Army": 0,
            "Scouts": 0,
            "Merchants": 0,
            "Other": 0
        }
        commissions = {
            "Navy": False,
            "Marines": False,
            "Army": False,
            "Scouts": False,
            "Merchants": False,
            "Other": False
        }
        skills = {}
        choice = input("Choose service to try for: (Navy, Marines, Army, Scouts, Merchant, Other)\n")
        if choice == "Navy":
            got_in_navy = enlist_navy(stats)
            if got_in_navy:
                enlisted = True
                term, alive = navy_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Navy.")
        elif choice == "Marines":
            got_in_marines = enlist_marines(stats)
            if got_in_marines:
                enlisted = True
                term, alive = marines_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Marines.")
        elif choice == "Army":
            got_in_army = enlist_army(stats)
            if got_in_army:
                enlisted = True
                term, alive = army_career(term, stats, ranks, commissions, age, skills, False)
            else:
                history.append("Failed to enlist in the Army.")
        elif choice == "Q":
            running = False
        if not enlisted:
            print("You're being drafted")
            history.append("Submitted to the Draft")
            a = roll_die(3) - 1
            if a == 0:
                term, alive = marines_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Marines"
            elif a == 1:
                term, alive = navy_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Navy"
            elif a == 2:
                term, alive = army_career(term, stats, ranks, commissions, age, skills, True)
                choice = "Army"
        age = 18 + term * 4
        if alive:
            cash, benefits_list = calc_muster_out_benefits(ranks, term, choice)
            # Navstats, benefits = treat_benefits(stats, benefits_list)
        else:
            cash = 0
            benefits = []
        read_history()
        print(char_details(stats, commissions, skills, ranks, age, cash, benefits))
