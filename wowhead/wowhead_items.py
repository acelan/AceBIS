#!/usr/bin/python3

import xmltodict
import argparse
import requests
import json
import re
import os
from classes.dk_unholy import dk_unholy
from classes.dk_blood import dk_blood
from classes.dk_frost import dk_frost
from classes.druid_balance import druid_balance
from classes.druid_feral import druid_feral
from classes.druid_guardian import druid_guardian
from classes.druid_restoration import druid_restoration
from classes.hunter_survival import hunter_survival
from classes.hunter_beastmastery import hunter_beastmastery
from classes.hunter_marksmanship import hunter_marksmanship
from classes.mage_arcane import mage_arcane
from classes.mage_fire import mage_fire
from classes.mage_frost import mage_frost
from classes.paladin_holy import paladin_holy
from classes.paladin_protection import paladin_protection
from classes.paladin_retribution import paladin_retribution
from classes.priest_discipline import priest_discipline
from classes.priest_shadow import priest_shadow
from classes.priest_holy import priest_holy
from classes.rogue_assassination import rogue_assassination
from classes.rogue_combat import rogue_combat
from classes.rogue_subtlety import rogue_subtlety
from classes.shaman_elemental import shaman_elemental
from classes.shaman_enhancement import shaman_enhancement
from classes.shaman_restoration import shaman_restoration
from classes.warlock_affliction import warlock_affliction
from classes.warlock_demonology import warlock_demonology
from classes.warlock_destruction import warlock_destruction
from classes.warrior_arms import warrior_arms
from classes.warrior_fury import warrior_fury
from classes.warrior_protection import warrior_protection


item_id = 0
first_id = 1000
final_id = 100000
#wowhead_wotlk="https://www.wowhead.com/wotlk/item=%s&xml"
wowhead_cata="https://www.wowhead.com/cata/item=%s&xml"

specs = {
    "dk_unholy": dk_unholy,
    "dk_blood": dk_blood,
    "dk_frost": dk_frost,
    "druid_balance": druid_balance,
    "druid_feral": druid_feral,
    "druid_guardian": druid_guardian,
    "druid_restoration": druid_restoration,
    "hunter_survival": hunter_survival,
    "hunter_beastmastery": hunter_beastmastery,
    "hunter_marksmanship": hunter_marksmanship,
    "mage_arcane": mage_arcane,
    "mage_fire": mage_fire,
    "mage_frost": mage_frost,
    "paladin_holy": paladin_holy,
    "paladin_protection": paladin_protection,
    "paladin_retribution": paladin_retribution,
    "priest_discipline": priest_discipline,
    "priest_shadow": priest_shadow,
    "priest_holy": priest_holy,
    "rogue_assassination": rogue_assassination,
    "rogue_combat": rogue_combat,
    "rogue_subtlety": rogue_subtlety,
    "shaman_elemental": shaman_elemental,
    "shaman_enhancement": shaman_enhancement,
    "shaman_restoration": shaman_restoration,
    "warlock_affliction": warlock_affliction,
    "warlock_demonology": warlock_demonology,
    "warlock_destruction": warlock_destruction,
    "warrior_arms": warrior_arms,
    "warrior_fury": warrior_fury,
    "warrior_protection": warrior_protection,
}

# socket{1,2,3} : 1 - meta, 2 - red, 3 - yellow, 4 - blue

def calculate_epv(spec, item, name):
    if not spec:
        return 0

    epv = 0
    for key in spec:
        if key in item:
            epv = epv + float(spec[key]) * item[key]
        # item needs to be activated, usually persists for 20s with 2min colddown
        if "use_" + key in item:
            #print("use_%s = %s, ep = %s" % (key, item["use_" + key], item["use_" + key] * 20 / 120))
            epv = epv + float(spec[key]) * item["use_" + key] * 20 / 120

    if "nsockets" in item:
        epv = epv + 100 * float(item["nsockets"])
    #for idx in [ "1", "2", "3", "4"]:
    #    if "socket" + idx in item:
    #        if item["socket" + idx] == 1:
    #            epv = epv + 40
    #        elif "socket" in spec:
    #            epv = epv + float(spec["socket"]) 

    return epv

def write_itemdata(data):
    with open('itemdata.txt', 'w') as file:
        file.write(json.dumps(data, ensure_ascii=False)) # use `json.loads` to do the reverse

def read_itemdata():
    if not os.path.exists("itemdata.txt"):
        return {}

    with open("itemdata.txt") as file:
        userdata = file.read()
        #print("read data: %s" % userdata)
        return json.loads(userdata)

def get_one_item(items, item_id, cached, update):
    item = {}

    item_id = str(item_id)

    # okay to get item from cache and item exists in cache
    if item_id in items.keys() and cached:
        print("get item_id %s from cache" % item_id)
        item = items[item_id]

    # want to update score, if the item doesn't exist then return
    if not item and update:
        return item

    # item doesn't exist in cache and not for update score
    if not item and not update:
        #url = wowhead_wotlk % item_id
        url = wowhead_cata % item_id
        try:
            r = requests.get(url)
            r.raise_for_status()
            root = xmltodict.parse(r.text)
        except (requests.RequestException, xmltodict.ParsingError) as err:
            print(f"Error retrieving item {item_id}: {err}")
            return

        if "item" not in root["wowhead"]:
            print("item_id %s not found on wowhead" % item_id)
            return

        print("retriving item_id %s from wowhead" % item_id)

        item = root["wowhead"]["item"]

        # do not store command or green items
        if int(item["quality"]["@id"]) <= 2:
            return

        # do not store low item level items
        if int(item["level"]) <= 230:
            return

        #value = item["name"]
        #print("name = %s" % value)
        #value = item["class"]["@id"]
        #print("class = %s" % value)
        #value = item["subclass"]["@id"]
        #print("subclass = %s" % value)
        value = item["inventorySlot"]["@id"]
        #print("inventorySlot = %s" % value)

        # can't equip
        if value == "0":
            return

        value = item["htmlTooltip"]
        m = re.search(r'Phase \d', value)
        if m is not None:
            value = m.group(0).split(' ')[1]
        else:
            value = "0"

        #print("phase = %s" % value)
        item["phase"] = value

        value = '{' + item["json"] + '}'
        #print("json = %s" % value)
        item_json = json.loads(value)
        for key in item_json.keys():
            item[key] = item_json[key]
        #print("json = %s" % item_json)
        # jsonEquip = "{\"appearances\":{\"0\":[55310,\"\"]},\"armor\":1821,\"avgbuyout\":27999997,\"critstrkrtng\":44,\"displayid\":55310,\"dura\":100,\"hitrtng\":60,\"nsockets\":2,\"reqlevel\":80,\"sellprice\":100067,\"slotbak\":1,\"socket1\":1,\"socket2\":4,\"socketbonus\":2787,\"str\":97}"
        value = '{' + item["jsonEquip"] + '}'
        item_equip_json = json.loads(value)
        #print("jsonEquip = %s" % item_equip_json)
        for key in item_equip_json.keys():
            #print("add key %s = %s" % (key, item_equip_json[key]))
            item[key] = item_equip_json[key]

        if "jsonUse" in item:
            # 'jsonUse': '"armorpenrtng":291'
            value = '{' + item["jsonUse"] + '}'
            print("jsonUse = %s" % value)
            item_use_json = json.loads(value)
            for key in item_use_json.keys():
                print("add key %s = %s" % (key, item_use_json[key]))
                item["use_" + key] = item_use_json[key]

    if len(item) == 0:
        return

    if int(item["level"]) > 379 and int(item["phase"]) <= 2:
        item["phase"] = '3'

    for spec in specs:
        item[spec] = calculate_epv(specs[spec], item, spec)

    items[item_id] = item

    #item = items[item_id]

    print(item)

def get_all_items(items, cached, update):
    for item_id in range(first_id, final_id):
        get_one_item(items, item_id, cached, update)

def main():
    parser = argparse.ArgumentParser(description='Get items from wowhead website.')
    parser.add_argument("-i", "--itemid", help="item id")
    parser.add_argument("-r", "--reload", help="retrive items from wowhead directly", action="store_true")
    parser.add_argument("-a", "--all", help="get all items", action="store_true")
    parser.add_argument("-u", "--update", help="update item score(won't access wowhead website)", action="store_true")
    args = parser.parse_args()

    items = read_itemdata() or {}

    if args.itemid:
        item_id = args.itemid
        get_one_item(items, item_id, not args.reload, args.update)

    if args.all:
        get_all_items(items, not args.reload, args.update)

    write_itemdata(items)

if __name__ == "__main__":
    main()
