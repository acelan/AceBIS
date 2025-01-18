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
    65005,
    65006,
    65008,
    65009,
    65010,
    65011,
    65012,
    65013,
    65014,
    65016,
    65097,
    65098,
    65099,
    65100,
    65101,
    65102,
    65103,
    65743,
    69184,
    69185,
    69198,
    69199,
    69200,
    70022,
    71388,
    71389,
    71390,
    71391,
    71392,
    71393,
    71394,
    71395,
    71396,
    71397,
    71398,
    71399,
    71400,
    71565,
    71566,
    71569,
    71570,
    71571,
    71572,
    71573,
    71574,
    71576,
    71578,
    71581,
    71582,
    71583,
    71584,
    71585,
    71586,
    71588,
    71589,
    71591,
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
        69109: 10000,
        68915: 9999,
        71617: 9998,
        65048: 9997,
        65109: 9996,
        62471: 9995,
        62466: 9994,
        70143: 9993,
        65072: 9992,
        69167: 9991,
        65118: 9990,
        69150: 9989,
        69113: 9988,
        68972: 9987,
        58483: 9986,
        56347: 9985,
        52352: 9984,
    },
    "dk_frost": {
        69113: 10000,
        68972: 9999,
        71617: 9998,
        65072: 9997,
        69167: 9996,
        65118: 9995,
        68712: 9994,
        56393: 9993,
        58180: 9992,
        56100: 9991,
        56345: 9990,
    },
    "dk_unholy": {
        69167: 10000,
        65072: 9999,
        56393: 9998,
        69113: 9997,
        68972: 9996,
        71617: 9995,
        65118: 9994,
        58180: 9993,
        68712: 9992,
        56100: 9991,
        56345: 9990,
    },
    "druid_balance": {
        69110: 10000,
        62047: 9999,
        69139: 9998,
        65105: 9997,
        65053: 9996,
        70142: 9995,
        65110: 9994,
        56400: 9993,
        56320: 9992,
        56462: 9991,
        64645: 9990,
        68710: 9989,
        56339: 9988,
        56407: 9987,
    },
    "druid_feral": {
        69150: 10000,
        69112: 9999,
        65140: 9998,
        65026: 9997,
        58181: 9996,
        69001: 9995,
        59520: 9994,
        56328: 9993,
        62468: 9992,
        56394: 9991,
    },
    "druid_guardian": {
        69109: 10000,
        65109: 9999,
        68915: 9998,
        65048: 9997,
        70143: 9996,
        69150: 9995,
        69112: 9994,
        65140: 9993,
        65026: 9992,
        58181: 9991,
        69001: 9990,
        62471: 9989,
        56347: 9988,
        62468: 9987,
    },
    "druid_restoration": {
        69111: 10000,
        68926: 9999,
        65124: 9998,
        69149: 9997,
        64645: 9996,
        62050: 9995,
        59500: 9994,
        68983: 9993,
        69000: 9992,
        60233: 9991,
        58184: 9990,
        68777: 9989,
        62467: 9988,
        56351: 9987,
        62044: 9986,
        65804: 9985,
    },
    "hunter_beastmastery": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        68927: 9997,
        69001: 9996,
        65026: 9995,
        65140: 9994,
        56394: 9993,
        56328: 9992,
        62051: 9991,
        56440: 9990,
    },
    "hunter_marksmanship": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        68927: 9997,
        69001: 9996,
        65026: 9995,
        65140: 9994,
        56394: 9993,
        56328: 9992,
        62051: 9991,
        56440: 9990,
        62468: 9989,
        62463: 9988,
    },
    "hunter_survival": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        68927: 9997,
        69001: 9996,
        65026: 9995,
        65140: 9994,
        56394: 9993,
        56328: 9992,
        62051: 9991,
        56440: 9990,
        62468: 9989,
        62463: 9988,
    },
    "mage_arcane": {
        65105: 10000,
        69110: 9999,
        60233: 9998,
        70142: 9997,
        62047: 9996,
        62021: 9995,
        68998: 9994,
        65053: 9993,
        62465: 9992,
        62470: 9991,
        58183: 9990,
        56320: 9989,
        56339: 9988,
        56407: 9987,
    },
    "mage_fire": {
        62047: 10000,
        62021: 9999,
        69110: 9998,
        65105: 9997,
        68998: 9996,
        65053: 9995,
        62465: 9994,
        62470: 9993,
        58183: 9992,
        56400: 9991,
        56320: 9990,
        56462: 9989,
        56407: 9988,
        56339: 9987,
    },
    "mage_frost": {
        62047: 10000,
        62021: 9999,
        69110: 9998,
        68998: 9997,
        65053: 9996,
        65105: 9995,
        62465: 9994,
        62470: 9993,
        58183: 9992,
        56320: 9991,
        56407: 9990,
        56462: 9989,
        56339: 9988,
    },
    "paladin_holy": {
        69111: 10000,
        65124: 9999,
        69149: 9998,
        68926: 9997,
        62050: 9996,
        62044: 9995,
        64645: 9994,
        69000: 9993,
        59500: 9992,
        68983: 9991,
        68777: 9990,
        52207: 9989,
        60233: 9988,
        58184: 9987,
        56351: 9986,
        56320: 9985,
        62467: 9984,
    },
    "paladin_protection": {
        69109: 10000,
        71617: 9999,
        69138: 9998,
        69002: 9997,
        68915: 9996,
        58483: 9995,
        52219: 9994,
        62466: 9993,
        62471: 9992,
        65048: 9991,
        65109: 9990,
        59332: 9989,
        59515: 9988,
        62464: 9987,
        62469: 9986,
        52352: 9985,
        56347: 9984,
    },
    "paladin_retribution": {
        69113: 10000,
        68972: 9999,
        71617: 9998,
        68712: 9997,
        69002: 9996,
        65072: 9995,
        59224: 9994,
        69167: 9993,
        56393: 9992,
        70141: 9991,
        65118: 9990,
        58180: 9989,
        59461: 9988,
        52351: 9987,
        56285: 9986,
        56345: 9985,
    },
    "priest_discipline": {
        69110: 10000,
        69139: 9999,
        69149: 9998,
        69111: 9997,
        68982: 9996,
        68983: 9995,
        68926: 9994,
        65124: 9993,
        65105: 9992,
        70142: 9991,
        62050: 9990,
        59500: 9989,
        64645: 9988,
        68777: 9987,
        52207: 9986,
        59519: 9985,
        60233: 9984,
        65029: 9983,
        58184: 9982,
        59354: 9981,
        56320: 9980,
        56351: 9979,
        52354: 9978,
        56414: 9977,
        56462: 9976,
        58183: 9975,
        56339: 9974,
        56400: 9973,
        56290: 9972,
        65804: 9971,
        63839: 9970,
        55787: 9969,
    },
    "priest_holy": {
        69149: 10000,
        69111: 9999,
        68983: 9998,
        68926: 9997,
        69110: 9996,
        69139: 9995,
        68982: 9994,
        65124: 9993,
        70142: 9992,
        62050: 9991,
        65105: 9990,
        59500: 9989,
        59519: 9988,
        64645: 9987,
        68777: 9986,
        52207: 9985,
        58184: 9984,
        60233: 9983,
        65029: 9982,
        59354: 9981,
        56351: 9980,
        56320: 9979,
        52354: 9978,
        56462: 9977,
        56414: 9976,
        58183: 9975,
        56339: 9974,
        56400: 9973,
        56290: 9972,
        65804: 9971,
        63839: 9970,
        55787: 9969,
    },
    "priest_shadow": {
        69110: 10000,
        62047: 9999,
        68925: 9998,
        69139: 9997,
        68982: 9996,
        68998: 9995,
        69000: 9994,
        65053: 9993,
        65105: 9992,
        70142: 9991,
        58183: 9990,
        59326: 9989,
        52353: 9988,
        59519: 9987,
        56400: 9986,
        68777: 9985,
        56320: 9984,
        62465: 9983,
        62470: 9982,
        56290: 9981,
        65110: 9980,
        59514: 9979,
        64645: 9978,
        56407: 9977,
        56462: 9976,
        56339: 9975,
        55889: 9974,
        65804: 9973,
        63839: 9972,
        55787: 9971,
    },
    "rogue_assassination": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        65026: 9997,
        68927: 9996,
        58181: 9995,
        68709: 9994,
        56328: 9993,
        56394: 9992,
        59441: 9991,
        59520: 9990,
        56427: 9989,
        65140: 9988,
        68776: 9987,
        59473: 9986,
        56440: 9985,
        56295: 9984,
        52199: 9983,
    },
    "rogue_combat": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        65026: 9997,
        68927: 9996,
        58181: 9995,
        59441: 9994,
        65140: 9993,
        56427: 9992,
        56394: 9991,
        56328: 9990,
        59520: 9989,
        59473: 9988,
        68776: 9987,
        68709: 9986,
        56440: 9985,
        56295: 9984,
        52199: 9983,
    },
    "rogue_subtlety": {
        69150: 10000,
        69112: 9999,
        68994: 9998,
        65026: 9997,
        68927: 9996,
        58181: 9995,
        65140: 9994,
        59441: 9993,
        68709: 9992,
        56427: 9991,
        56328: 9990,
        59520: 9989,
        59473: 9988,
        56394: 9987,
        68776: 9986,
        56440: 9985,
        56295: 9984,
        52199: 9983,
    },
    "shaman_elemental": {
        69110: 10000,
        62047: 9999,
        68925: 9998,
        69139: 9997,
        65053: 9996,
        65110: 9995,
        65105: 9994,
        70142: 9993,
        58183: 9992,
        56320: 9991,
        56462: 9990,
        68777: 9989,
        68710: 9988,
        56339: 9987,
        56407: 9986,
        64645: 9985,
        65804: 9984,
    },
    "shaman_enhancement": {
        69150: 10000,
        69001: 9999,
        69112: 9998,
        65140: 9997,
        58181: 9996,
        65026: 9995,
        59520: 9994,
        56427: 9993,
        56394: 9992,
        62463: 9991,
        56440: 9990,
        56328: 9989,
        62051: 9988,
    },
    "shaman_restoration": {
        69149: 10000,
        69111: 9999,
        60233: 9998,
        62050: 9997,
        62044: 9996,
        65124: 9995,
        64645: 9994,
        68777: 9993,
        52207: 9992,
        58184: 9991,
        62467: 9990,
        56351: 9989,
        65804: 9988,
    },
    "warlock_affliction": {
        69110: 10000,
        62047: 9999,
        69139: 9998,
        68925: 9997,
        68982: 9996,
        65053: 9995,
        68998: 9994,
        59326: 9993,
        65105: 9992,
        59519: 9991,
        62465: 9990,
        58183: 9989,
        56320: 9988,
        56407: 9987,
        56462: 9986,
        56339: 9985,
        52353: 9984,
    },
    "warlock_demonology": {
        70142: 10000,
        69110: 9999,
        62047: 9998,
        69139: 9997,
        68925: 9996,
        68982: 9995,
        65053: 9994,
        68998: 9993,
        58183: 9992,
        59326: 9991,
        65105: 9990,
        59519: 9989,
        62465: 9988,
        56320: 9987,
        56407: 9986,
        56339: 9985,
        56462: 9984,
        52353: 9983,
        65804: 9982,
    },
    "warlock_destruction": {
        69110: 10000,
        62047: 9999,
        69139: 9998,
        68925: 9997,
        68982: 9996,
        65053: 9995,
        68998: 9994,
        59326: 9993,
        65105: 9992,
        59519: 9991,
        62465: 9990,
        58183: 9989,
        56320: 9988,
        56407: 9987,
        56462: 9986,
        56339: 9985,
        52353: 9984,
    },
    "warrior_arms": {
        69167: 10000,
        69113: 9999,
        68972: 9998,
        71617: 9997,
        65072: 9996,
        59461: 9995,
        60572: 9994,
        65118: 9993,
        58180: 9992,
        68712: 9991,
        56393: 9990,
        62049: 9989,
        56100: 9988,
        56345: 9987,
    },
    "warrior_fury": {
        69167: 10000,
        69113: 9999,
        68972: 9998,
        71617: 9997,
        65072: 9996,
        59461: 9995,
        60572: 9994,
        65118: 9993,
        58180: 9992,
        68712: 9991,
        56393: 9990,
    },
    "warrior_protection": {
        69109: 10000,
        68915: 9999,
        71617: 9998,
        69138: 9997,
        68981: 9996,
        65048: 9995,
        65109: 9994,
        70143: 9993,
        68996: 9992,
        69002: 9991,
        62471: 9990,
        68713: 9989,
        58182: 9988,
        59332: 9987,
        59515: 9986,
        56347: 9985,
        58483: 9984,
        52352: 9983,
        50364: 9982,
        56280: 9981,
        56449: 9980,
        62048: 9979,
        56370: 9978,
    },
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
        for phase in ["0", "1", "2", "3"]:   # select items from P0 to P5
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
