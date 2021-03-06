#!/usr/bin/python

import csv
import re
import os
import struct
import collections
from urllib.parse import urlparse
import requests

bis_list = {}
slots = {"BACK", "CHEST", "FEET", "FINGER", "HANDS", "HEAD", "LEGS", "NECK", "OFFHAND", "ONEHAND", "RANGED", "RELIC", "SHOULDER", "TRINKET", "TWOHAND", "WAIST", "WRIST"}
classes = {"Warrior", "Rogue", "Priest", "Hunter", "Druid", "Paladin", "Mage", "Warlock", "Shaman"}

col_entry = 0           # item id
col_InventoryType = 1   # Back/Chest/Feet/Finger/...
col_itemclass = 2       # Armor/Weapon
col_subclass = 3        # Cloth/Totem
col_name = 4
col_class = 9           # specific for a certain class or classes
col_prot = 10           # score for Pretection Warrior spec.
col_arms = 11           # score for Arms Warrior spec.
col_fury = 12           # score for Fury Warrior spec.
col_rogue = 13          # score for Rogue(combat)
col_holy = 14           # score for Holy Priest
col_shad = 15           # score for Shadow Priest
col_bm = 16             # score for BeastMastery Hunter
col_sv = 17
col_tree = 18
col_owl = 19
col_cat = 20
col_bear = 21
col_arc = 22
col_fire = 23
col_affl = 24
col_dest = 25
col_tank = 26
col_ret = 27
col_heal = 28
col_ele = 29
col_enh = 30
col_res = 31
col_dod = 50            # dodge rating
col_par = 51            # parry rating
col_def = 52            # defense rating
col_sblock = 53         # block value
col_brating = 54        # block rating
col_location = 63
col_phase = 65

def nested_dict():
    return collections.defaultdict(nested_dict)

def gen_header(phase, build):
    classes = ""
    for i in build:
        if i.isupper() == True:
            classes = i
        else:
            classes += i
    return "local bis_%s = AceBIS:RegisterBIS(\"%s\", \"%s\", \"%s\")\n" % (phase, classes, build, phase)

def write_file(classes, output):
    file1 = open("AceBIS/Data/" + classes + ".lua", "w")
    file1.write(output)
    file1.close()

def build_list():
    bis_list = nested_dict()
    for s in slots:
        print("Parsing %s data" % s)
        root = "wowclassicbis"
        filename = s + '.csv'
    
        with open(os.path.join(root, filename), newline='') as csvfile:
            print("Reading %s..." % filename)
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                itemid = row[col_entry]
                phase = row[col_phase]
    
                item = {}
                for i in range(col_prot, col_res + 1):
                    score = row[i]
                    if score == "0":
                        continue

                    if i == col_prot:
                        cclass = "Warrior"
                        spec = "Protection"
                    if i == col_arms:
                        cclass = "Warrior"
                        spec = "Arms"
                    if i == col_fury:
                        cclass = "Warrior"
                        spec = "Fury"
                    if i == col_rogue:
                        cclass = "Rogue"
                        spec = "Combat"
                    if i == col_holy:
                        cclass = "Priest"
                        spec = "Holy"
                    if i == col_shad:
                        cclass = "Priest"
                        spec = "Shadow"
                    if i == col_bm:
                        cclass = "Hunter"
                        spec = "BeastMastery"
                    if i == col_sv:
                        cclass = "Hunter"
                        spec = "Survival"
                    if i == col_tree:
                        cclass = "Druid"
                        spec = "Restoration"
                    if i == col_owl:
                        cclass = "Druid"
                        spec = "Balance"
                    if i == col_cat:
                        cclass = "Druid"
                        spec = "Feral(DPS)"
                    if i == col_bear:
                        cclass = "Druid"
                        spec = "Feral(Tank)"
                    if i == col_arc:
                        cclass = "Mage"
                        spec = "Arcane"
                    if i == col_fire:
                        cclass = "Mage"
                        spec = "Fire"
                    if i == col_affl:
                        cclass = "Warlock"
                        spec = "Affliction"
                    if i == col_dest:
                        cclass = "Warlock"
                        spec = "Destruction"
                    if i == col_tank:
                        cclass = "Paladin"
                        spec = "Protection"
                    if i == col_ret:
                        cclass = "Paladin"
                        spec = "Retribution"
                    if i == col_heal:
                        cclass = "Paladin"
                        spec = "Holy"
                    if i == col_ele:
                        cclass = "Shaman"
                        spec = "Elemental"
                    if i == col_enh:
                        cclass = "Shaman"
                        spec = "Enhancement"
                    if i == col_res:
                        cclass = "Shaman"
                        spec = "Restoration"

                    # class specific gear
                    if row[col_class] != "NA" and row[col_class] != "Class" and row[col_class] != "10":
                        if cclass not in row[col_class]:
                            #print("%s not in %s" % (cclass, row[col_class]))
                            continue

                    itemclass = row[col_itemclass]
                    itemsubclass = row[col_subclass]
                    itemtype = row[col_InventoryType]
                    if itemtype == "Held In Off-Hand":
                        itemtype = "Off-Hand"

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
                        if cclass in ["Paladin", "Warrior"]:
                            if itemsubclass in []:
                                continue

                    if itemsubclass == "Shield" and cclass not in ["Warrior", "Paladin", "Shaman"]:
                        continue

                    if itemtype == "Two-Hand":
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

                    if itemtype in ["Main Hand", "One Hand"]:
                        if cclass == "Rogue" and itemsubclass == "Dagger":
                            continue
                    if itemtype in ["Main Hand", "One Hand", "Off Hand"]:
                        if cclass in ["Rogue", "Druid"]:
                            if itemsubclass in ["Axe"]:
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

                    if itemtype in ["Off Hand"]:
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
                            if itemsubclass in ["Leather", "Mail"]:
                                continue

                    if spec == "Protection" and row[col_dod] == "NULL" and row[col_par] == "NULL" and row[col_def] == "NULL" and row[col_sblock] == "NULL" and row[col_brating] == "NULL":
                        if itemclass == "Armor" and itemsubclass not in ["Amulet", "Trinket"]:
                            continue
                        if itemclass == "Weapon" and itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"]:
                            continue

                    item = {"id": itemid, "phase": phase, "class": cclass, "spec": spec, "slot": s, "type": itemtype, "itemclass": itemclass, "subclass": itemsubclass, "score": score, "location": row[col_location]}
                    if itemid == "28523" or itemid == "31286":
                        print(item)
                    bis_list[cclass][spec][phase][itemtype.replace(" ", "").replace("-", "")][itemid] = item

    return bis_list

bis_list = build_list()

for cclass in classes:
    print(cclass)
    for spec in bis_list[cclass].keys():
        print(spec)
        output = ""
        for phase in {"0", "1", "2", "3", "4", "5"}:   # select items from P0 to P5
            p = "P" + phase
            output += gen_header(p, spec + cclass)
            #print("%s %s" % (spec, cclass))
            mainhand_flag = False
            for s in list(bis_list[cclass][spec][phase]):
                #print(s)
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
                    if cclass == "Hunter" and s == "CHEST":
                        print("%s %s %s %s %s #%s" % (spec, cclass, itemid, items[itemid]["score"], p, index))
                    #print(output)
                    index += 1
                    if index > 15:
                        break
        write_file(spec + cclass, output)
