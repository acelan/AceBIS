#!/usr/bin/python3

import json
import os
import collections

bis_list = {}
slots = ["Back", "Chest", "Feet", "Finger", "Hands", "Head", "Legs", "Neck", "Off Hand", "One-Hand", "Ranged", "Relic", "Shoulder", "Trinket", "Two-Hand", "Waist", "Wrist", "Held In Off-hand", "Main Hand", "Thrown"]
itemtypes = ["Back", "Chest", "Boots", "Finger", "Hands", "Helm", "Pants", "Neck", "Shoulder", "Trinket", "TwoHand", "Waist", "Bracers", "OffHand", "MainHand", "Ranged"]

classes = ["Warrior", "Rogue", "Priest", "Hunter", "Druid", "Paladin", "Mage", "Warlock", "Shaman", "Death Knight"]

# items are not available to players
blacklist = [
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
    33350,
    34139,
    38468,
    39263,
    40309,
    40310,
    40311,
    40312,
    40313,
    40314,
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
    45350,
    45499,
    45939,
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
    46308,
    46309,
    46844,
    47058,
    47506,
    47513,
    47521,
    47523,
    47542,
    47543,
    47544,
    48422,
    48697,
    48699,
    48711,
    48714,
    48725,
    48726,
    48727,
    48728,
    48729,
    48730,
    48731,
    48732,
    48733,
    48734,
    48746,
    48747,
    48748,
    48749,
    48750,
    48751,
    48752,
    48753,
    48754,
    48755,
    48756,
    48757,
    48758,
    48759,
    48760,
    48761,
    48762,
    48763,
    48764,
    49024,
    49292,
    49293,
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
    51395,
    51450,
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
    56522,
    60588,
    60597,
    65743,
    70022,
    78534,
    # 57682 ~ 57754
    # 58504 ~ 58778
    # 61635 ~ 61919
    # 69255 ~ 69263
    # 51516 ~ 51529
    # 51440 ~ 51448
]

rephase = {
    # 45340: '2',
}

# to better score trinket
rescore = {
    "dk_blood": {
        62471: 10000,
        62466: 9999,
        65048: 9998,
        65109: 9997,
        58483: 9996,
        56347: 9995,
        52352: 9994
    },
    "dk_frost": {
        65072: 10000,
        68712: 9999,
        65118: 9998,
        56393: 9997,
        58180: 9996,
        56100: 9995,
        56345: 9994
    },
    "dk_unholy": {
        65072: 10000,
        56393: 9999,
        58180: 9998,
        65118: 9997,
        68712: 9996,
        56100: 9995,
        56345: 9994
    },
    "druid_balance": {
        62047: 10000,
        65053: 9999,
        65110: 9998,
        65105: 9997,
        56400: 9996,
        56320: 9995,
        56462: 9994,
        64645: 9993,
        68710: 9992,
        56339: 9991,
        56407: 9990
    },
    "druid_feral": {
        65140: 10000,
        65026: 9999,
        56328: 9998,
        59520: 9997,
        58181: 9996,
        62468: 9995,
        56394: 9994
    },
    "druid_guardian": {
        65048: 10000,
        65109: 9999,
        62471: 9998,
        56347: 9997,
        62468: 9996
    },
    "druid_restoration": {
        59500: 10000,
        64645: 9999,
        62050: 9998,
        60233: 9997,
        68777: 9996,
        58184: 9995,
        62467: 9994,
        56351: 9993,
        65124: 9992,
        62044: 9991,
        65804: 9990
    },
    "hunter_beastmastery": {
        65140: 10000,
        65026: 9999,
        56394: 9998,
        56328: 9997,
        62051: 9996,
        56440: 9995
    },
    "hunter_marksmanship": {
        65140: 10000,
        65026: 9999,
        56394: 9998,
        56328: 9997,
        62051: 9996,
        56440: 9995,
        62468: 9994,
        62463: 9993
    },
    "hunter_survival": {
        65140: 10000,
        65026: 9999,
        56394: 9998,
        56328: 9997,
        62051: 9996,
        56440: 9995,
        62468: 9994,
        62463: 9993
    },
    "mage_arcane": {
        65053: 10000,
        65105: 9999,
        58183: 9998,
        62465: 9997,
        62047: 9996,
        62470: 9995,
        62021: 9994,
        56320: 9993,
        56339: 9992,
        56407: 9991
    },
    "mage_fire": {
        65105: 10000,
        62047: 9999,
        65053: 9998,
        62465: 9997,
        58183: 9996,
        56400: 9995,
        62021: 9994,
        62470: 9993,
        56320: 9992,
        56462: 9991,
        56407: 9990,
        56339: 9989
    },
    "mage_frost": {
        62047: 10000,
        65053: 9999,
        62021: 9998,
        58183: 9997,
        62465: 9996,
        62470: 9995,
        56320: 9994,
        56407: 9993,
        56462: 9992,
        56339: 9991
    },
    "paladin_holy": {
        60233: 10000,
        65124: 9999,
        62050: 9998,
        62044: 9997,
        64645: 9996,
        59500: 9995,
        68777: 9994,
        58184: 9993,
        56351: 9992,
        56320: 9991,
        62467: 9990
    },
    "paladin_protection": {
        58483: 10000,
        62466: 9999,
        62471: 9998,
        65048: 9997,
        65109: 9996,
        59332: 9995,
        59515: 9994,
        62464: 9993,
        62469: 9992,
        52352: 9991,
        56347: 9990
    },
    "paladin_retribution": {
        68712: 10000,
        56393: 9999,
        65072: 9998,
        65118: 9997,
        58180: 9996,
        59461: 9995,
        59224: 9994,
        52351: 9993,
        56285: 9992,
        56345: 9991
    },
    "priest_discipline": {
        65124: 10000,
        60233: 9999,
        62050: 9998,
        65029: 9997,
        65105: 9996,
        59500: 9995,
        64645: 9994,
        68777: 9993,
        59519: 9992,
        58184: 9991,
        59354: 9990,
        56320: 9989,
        56351: 9988,
        52354: 9987,
        56414: 9986,
        56462: 9985,
        58183: 9984,
        56339: 9983,
        56400: 9982,
        56290: 9981,
        65804: 9980,
        63839: 9979,
        55787: 9978
    },
    "priest_holy": {
        65124: 10000,
        60233: 9999,
        65029: 9998,
        62050: 9997,
        65105: 9996,
        59500: 9995,
        59519: 9994,
        64645: 9993,
        68777: 9992,
        58184: 9991,
        59354: 9990,
        56351: 9989,
        56320: 9988,
        52354: 9987,
        56462: 9986,
        56414: 9985,
        58183: 9984,
        56339: 9983,
        56400: 9982,
        56290: 9981,
        65804: 9980,
        63839: 9979,
        55787: 9978
    },
    "priest_shadow": {
        62047: 10000,
        65053: 9999,
        56400: 9998,
        65105: 9997,
        58183: 9996,
        59326: 9995,
        52353: 9994,
        59519: 9993,
        68777: 9992,
        56320: 9991,
        62465: 9990,
        62470: 9989,
        56290: 9988,
        65110: 9987,
        59514: 9986,
        64645: 9985,
        56407: 9984,
        56462: 9983,
        56339: 9982,
        55889: 9981,
        65804: 9980,
        63839: 9979,
        55787: 9978
    },
    "rogue_assassination": {
        58181: 10000,
        65026: 9999,
        68709: 9998,
        56328: 9997,
        56394: 9996,
        59441: 9995,
        59520: 9994,
        56427: 9993,
        65140: 9992,
        68776: 9991,
        59473: 9990,
        56440: 9989,
        56295: 9988,
        52199: 9987
    },
    "rogue_combat": {
        58181: 10000,
        65026: 9999,
        59441: 9998,
        65140: 9997,
        56427: 9996,
        56394: 9995,
        56328: 9994,
        59520: 9993,
        59473: 9992,
        68776: 9991,
        68709: 9990,
        56440: 9989,
        56295: 9988,
        52199: 9987
    },
    "rogue_subtlety": {
        58181: 10000,
        65140: 9999,
        65026: 9998,
        59441: 9997,
        68709: 9996,
        56427: 9995,
        56328: 9994,
        59520: 9993,
        59473: 9992,
        56394: 9991,
        68776: 9990,
        56440: 9989,
        56295: 9988,
        52199: 9987
    },
    "shaman_elemental": {
        62047: 10000,
        65053: 9999,
        65110: 9998,
        65105: 9997,
        58183: 9996,
        56320: 9995,
        56462: 9994,
        68777: 9993,
        68710: 9992,
        56339: 9991,
        56407: 9990,
        64645: 9989,
        65804: 9988
    },
    "shaman_enhancement": {
        65140: 10000,
        58181: 9999,
        65026: 9998,
        59520: 9997,
        56427: 9996,
        56394: 9995,
        62463: 9994,
        56440: 9993,
        56328: 9992,
        62051: 9991
    },
    "shaman_restoration": {
        60233: 10000,
        64645: 9999,
        65124: 9998,
        62050: 9997,
        62044: 9996,
        68777: 9995,
        58184: 9994,
        62467: 9993,
        56351: 9992,
        65804: 9991
    },
    "warlock_affliction": {
        62047: 10000,
        65053: 9999,
        59326: 9998,
        65105: 9997,
        59519: 9996,
        62465: 9995,
        58183: 9994,
        56320: 9993,
        56407: 9992,
        56462: 9991,
        56339: 9990,
        52353: 9989
    },
    "warlock_demonology": {
        62047: 10000,
        65053: 9999,
        58183: 9998,
        59326: 9997,
        65105: 9996,
        59519: 9995,
        62465: 9994,
        56320: 9993,
        56407: 9992,
        56339: 9991,
        56462: 9990,
        52353: 9989,
        65804: 9988
    },
    "warlock_destruction": {
        62047: 10000,
        65053: 9999,
        59326: 9998,
        65105: 9997,
        59519: 9996,
        62465: 9995,
        58183: 9994,
        56320: 9993,
        56407: 9992,
        56462: 9991,
        56339: 9990,
        52353: 9989
    },
    "warrior_arms": {
        60572: 10000,
        59461: 9999,
        65072: 9998,
        65118: 9997,
        58180: 9996,
        68712: 9995,
        56393: 9994,
        62049: 9993,
        56100: 9992,
        56345: 9991
    },
    "warrior_fury": {
        60572: 10000,
        59461: 9999,
        65072: 9998,
        65118: 9997,
        58180: 9996,
        68712: 9995,
        56393: 9994
    },
    "warrior_protection": {
        65048: 10000,
        65109: 9999,
        68713: 9998,
        58182: 9997,
        59332: 9996,
        59515: 9995,
        56347: 9994,
        62471: 9993,
        58483: 9992,
        52352: 9991,
        50364: 9990,
        56280: 9989,
        56449: 9988,
        62048: 9987,
        56370: 9986
    }
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

sides = {
    0: "Neutral",
    1: "Ally",
    2: "Horde",
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
    -6: "Back",                     # id = 47042
    -5: "OffHand",                  # id = 47053
    -4: "Trinket",                  # id = 47041
    -3: "Neck",                     # id = 47043
    -2: "Finger",                   # id = 47054
    0: 'Miscellaneous',             # id = 48945, no material
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
    11: "Relic",                    # 55248 @_@?
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
    #"Shield",                      #
    18: "Crossbow",                 # 'subclass': 18
    19: "Wand",                     # 'subclass': 19
    20: "Fishing Pole",             # 'subclass': 20
}

def nested_dict():
    return collections.defaultdict(nested_dict)

def read_itemdata():
    filename = "wowhead/itemdata.txt"
    if not os.path.exists(filename):
        return False

    with open(filename) as file:
        return json.loads(file.read())

def gen_header(phase, classes, spec):
    return "local bis_%s = AceBIS:RegisterBIS(\"%s\", \"%s\", \"%s\")\n" % (phase, classes, spec+classes, phase)

def write_file(classes, output):
    with open(f"AceBIS/Data/{classes}.lua", "w") as file:
        file.write(output)

def build_list():
    bis_list = nested_dict()
    items = read_itemdata()

    def is_blacklisted(itemid):
        return (itemid in blacklist or
                51440 <= itemid <= 51448 or
                51516 <= itemid <= 51529 or
                57682 <= itemid <= 57754 or
                58504 <= itemid <= 58778 or
                61635 <= itemid <= 61919 or
                69255 <= itemid <= 69263)

    def get_class_spec(i):
        cclass, spec = i.split("_")
        return "DK" if cclass == "dk" else cclass.capitalize(), spec.capitalize()

    def get_item_details(item):
        itemclass = item_class[int(item["class"]["@id"])]
        itemtype = inv_type[int(item["inventorySlot"]["@id"])]
        itemsubclass = ""

        if int(item["subclass"]) >= 0:
            if int(item["class"]["@id"]) in [0, 2]:
                itemsubclass = item2_subclass[int(item["subclass"])]
            elif int(item["class"]["@id"]) == 4:
                itemsubclass = item4_subclass[int(item["subclass"])]

        if int(item["subclass"]) == -5 and int(item["class"]["@id"]) == 4:
            itemclass, itemtype, itemsubclass = "Weapon", "OffHand", "OffHand"
        if int(item["subclass"]) == -6 and int(item["class"]["@id"]) == 4:
            itemclass, itemtype, itemsubclass = "Armor", "Back", "Cloth"

        if itemsubclass in ["Relic", "Thrown"]:
            itemtype = "Ranged"

        itemtype = {"Head": "Helm", "Wrist": "Bracers", "Legs": "Pants", "Feet": "Boots"}.get(itemtype, itemtype)

        return itemclass, itemtype, itemsubclass

    def is_valid_for_class_spec(cclass, spec, itemclass, itemtype, itemsubclass, item):
        if itemtype == "Ammo":
            return False

        if cclass == "DK":
            if "spldmg" in item:
                return False

            if itemclass == "Armor":
                if itemsubclass != "Plate" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemtype == "Ranged" and itemsubclass != "Relic":
                    return False
                if itemsubclass in ["Shield", "Staff", "Fist", "Dagger"]:
                    return False
        elif cclass == "Druid":
            if "spldmg" in item and spec == "Feral":
                return False

            if itemclass == "Armor":
                if itemsubclass != "Leather" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemtype == "Ranged" and itemsubclass != "Relic":
                    return False
                if itemsubclass == "Shield":
                    return False
                if itemsubclass in ["Axe", "Sword"]:
                    return False
                if itemtype == "TwoHand" and itemsubclass in ["Axe", "Sword"]:
                    return False
                if itemtype == "OffHand":
                    if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                        return False
        elif cclass == "Hunter":
            if itemclass == "Armor":
                if itemsubclass != "Mail" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Shield":
                    return False
                if itemsubclass  == "Mace":
                    return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Wand", "Thrown"]:
                        return False
        elif cclass == "Mage":
            if "mleatkpwr" in item or "agi" in item or "str" in item:
                return False

            if itemclass == "Armor":
                if itemsubclass != "Cloth" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Shield":
                    return False
                if itemtype == "TwoHand" and itemsubclass in ["Axe", "Sword", "Mace", "Polearm"]:
                    return False
                if itemsubclass in ["Axe", "Mace", "Fist"]: # for MainHand and OneHand
                    return False
                if itemtype == "OffHand":
                    if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                        return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown"]:
                        return False
        elif cclass == "Paladin":
            if itemclass == "Armor":
                if itemsubclass != "Plate" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if spec == "Protection" and "dodgertng" not in item and "parryrtng" not in item and "blockrtng" not in item:
                    if itemtype not in ["Amulet", "Trinket", "Ranged", "OffHand"]:
                        return False
            elif itemclass == "Weapon":
                if itemtype == "Ranged" and itemsubclass != "Relic":
                    return False
        elif cclass == "Priest":
            if "mleatkpwr" in item or "agi" in item or "str" in item:
                return False

            if itemclass == "Armor":
                if itemsubclass != "Cloth" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Shield":
                    return False
                if itemsubclass in ["Axe", "Sword", "Fist"]: # for MainHand and OneHand
                    return False
                if itemtype == "TwoHand" and itemsubclass in ["Axe", "Sword", "Mace", "Polearm"]:
                    return False
                if itemtype == "OffHand":
                    if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                        return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown"]:
                        return False
        elif cclass == "Rogue":
            if "spldmg" in item:
                return False

            if itemclass == "Armor":
                if itemsubclass != "Leather" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Shield":
                    return False
                if itemtype == "TwoHand":
                    return False
                if spec == "Assassination" and itemtype in ["MainHand", "OneHand", "OffHand"] and itemsubclass != "Dagger":
                    return False
                if spec == "Combat" and itemtype in ["MainHand", "OneHand", "OffHand"] and itemsubclass == "Dagger":
                    return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Wand"]:
                        return False
        elif cclass == "Shaman":
            if "spldmg" not in item and itemtype != "Ranged" and spec == "Restoration":
                return False

            if itemclass == "Armor":
                if itemsubclass != "Mail" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "Ranged", "OffHand"]:
                    return False
                if itemtype == "Ranged" and itemsubclass != "Relic":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Sword":
                    return False
                if itemtype == "TwoHand" and itemsubclass in ["Axe", "Sword"]:
                    return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown", "Wand"]:
                        return False
        elif cclass == "Warlock":
            if "mleatkpwr" in item or "agi" in item or "str" in item:
                return False

            if itemclass == "Armor":
                if itemsubclass != "Cloth" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
                if itemtype == "OffHand" and itemsubclass == "Shield":
                    return False
            elif itemclass == "Weapon":
                if itemsubclass == "Shield":
                    return False
                if itemsubclass in ["Axe", "Mace", "Fist"]: # for MainHand and OneHand
                    return False
                if itemtype == "TwoHand" and itemsubclass in ["Axe", "Sword", "Mace", "Polearm"]:
                    return False
                if itemtype == "OffHand":
                    if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                        return False
                if itemtype == "Ranged":
                    if itemsubclass in ["Gun", "Bow", "Crossbow", "Thrown"]:
                        return False
        elif cclass == "Warrior":
            if "spldmg" in item:
                return False

            if spec == "Protection" and "dodgertng" not in item and "parryrtng" not in item and "blockrtng" not in item:
                if itemtype not in ["Amulet", "Trinket", "Ranged", "OffHand"]:
                    return False
            if itemclass == "Armor":
                if itemsubclass != "Plate" and itemtype not in ["Back", "Finger", "Neck", "Trinket", "Ranged", "OffHand"]:
                    return False
                if itemsubclass == "Relic":
                    return False
            elif itemclass == "Weapon":
                if itemtype == "Ranged":
                    if itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"]:
                        return False

        return True

    for item in items.values():
        itemid = item["id"]
        phase = rephase.get(itemid, item["phase"])

        if is_blacklisted(itemid):
            continue

        for i in {'dk_unholy', 'dk_blood', 'dk_frost', 'druid_balance', 'druid_feral', 'druid_restoration', 'druid_guardian', 'hunter_survival', 'hunter_beastmastery', 'hunter_marksmanship', 'mage_arcane', 'mage_fire', 'mage_frost', 'paladin_holy', 'paladin_protection', 'paladin_retribution', 'priest_discipline', 'priest_shadow', 'priest_holy', 'rogue_assassination', 'rogue_combat', 'rogue_subtlety', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_affliction', 'warlock_demonology', 'warlock_destruction', 'warrior_arms', 'warrior_fury', 'warrior_protection'}:
            score = item[i]
            cclass, spec = get_class_spec(i)

            if "reqclass" in item and not (int([k for k, v in classs.items() if v == cclass][0]) & int(item["reqclass"])):
                continue

            side = sides[int(item["side"])] if "side" in item else "Neutral"

            class_spec = f"{cclass}_{spec}".lower()
            if class_spec in rescore and itemid in rescore[class_spec]:
                score = rescore[class_spec][itemid]

            try:
                itemclass, itemtype, itemsubclass = get_item_details(item)
            except Exception as err:
                print(f"Error processing item {itemid}: {err}")
                continue

            if not is_valid_for_class_spec(cclass, spec, itemclass, itemtype, itemsubclass, item):
                continue

            if score == 0:
                continue

            item_tmp = {
                "id": itemid, "phase": phase, "class": cclass, "spec": spec,
                "slot": itemtype, "type": itemtype, "itemclass": itemclass,
                "subclass": itemsubclass, "score": score, "side": side
            }


            if cclass == "Warrior" and spec == "Fury":
                if itemtype == "TwoHand":
                    itemtype = "OneHand"
                elif itemtype in ["MainHand", "OneHand"]:
                    continue

            bis_list[cclass][spec][phase][itemtype][itemid] = item_tmp

    return bis_list

bis_list = build_list()

for cclass in classs.values():
    for spec in bis_list[cclass].keys():
        print("%s - %s" % (cclass, spec))
        output = ""
        for phase in ["0", "1", "2"]:   # select items from P0 to P5
            p = "P" + phase
            output += gen_header(p, cclass, spec)
            #print("%s %s" % (spec, cclass))
            for s in itemtypes:
                items = bis_list[cclass][spec][phase][s]
                # OneHand weapon could be MainHand or OffHand weapon for "Warrior", "Rogue", "DK", "Hunter", "Shaman(Enh)"
                if cclass in ["Warrior", "Rogue", "DK", "Hunter", "Shaman"]:
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                    if s == "OffHand":
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                        else:
                            items = {**items, **bis_list[cclass][spec][phase]["OneHand"]}
                    if s == "OneHand":
                        # No MainHand weapon for this class + spec, then OneHand would be MainHand
                        if "MainHand" not in bis_list[cclass][spec][phase]:
                            s = "MainHand"
                        elif "OffHand" not in bis_list[cclass][spec][phase]:
                            s = "OffHand"
                        else:
                            continue

                if phase == "1" or phase == "2" or phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["0"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["0"]["OneHand"]}
                    if s == "OffHand":
                        if cclass in ["Warrior", "Rogue", "DK", "Hunter"]:
                            items = {**items, **bis_list[cclass][spec]["0"]["OneHand"]}
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec]["0"]["OneHand"]}
                if phase == "2" or phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["1"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["1"]["OneHand"]}
                    if s == "OffHand":
                        if cclass in ["Warrior", "Rogue", "DK", "Hunter"]:
                            items = {**items, **bis_list[cclass][spec]["1"]["OneHand"]}
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec]["1"]["OneHand"]}
                if phase == "3" or phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["2"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["2"]["OneHand"]}
                    if s == "OffHand":
                        if cclass in ["Warrior", "Rogue", "DK", "Hunter"]:
                            items = {**items, **bis_list[cclass][spec]["2"]["OneHand"]}
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec]["2"]["OneHand"]}
                if phase == "4" or phase == "5":
                    items = {**items, **bis_list[cclass][spec]["3"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["3"]["OneHand"]}
                    if s == "OffHand":
                        if cclass in ["Warrior", "Rogue", "DK", "Hunter"]:
                            items = {**items, **bis_list[cclass][spec]["3"]["OneHand"]}
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec]["3"]["OneHand"]}
                if phase == "5":
                    items = {**items, **bis_list[cclass][spec]["4"][s]}
                    if s == "MainHand":
                        items = {**items, **bis_list[cclass][spec]["4"]["OneHand"]}
                    if s == "OffHand":
                        if cclass in ["Warrior", "Rogue", "DK", "Hunter"]:
                            items = {**items, **bis_list[cclass][spec]["4"]["OneHand"]}
                        if cclass == "Shaman" and spec == "Enhancement":
                            items = {**items, **bis_list[cclass][spec]["4"]["OneHand"]}

                sorted_keys = sorted(items.keys(), key=lambda x: (float(items[x]['score'])), reverse=True)
                index = 1
                for itemid in sorted_keys:
                    if cclass in ["Warrior", "Paladin"] and spec == "Protection":
                        item = items[itemid]
                        if s == "OffHand" and item["subclass"] != "Shield":
                            continue
                    if cclass == "Warrior" and spec == "Arms":
                        item = items[itemid]
                        if s == "OffHand" and item["subclass"] == "Shield":
                            continue

                    # print("%s %s %s %s %s %s" % (cclass, spec, phase, s, itemid, bis_list[cclass][spec][phase][s][itemid]["type"]))
                    #output += "AceBIS:BISitem(bis_%s, \"%s\", \"%s\", \"%s\", \"%s\")\n" % (p, index, itemid, p, bis_list[cclass][spec][phase][s][itemid]["type"])
                    output += "AceBIS:BISitem(bis_%s, \"%s\", \"%s\", \"%s\", \"%s\")\n" % (p, index, itemid, p, s)
                    #if cclass == "Warrior" and spec == "Fury" and s == "OffHand":
                    #if itemid == 50646:
                    #    print("%s %s %s %s %s #%s" % (spec, cclass, itemid, items[itemid]["score"], p, index))
                    #print(output)
                    index += 1
                    if index > 30:
                        break
        write_file(spec + cclass, output)
