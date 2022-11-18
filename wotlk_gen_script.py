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
    43648,
    43649,
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
                
                if itemid == 49809:
                    phase = '4'
                if itemid == 45391:
                    phase = '2'
                if itemid == 45394:
                    phase = '2'

                if itemid in blacklist:
                    continue
                #if itemid in invalid:
                #    continue
    
                item_tmp = {}
                #print("id = %s" % item["id"])
                #print("subclass = %s" % item["subclass"])
                #print("inventorySlot = %s" % item["inventorySlot"])
                for i in {'dk_unholy', 'druid_balance', 'druid_feral', 'hunter_survival', 'mage_arcane', 'paladin_protection', 'paladin_retribution', 'priest_shadow', 'rogue_assassination', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_afflication', 'warrior_arm', 'warrior_fury', 'warrior_protection'}:
                    score = item[i]
                    if score == "0":
                        continue

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

                    if itemtype == "Relic" or itemtype == "Ammo":
                        continue
                    if itemtype == "Thrown":
                        itemtype = "Ranged"

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

                    if "mleatkpwr" in item:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            continue
                    if "spldmg" in item:
                        if cclass in ["Warrior", "DK", "Rogue"]:
                            continue
                        if cclass == "Druid" and spec == "Feral":
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
                        if itemclass == "Armor" and itemsubclass not in ["Amulet", "Trinket"]:
                            continue
                        if itemclass == "Weapon" and itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"]:
                            continue


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

                    #if itemid == 33475:
                    #    print("%s %s %s %s %s" % (spec, cclass, itemid, score, phase))

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
            mainhand_flag = False
            for s in list(bis_list[cclass][spec][phase]):
                items = bis_list[cclass][spec][phase][s]
                # OneHand weapon could be MainHand or OffHand weapon
                if s == "MainHand":
                    items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                    mainhand_flag = True
                if s == "OffHand":
                    items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                if s == "OneHand":
                    if mainhand_flag:
                        continue
                    s = "MainHand"

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
                    if items[itemid]["score"] == "0":
                        continue

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