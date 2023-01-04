#!/usr/bin/python3

import json
import re
import os
import struct
import collections

bis_list = {}
slots = {"Back", "Chest", "Feet", "Finger", "Hands", "Head", "Legs", "Neck", "Off Hand", "One-Hand", "Ranged", "Relic", "Shoulder", "Trinket", "Two-Hand", "Waist", "Wrist", "Held In Off-hand", "Main Hand", "Thrown"}
classes = {"Warrior", "Rogue", "Priest", "Hunter", "Druid", "Paladin", "Mage", "Warlock", "Shaman", "Death Knight"}

# items are not available to players
blacklist = {
    29824,
    29827,
    29828,
    29829,
    29830,
    29831,
    29832,
    29833,
    29834,
    29835,
    29836,
    29865,
    29879,
    29881,
    29883,
    29888,
    29890,
    29891,
    29892,
    29893,
    29895,
    29897,
    29899,
    30176,
    34139,
    39263,
    40311,
    40479,
    40480,
    40481,
    40646,
    40647,
    40648,
    40649,
    40650,
    40651,
    40654,
    40655,
    40656,
    40657,
    40658,
    40659,
    40660,
    40661,
    40662,
    40663,
    40664,
    40665,
    42919,
    43648,
    43649,
    43727,
    43728,
    43729,
    43730,
    43731,
    43732,
    43733,
    43734,
    43735,
    43736,
    43737,
    43738,
    43739,
    43740,
    43741,
    43742,
    43743,
    43744,
    43745,
    43746,
    43747,
    43748,
    43749,
    43750,
    43751,
    43752,
    43753,
    43754,
    43755,
    43756,
    43757,
    43758,
    43759,
    43760,
    43761,
    43762,
    43763,
    43764,
    43765,
    43766,
    43767,
    43768,
    43769,
    43770,
    43771,
    43772,
    43773,
    43774,
    43775,
    43776,
    43777,
    43778,
    43779,
    43780,
    43781,
    43782,
    43783,
    43784,
    43785,
    43786,
    43787,
    43788,
    43789,
    43790,
    43791,
    43792,
    43793,
    43794,
    43795,
    43796,
    43797,
    43798,
    43799,
    43800,
    43801,
    43802,
    43803,
    43804,
    43805,
    43806,
    43807,
    43808,
    43809,
    43810,
    43811,
    43812,
    43813,
    43814,
    43815,
    43816,
    43817,
    43818,
    43819,
    43820,
    45172,
    45173,
    45174,
    45175,
    45499,
    46230,
    46231,
    46232,
    46233,
    46234,
    46235,
    46236,
    46237,
    46238,
    46239,
    46240,
    46241,
    46242,
    46243,
    46244,
    46245,
    46246,
    46247,
    46248,
    46249,
    46250,
    46251,
    46252,
    46253,
    46254,
    46255,
    46256,
    46257,
    46258,
    46259,
    46260,
    46261,
    46262,
    46263,
    46264,
    46265,
    46266,
    46267,
    46268,
    46269,
    46270,
    46271,
    46272,
    46273,
    46274,
    46275,
    46276,
    46277,
    46278,
    46279,
    46280,
    46281,
    46282,
    46283,
    46284,
    46285,
    46286,
    46287,
    46288,
    46289,
    46290,
    46291,
    46292,
    46293,
    46294,
    46295,
    46296,
    46297,
    46298,
    46299,
    46300,
    46301,
    46302,
    46303,
    46304,
    46305,
    46306,
    46307,
    46844,
    47542,
    47543,
    47544,
    49024,
    49357,
    49686,
    50132,
    50133,
    50251,
    50256,
    50329,
    50330,
    50331,
    50332,
    52567,
    52686,
    53055,
    53056,
    53096,
    53491,
    53492,
    53493,
    53494,
    53495,
    53496,
    53497,
    53498,
    53499,
    53500,
    53501,
    53502,
    53503,
    53504,
    53505,
    53506,
    53507,
    53508,
    53509,
    53889,
    53890,
    53924,
    54592,
    54848,
}

rephase = {
    45340: '2',
    45341: '2',
    45342: '2',
    45343: '2',
    45344: '2',
    45345: '2',
    45346: '2',
    45347: '2',
    45348: '2',
    45349: '2',
    45351: '2',
    45352: '2',
    45353: '2',
    45354: '2',
    45365: '2',
    45367: '2',
    45368: '2',
    45369: '2',
    45391: '2',
    45392: '2',
    45393: '2',
    45394: '2',
    45395: '2',
    45396: '2',
    45397: '2',
    45398: '2',
    45399: '2',
    45400: '2',
    45401: '2',
    45402: '2',
    45403: '2',
    45404: '3',
    45405: '3',
    45406: '2',
    45408: '2',
    45409: '2',
    45410: '2',
    45411: '2',
    45412: '2',
    45413: '2',
    45414: '2',
    45415: '2',
    45416: '2',
    45417: '2',
    45419: '2',
    45420: '2',
    45421: '2',
    45422: '2',
    45424: '2',
    45425: '2',
    45426: '2',
    45427: '2',
    45428: '2',
    46131: '2',
    46313: '2',
    49089: '4',
    49801: '4',
    49807: '4',
    49808: '4',
    49809: '4',
    49810: '4',
    49811: '4',
    49812: '4',
}

# to better score trinket
rescore = {
    # Mirror of Truth
    40684: {"AssassinationRogue": 1000, "SurvivalHunter": 999, "EnhancementShaman": 1000},
    # Fury of the Five Flights
    40431: {"AssassinationRogue": 998, "RetributionPaladin": 999},
    # Dying Curse
    40255: {"BalanceDruid": 1000, "ArcaneMage": 999, "ShadowPriest": 1000, "ElementalShaman": 999, "AfflictionWarlock": 999},
    # Illustration of the Dragon Soul
    40432: {"BalanceDruid": 999, "ShadowPriest": 999, "ElementalShaman": 1000, "AfflictionWarlock": 1000},
    # Ring of Invincibility
    40717: {"FeralDruid": 1000},
    # Darkmoon Card: Greatness(+str)
    42987: {"FeralDruid": 999, "RetributionPaladin": 1000, "FuryWarrior": 1000, "UnholyDK": 999},
    # Surge Needle Ring
    40474: {"SusvivalHunter": 1000},
    # Embrace of the Spider
    39229: {"ArcaneMage": 1000},
    # Figurine - Monarch Crab
    44063: {"ProtectionPaladin": 1000, "ProtectionWarrior": 999},
    # Essence of Gossamer
    37220: {"ProtectionPaladin": 999},
    # Darkmoon Card: Greatness(+agi)
    44253: {"AssassinationRogue": 999},
    # Meteorite Whetstone
    37390: {"EnhancementShaman": 999, "UnholyDK": 1000},
    # Grim Toll
    40256: {"FuryWarrior": 999},
    # Defender's Code
    40257: {"ProtectionWarrior": 1000},
}

classs = {
    1: "Warrior",
    2: "Paladin",
    4: "Hunter",
    8: "Rogue",
    16: "Priest",
    32: "DK",
    64: "Shaman",
    128: "Mage",
    256: "Warlock",
    1024: "Druid",
}

inv_type = {
    1: "Head",                      # {'@id': '1', '#text': 'Head'}
    2: "Neck",                      # {'@id': '2', '#text': 'Neck'}
    3: "Shoulder",                  # {'@id': '3', '#text': 'Shoulder'}
    4: "Shirt",                     # 'inventorySlot': {'@id': '4', '#text': 'Shirt'}
    5: "Chest",                     # 'inventorySlot': {'@id': '5', '#text': 'Chest'}
    6: "Waist",                     # {'@id': '6', '#text': 'Waist'}
    7: "Legs",                      # {'@id': '7', '#text': 'Legs'}
    8: "Feet",                      # 'inventorySlot': {'@id': '8', '#text': 'Feet'}
    9: "Wrist",                     # {'@id': '9', '#text': 'Wrist'}
    10: "Hands",                    # {'@id': '10', '#text': 'Hands'}
    11: "Finger",                   # {'@id': '11', '#text': 'Finger'}
    12: "Trinket",                  # {'@id': '12', '#text': 'Trinket'}
    13: "OneHand",                  # 'inventorySlot': {'@id': '13', '#text': 'One-Hand'}
    14: "OffHand",                  # {'@id': '14', '#text': 'Off Hand'}
    15: "Ranged",                   # 'inventorySlot': {'@id': '15', '#text': 'Ranged'}
    16: "Back",                     # {'@id': '16', '#text': 'Back'}
    17: "TwoHand",                  # 'inventorySlot': {'@id': '17', '#text': 'Two-Hand'}
    21: "MainHand",                 # 'inventorySlot': {'@id': '21', '#text': 'Main Hand'}
    22: "OffHand",                  # 'inventorySlot': {'@id': '22', '#text': 'Off Hand'}
    23: "OffHand",                  # "inventorySlot": {"@id": "23", "#text": "Held In Off-hand"}
    24: "Ammo",                     # {'@id': '24', '#text': 'Ammo'}
    25: "Thrown",                   # 'inventorySlot': {'@id': '25', '#text': 'Thrown'}
    28: "Relic",                    # {'@id': '28', '#text': 'Relic'}
}

item_class = {
    2: "Weapon",                    # 'class': {'@id': '2', '#text': 'Weapons'}
    4: "Armor",                     # 'class': {'@id': '4', '#text': 'Armor'}
    6: "Projectiles",               # 'class': {'@id': '6', '#text': 'Projectiles'}
    15: "Miscellaneous",            # 'class': {'@id': '15', '#text': 'Miscellaneous'}
}

item4_subclass = {
    1: "Cloth",                     # 'subclass': 1
    2: "Leather",
    3: "Mail",
    4: "Plate",
    #"Plate",
    #"Mail",
    #"Leather",
    6: "Shield",
    7: "Libram",                    # 35039
    8: "Idol",                      # 35019
    9: "Totem",                     # 35104
    10: "Sigil",                    # 35104
}

item2_subclass = {
    0: "Axe",                       # One Hand/Off Hand 'subclass': 0 / Two Hand 'subclass': 1
    1: "Axe",                       # One Hand/Off Hand 'subclass': 0 / Two Hand 'subclass': 1
    2: "Bow",                       # 'subclass': 2
    3: "Gun",                       # 'subclass': 3
    4: "Mace",                      # Main Hand/One Hand 'subclass': 4 / Two Hand 'subclass': 5
    5: "Mace",                      # Main Hand/One Hand 'subclass': 4 / Two Hand 'subclass': 5
    6: "Polearm",                   # 'subclass': 6
    7: "Sword",                     # Main Hand/One Hand/Off Hand 'subclass': 7 / Two Hand 'subclass': 8
    8: "Sword",                     # Main Hand/One Hand/Off Hand 'subclass': 7 / Two Hand 'subclass': 8
    9: "",                          # Relic
    10: "Staff",                    # 'subclass': 10
    13: "Fist",                     # 'subclass': 13
    14: "Staff",                    # item = 41755, The Fire Extinguisher
    15: "Dagger",                   # 'subclass': 15
    16: "Thrown",                   # 'subclass': 16
    #"Off-hand Frills",
    #"Shield",                   # 
    18: "Crossbow",                 # 'subclass': 18
    19: "Wand",                     # 'subclass': 19
    20: "Fishing Pole",             # 'subclass': 20
}

def nested_dict():
    return collections.defaultdict(nested_dict)

def write_slot(item):
    #print(item)
    filename = "wotlk-" + item["inventorySlot"]["#text"]
    with open(filename, 'a+') as file:
        file.write(json.dumps(item, ensure_ascii=False)) # use `json.loads` to do the reverse
        
def read_itemdata():
    filename = "wowhead/itemdata.txt"
    if not os.path.exists(filename):
        return False
    
    with open(filename) as file:
        userdata = file.read()
        #print("read data: %s" % userdata)
        return json.loads(userdata)

def gen_header(phase, classes, spec):
    return "local bis_%s = AceBIS:RegisterBIS(\"%s\", \"%s\", \"%s\")\n" % (phase, classes, spec+classes, phase)

def write_file(classes, output):
    file1 = open("AceBIS/Data/" + classes + ".lua", "w")
    file1.write(output)
    file1.close()

def build_list():
    bis_list = nested_dict()
    items = read_itemdata()
    for s in slots:
            for item in items.values():
                itemid = item["id"]
                phase = item["phase"]

                if itemid in rephase:
                    phase = rephase[itemid]
                # treat TBC items as P0 items, the highest ilv is 164
                if item["level"] < 170:
                    phase = '0'

                if itemid in blacklist:
                    continue
    
                item_tmp = {}
                #print("id = %s" % item["id"])
                #print("subclass = %s" % item["subclass"])
                #print("inventorySlot = %s" % item["inventorySlot"])
                for i in {'dk_unholy', 'druid_balance', 'druid_feral', 'hunter_survival', 'mage_arcane', 'paladin_protection', 'paladin_retribution', 'priest_discipline', 'priest_shadow', 'rogue_assassination', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_affliction', 'warrior_arms', 'warrior_fury', 'warrior_protection'}:
                    score = item[i]
                    #print("item = %s" % i)

                    cclass = i.split("_")[0].capitalize()
                    if cclass == "Dk":
                        cclass = "DK"

                    # continue if the item if for specific class
                    keys = [k for k, v in classs.items() if v == cclass]
                    if "reqclass" in item:
                        if not (int(keys[0]) & int(item["reqclass"])):
                            #print("item class = %s, class = %s" % (int(item["reqclass"]),int(keys[0])))
                            continue

                    # remove this after data retrived from wowhead again
                    if cclass == "Rogue":
                        spec = "Assassination"
                    elif cclass == "Hunter":
                        spec = "Survival"
                    else:
                        spec = i.split("_")[1].capitalize()

                    if itemid in rescore:
                        if spec + cclass in rescore[itemid]:
                            score = rescore[itemid][spec + cclass]

                    itemclass = ""
                    itemsubclass = ""
                    itemtype = ""
                    try:
                        itemclass = item_class[int(item["class"]["@id"])]

                        if int(item["subclass"]) > 0:
                            if int(item["class"]["@id"]) == 2:
                                itemsubclass = item2_subclass[int(item["subclass"])]
                            elif int(item["class"]["@id"]) == 4:
                                itemsubclass = item4_subclass[int(item["subclass"])]

                        itemtype = inv_type[int(item["inventorySlot"]["@id"])]
                    except:
                        print("id = %s" % item["id"])
                        print("class = %s" % item["class"])
                        print("subclass = %s" % item["subclass"])
                        print("inventorySlot = %s" % item["inventorySlot"])
                        exit(0)

                    if itemtype == "Ammo":
                        continue
                    if itemtype == "Thrown":
                        itemtype = "Ranged"
                    if itemtype == "Ranged" and cclass in ["Paladin", "DK", "Shaman", "Druid"]:
                        continue

                    if itemsubclass in ["Libram", "Sigil", "Totem", "Idol"]:
                        if cclass not in ["Paladin", "DK", "Shaman", "Druid"]:
                            continue
                        score = itemid
                        if cclass == "Paladin" and itemsubclass == "Libram":
                            itemtype = "Ranged"
                        elif cclass == "DK" and itemsubclass == "Sigil":
                            itemtype = "Ranged"
                        elif cclass == "Shaman" and itemsubclass == "Totem":
                            itemtype = "Ranged"
                        elif cclass == "Druid" and itemsubclass == "Idol":
                            itemtype = "Ranged"
                        else:
                            continue

                    if score == 0:
                        continue

                    if itemclass == "Armor":
                        if cclass in ["Mage", "Priest", "Warlock"]:
                            if itemsubclass in ["Leather", "Mail", "Plate"]:
                                continue
                        if cclass in ["Rogue", "Druid"]:
                            if itemsubclass in ["Mail", "Plate"]:
                                continue
                        if cclass in ["Hunter", "Shaman"]:
                            if itemsubclass in ["Plate"]:
                                continue
                        if cclass in ["Paladin", "Warrior", "DK"]:
                            if itemsubclass in []:
                                continue

                    if itemsubclass == "Shield" and cclass not in ["Warrior", "Paladin", "Shaman"]:
                        continue

                    if itemtype == "TwoHand":
                        if cclass in ["Rogue"]:
                            continue
                        if cclass in ["Mage", "Priest", "Warlock"]:
                            if itemsubclass in ["Axe", "Sword", "Mace", "Polearm"]:
                                continue
                        if cclass in ["Druid", "Shaman"]:
                            if itemsubclass in ["Sword", "Polearm"]:
                                continue
                        if cclass in ["Hunter"]:
                            if itemsubclass in ["Mace"]:
                                continue

                    if itemtype in ["MainHand", "OneHand", "OffHand"]:
                        if cclass in ["Rogue", "Druid"]:
                            if itemsubclass in ["Axe"]:
                                continue
                            if spec in ["Assassination"] and itemsubclass not in ["Dagger"]:
                                continue
                        if cclass in ["Mage", "Warlock"]:
                            if itemsubclass in ["Axe", "Mace", "Fist"]:
                                continue
                        if cclass in ["Priest"]:
                            if itemsubclass in ["Axe", "Sword", "Fist"]:
                                continue
                        if cclass in ["Shaman"]:
                            if itemsubclass in ["Sword"]:
                                continue
                        if cclass in ["Hunter"]:
                            if itemsubclass in ["Mace"]:
                                continue

                    #if itemid == 36871:
                    #    print("%s" % (item.keys()))
                    if "mleatkpwr" in item:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            continue
                    if "spldmg" not in item:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            if itemclass == "Armor" and itemtype not in ["Amulet", "Trinket"]:
                                continue
                    if "spldmg" in item:
                        if cclass in ["Warrior", "DK", "Rogue"]:
                            continue
                        if cclass == "Druid" and spec == "Feral":
                            continue
                    if cclass == "Shaman" and spec == "Restoration":
                        if "spldmg" not in item and itemtype not in "Ranged":
                            continue

                    if itemtype in ["OffHand"]:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                                continue

                    if itemtype in ["Ranged"]:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown"]:
                                continue
                        if cclass in ["Druid", "Shaman", "Paladin"]:
                            if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown", "Wand"]:
                                continue
                        if cclass in ["Warrior", "Rogue", "Hunter"]:
                            if itemsubclass in ["Wand"]:
                                continue

                    if spec == "Protection" and itemclass == "Armor":
                            if itemsubclass in ["Cloth", "Leather", "Mail"]:
                                continue

                    if spec == "Protection" and "defrtng" not in item and "dodgertng" not in item and "parryrtng" not in item and "blockrtng" not in item and "blockamount" not in item:
                        if itemclass == "Armor" and itemtype not in ["Amulet", "Trinket"]:
                            continue
                        if itemclass == "Weapon" and itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"]:
                            continue

                    # special setting for current assassination rogue weapon
                    if cclass == "Rogue" and spec == "Assassination":
                        if itemsubclass  == "Dagger":
                            score = score / float(item["speed"])    # weapon speed matter
                            if float(item["speed"]) > 1.4:          # slow weapon should equip in off hand
                                if itemtype == "OneHand":
                                    itemtype = "OffHand"
                            elif float(item["speed"]) == 1.3:       # for fastest weapon
                                score = score * 1.5
                            score = score + int(item["mledps"])

                    item_tmp = {"id": itemid, "phase": phase, "class": cclass, "spec": spec, "slot": s, "type": itemtype, "itemclass": itemclass, "subclass": itemsubclass, "score": score}
                    if itemtype == "Head":
                        itemtype = "Helm"
                    elif itemtype == "Wrist":
                        itemtype = "Bracers"
                    elif itemtype == "Legs":
                        itemtype = "Pants"
                    elif itemtype == "Feet":
                        itemtype = "Boots"
                    bis_list[cclass][spec][phase][itemtype][itemid] = item_tmp

                    # Fury Warrior can use TwoHand weapon as MainHand and OffHand weapon, so treat it as OneHand
                    if cclass == "Warrior" and spec == "Fury" and itemtype == "TwoHand":
                        bis_list[cclass][spec][phase]["OneHand"][itemid] = item_tmp

                    #if itemtype == "Trinket" and cclass == "Warlock" and spec == "Affliction":
                    #    print("after %s %s" % (itemid, score))
                    #if itemid in [39714, 37856, 40386] and cclass == "Rogue" and spec == "Assassination":
                    #    print("after %s %s" % (itemid, score))
                    #    print("%s %s %s %s %s %s" % (spec, cclass, itemid, score, phase, item["speed"]))

    #print(list(bis_list["Warrior"]["Fury"]["1"]))
    return bis_list

bis_list = build_list()

for cclass in classs.values():
    for spec in bis_list[cclass].keys():
        print("%s - %s" % (cclass, spec))
        output = ""
        for phase in {"0", "1"}:   # select items from P0 to P5
            p = "P" + phase
            output += gen_header(p, cclass, spec)
            #print("%s %s" % (spec, cclass))
            for s in list(bis_list[cclass][spec][phase]):
                items = bis_list[cclass][spec][phase][s]
                # OneHand weapon could be MainHand or OffHand weapon
                if s == "MainHand":
                    items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                if s == "OffHand":
                    items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                if s == "OneHand":
                    # No MainHand weapon for this class + spec, then OneHand would be MainHand
                    if "MainHand" not in bis_list[cclass][spec][phase]:
                        s = "MainHand"
                    else:
                        continue

                if phase == "1" or phase == "2" or phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["0"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["0"]["OneHand"]}
                    if s == "OffHand":
                        items = {**items, **bis_list[cclass][spec]["0"]["OneHand"]}
                if phase == "2" or phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["1"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["1"]["OneHand"]}
                    if s == "OffHand":
                        items = {**items, **bis_list[cclass][spec]["1"]["OneHand"]}
                if phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["2"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["2"]["OneHand"]}
                    if s == "OffHand":
                        items = {**items, **bis_list[cclass][spec]["2"]["OneHand"]}
                if phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["3"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["3"]["OneHand"]}
                    if s == "OffHand":
                        items = {**items, **bis_list[cclass][spec]["3"]["OneHand"]}
                if phase == "5":
                    items = {**items, **bis_list[cclass][spec]["4"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["4"]["OneHand"]}
                    if s == "OffHand":
                        items = {**items, **bis_list[cclass][spec]["4"]["OneHand"]}

                sorted_keys = sorted(items.keys(), key=lambda x: (float(items[x]['score'])), reverse=True)
                index = 1
                for itemid in sorted_keys:
                    # print("%s %s %s %s %s %s" % (cclass, spec, phase, s, itemid, bis_list[cclass][spec][phase][s][itemid]["type"]))
                    #output += "AceBIS:BISitem(bis_%s, \"%s\", \"%s\", \"%s\", \"%s\")\n" % (p, index, itemid, p, bis_list[cclass][spec][phase][s][itemid]["type"])
                    output += "AceBIS:BISitem(bis_%s, \"%s\", \"%s\", \"%s\", \"%s\")\n" % (p, index, itemid, p, s)
                    #if cclass == "Warrior" and spec == "Fury" and s == "OffHand":
                    #if itemid == 33475:
                    #    print("%s %s %s %s %s #%s" % (spec, cclass, itemid, items[itemid]["score"], p, index))
                    #print(output)
                    index += 1
                    if index > 15:
                        break
        write_file(spec + cclass, output)
