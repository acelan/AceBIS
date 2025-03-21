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
        78003: 10000,
        77990: 9999,
        77211: 9998,
        77206: 9997,
        77983: 9996,
        77970: 9995,
        69109: 9994,
        68915: 9993,
        71617: 9992,
        74035: 9991,
        72900: 9990,
        65048: 9989,
        62471: 9988,
        62466: 9987,
        65109: 9986,
        70143: 9985,
        65072: 9984,
        69167: 9983,
        65118: 9982,
        69150: 9981,
        69113: 9980,
        68972: 9979,
        58483: 9978,
        56347: 9977,
        52352: 9976,
    },
    "dk_frost": {
        77992: 10000,
        77997: 9999,
        78002: 9998,
        77205: 9997,
        77200: 9996,
        69113: 9995,
        68972: 9994,
        71617: 9993,
        65072: 9992,
        69167: 9991,
        65118: 9990,
        68712: 9989,
        56393: 9988,
        58180: 9987,
        56100: 9986,
        56345: 9985,
    },
    "dk_unholy": {
        77992: 10000,
        77997: 9999,
        78002: 9998,
        77205: 9997,
        77200: 9996,
        69167: 9995,
        65072: 9994,
        56393: 9993,
        69113: 9992,
        68972: 9991,
        71617: 9990,
        65118: 9989,
        58180: 9988,
        68712: 9987,
        56100: 9986,
        56345: 9985,
    },
    "druid_balance": {
        77995: 10000,
        77991: 9999,
        77198: 9998,
        77203: 9997,
        69110: 9996,
        78000: 9995,
        77975: 9994,
        77971: 9993,
        77990: 9992,
        77206: 9991,
        65105: 9990,
        70142: 9989,
        77970: 9988,
        62047: 9987,
        69139: 9986,
        65053: 9985,
        65110: 9984,
        56400: 9983,
        56320: 9982,
        56462: 9981,
        64645: 9980,
        68710: 9979,
        56339: 9978,
        56407: 9977,
    },
    "druid_feral": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77974: 9996,
        77979: 9995,
        77993: 9994,
        77113: 9993,
        69150: 9992,
        77202: 9991,
        77973: 9990,
        69112: 9989,
        65140: 9988,
        65026: 9987,
        58181: 9986,
        69001: 9985,
        59520: 9984,
        56328: 9983,
        62468: 9982,
        56394: 9981,
    },
    "druid_guardian": {
        78003: 10000,
        77994: 9999,
        69109: 9998,
        77990: 9997,
        65109: 9996,
        68915: 9995,
        65048: 9994,
        70143: 9993,
        69150: 9992,
        69112: 9991,
        65140: 9990,
        65026: 9989,
        58181: 9988,
        69001: 9987,
        62471: 9986,
        56347: 9985,
        62468: 9984,
    },
    "druid_restoration": {
        77996: 10000,
        78001: 9999,
        77199: 9998,
        69111: 9997,
        77209: 9996,
        77976: 9995,
        72898: 9994,
        68926: 9993,
        77989: 9992,
        77981: 9991,
        77204: 9990,
        65124: 9989,
        69149: 9988,
        64645: 9987,
        62050: 9986,
        59500: 9985,
        68983: 9984,
        69000: 9983,
        60233: 9982,
        58184: 9981,
        68777: 9980,
        62467: 9979,
        56351: 9978,
        62044: 9977,
        65804: 9976,
    },
    "hunter_beastmastery": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77979: 9996,
        77974: 9995,
        77993: 9994,
        69150: 9993,
        69112: 9992,
        68994: 9991,
        68927: 9990,
        69001: 9989,
        65026: 9988,
        65140: 9987,
        56394: 9986,
        56328: 9985,
        62051: 9984,
        56440: 9983,
    },
    "hunter_marksmanship": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77979: 9996,
        77974: 9995,
        77993: 9994,
        69150: 9993,
        69112: 9992,
        68994: 9991,
        68927: 9990,
        69001: 9989,
        65026: 9988,
        65140: 9987,
        56394: 9986,
        56328: 9985,
        62051: 9984,
        56440: 9983,
        62468: 9982,
        62463: 9981,
    },
    "hunter_survival": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77979: 9996,
        77974: 9995,
        77993: 9994,
        69150: 9993,
        69112: 9992,
        68994: 9991,
        68927: 9990,
        69001: 9989,
        65026: 9988,
        65140: 9987,
        56394: 9986,
        56328: 9985,
        62051: 9984,
        56440: 9983,
        62468: 9982,
        62463: 9981,
    },
    "mage_arcane": {
        77995: 10000,
        78000: 9999,
        77114: 9998,
        77991: 9997,
        77975: 9996,
        77980: 9995,
        60233: 9994,
        69110: 9993,
        62047: 9992,
        62021: 9991,
        65105: 9990,
        70142: 9989,
        68998: 9988,
        65053: 9987,
        62465: 9986,
        62470: 9985,
        58183: 9984,
        56320: 9983,
        56339: 9982,
        56407: 9981,
    },
    "mage_fire": {
        77991: 10000,
        77995: 9999,
        77971: 9998,
        77975: 9997,
        69110: 9996,
        77114: 9995,
        62047: 9994,
        62021: 9993,
        65105: 9992,
        68998: 9991,
        65053: 9990,
        62465: 9989,
        62470: 9988,
        58183: 9987,
        56400: 9986,
        56320: 9985,
        56462: 9984,
        56407: 9983,
        56339: 9982,
    },
    "mage_frost": {
        77991: 10000,
        77995: 9999,
        69110: 9998,
        77114: 9997,
        77971: 9996,
        77975: 9995,
        62047: 9994,
        62021: 9993,
        68998: 9992,
        65053: 9991,
        65105: 9990,
        62465: 9989,
        62470: 9988,
        58183: 9987,
        56320: 9986,
        56407: 9985,
        56462: 9984,
        56339: 9983,
    },
    "paladin_holy": {
        77996: 10000,
        78001: 9999,
        77989: 9998,
        77199: 9997,
        77209: 9996,
        77976: 9995,
        77204: 9994,
        77981: 9993,
        77969: 9992,
        65124: 9991,
        69111: 9990,
        69149: 9989,
        68926: 9988,
        62050: 9987,
        62044: 9986,
        64645: 9985,
        69000: 9984,
        59500: 9983,
        68983: 9982,
        68777: 9981,
        52207: 9980,
        60233: 9979,
        58184: 9978,
        56351: 9977,
        56320: 9976,
        62467: 9975,
    },
    "paladin_protection": {
        78003: 10000,
        77117: 9999,
        69138: 9998,
        77990: 9997,
        62466: 9996,
        62471: 9995,
        69109: 9994,
        71617: 9993,
        69002: 9992,
        68915: 9991,
        58483: 9990,
        52219: 9989,
        65048: 9988,
        65109: 9987,
        59332: 9986,
        59515: 9985,
        62464: 9984,
        62469: 9983,
        52352: 9982,
        56347: 9981,
    },
    "paladin_retribution": {
        77997: 10000,
        77992: 9999,
        78002: 9998,
        77200: 9997,
        77116: 9996,
        73496: 9995,
        77210: 9994,
        69113: 9993,
        68972: 9992,
        71617: 9991,
        77205: 9990,
        77977: 9989,
        72899: 9988,
        65072: 9987,
        73491: 9986,
        77982: 9985,
        77972: 9984,
        68712: 9983,
        69002: 9982,
        59224: 9981,
        69167: 9980,
        56393: 9979,
        70141: 9978,
        65118: 9977,
        58180: 9976,
        59461: 9975,
        52351: 9974,
        56285: 9973,
        56345: 9972,
    },
    "priest_discipline": {
        77995: 10000,
        77198: 9999,
        77996: 9998,
        77991: 9997,
        77989: 9996,
        78001: 9995,
        77975: 9994,
        77199: 9993,
        77204: 9992,
        77209: 9991,
        77976: 9990,
        69149: 9989,
        77969: 9988,
        77981: 9987,
        77114: 9986,
        77115: 9985,
        69110: 9984,
        69139: 9983,
        69111: 9982,
        68982: 9981,
        68983: 9980,
        68926: 9979,
        65124: 9978,
        65105: 9977,
        70142: 9976,
        62050: 9975,
        59500: 9974,
        64645: 9973,
        68777: 9972,
        52207: 9971,
        59519: 9970,
        60233: 9969,
        65029: 9968,
        58184: 9967,
        59354: 9966,
        56320: 9965,
        56351: 9964,
        52354: 9963,
        56414: 9962,
        56462: 9961,
        58183: 9960,
        56339: 9959,
        56400: 9958,
        56290: 9957,
        65804: 9956,
        63839: 9955,
        55787: 9954,
    },
    "priest_holy": {
        77996: 10000,
        78001: 9999,
        77199: 9998,
        77976: 9997,
        77989: 9996,
        77209: 9995,
        77981: 9994,
        69149: 9993,
        77114: 9992,
        77115: 9991,
        77204: 9990,
        77969: 9989,
        69111: 9988,
        68983: 9987,
        68926: 9986,
        69110: 9985,
        69139: 9984,
        68982: 9983,
        65124: 9982,
        70142: 9981,
        62050: 9980,
        65105: 9979,
        59500: 9978,
        59519: 9977,
        64645: 9976,
        68777: 9975,
        52207: 9974,
        58184: 9973,
        60233: 9972,
        65029: 9971,
        59354: 9970,
        56351: 9969,
        56320: 9968,
        52354: 9967,
        56462: 9966,
        56414: 9965,
        58183: 9964,
        56339: 9963,
        56400: 9962,
        56290: 9961,
        65804: 9960,
        63839: 9959,
        55787: 9958,
    },
    "priest_shadow": {
        77995: 10000,
        78000: 9999,
        77198: 9998,
        77991: 9997,
        77114: 9996,
        69110: 9995,
        62047: 9994,
        72898: 9993,
        68925: 9992,
        69139: 9991,
        68982: 9990,
        68998: 9989,
        69000: 9988,
        65053: 9987,
        65105: 9986,
        70142: 9985,
        58183: 9984,
        59326: 9983,
        52353: 9982,
        59519: 9981,
        56400: 9980,
        68777: 9979,
        56320: 9978,
        62465: 9977,
        62470: 9976,
        56290: 9975,
        65110: 9974,
        59514: 9973,
        64645: 9972,
        56407: 9971,
        56462: 9970,
        56339: 9969,
        55889: 9968,
        65804: 9967,
        63839: 9966,
        55787: 9965,
    },
    "rogue_assassination": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77993: 9997,
        77207: 9996,
        77202: 9995,
        77974: 9994,
        69150: 9993,
        77113: 9992,
        77979: 9991,
        77973: 9990,
        69112: 9989,
        68994: 9988,
        65026: 9987,
        68927: 9986,
        58181: 9985,
        68709: 9984,
        56328: 9983,
        56394: 9982,
        59441: 9981,
        59520: 9980,
        56427: 9979,
        65140: 9978,
        68776: 9977,
        59473: 9976,
        56440: 9975,
        56295: 9974,
        52199: 9973,
    },
    "rogue_combat": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77993: 9996,
        77974: 9995,
        77113: 9994,
        77979: 9993,
        77202: 9992,
        69150: 9991,
        69112: 9990,
        77973: 9989,
        68994: 9988,
        65026: 9987,
        68927: 9986,
        58181: 9985,
        59441: 9984,
        65140: 9983,
        56427: 9982,
        56394: 9981,
        56328: 9980,
        59520: 9979,
        59473: 9978,
        68776: 9977,
        68709: 9976,
        56440: 9975,
        56295: 9974,
        52199: 9973,
    },
    "rogue_subtlety": {
        77994: 10000,
        77999: 9999,
        77197: 9998,
        77207: 9997,
        77113: 9996,
        77993: 9995,
        77974: 9994,
        77979: 9993,
        77202: 9992,
        69150: 9991,
        69112: 9990,
        77973: 9989,
        68994: 9988,
        65026: 9987,
        68927: 9986,
        58181: 9985,
        65140: 9984,
        59441: 9983,
        68709: 9982,
        56427: 9981,
        56328: 9980,
        59520: 9979,
        59473: 9978,
        56394: 9977,
        68776: 9976,
        56440: 9975,
        56295: 9974,
        52199: 9973,
    },
    "shaman_elemental": {
        77995: 10000,
        78000: 9999,
        69110: 9998,
        77114: 9997,
        62047: 9996,
        68925: 9995,
        69139: 9994,
        65053: 9993,
        65110: 9992,
        65105: 9991,
        70142: 9990,
        58183: 9989,
        56320: 9988,
        56462: 9987,
        68777: 9986,
        68710: 9985,
        56339: 9984,
        56407: 9983,
        64645: 9982,
        65804: 9981,
    },
    "shaman_enhancement": {
        77994: 10000,
        77999: 9999,
        69150: 9998,
        77113: 9997,
        69001: 9996,
        69112: 9995,
        65140: 9994,
        58181: 9993,
        65026: 9992,
        59520: 9991,
        56427: 9990,
        56394: 9989,
        62463: 9988,
        56440: 9987,
        56328: 9986,
        62051: 9985,
    },
    "shaman_restoration": {
        77996: 10000,
        78001: 9999,
        77995: 9998,
        77989: 9997,
        69111: 9996,
        65124: 9995,
        69149: 9994,
        62050: 9993,
        62044: 9992,
        64645: 9991,
        60233: 9990,
        68777: 9989,
        52207: 9988,
        58184: 9987,
        62467: 9986,
        56351: 9985,
        65804: 9984,
    },
    "warlock_affliction": {
        77991: 10000,
        78000: 9999,
        77203: 9998,
        77208: 9997,
        77995: 9996,
        69110: 9995,
        62047: 9994,
        69139: 9993,
        68925: 9992,
        68982: 9991,
        65053: 9990,
        68998: 9989,
        59326: 9988,
        65105: 9987,
        59519: 9986,
        62465: 9985,
        58183: 9984,
        56320: 9983,
        56407: 9982,
        56462: 9981,
        56339: 9980,
        52353: 9979,
    },
    "warlock_demonology": {
        77991: 10000,
        78000: 9999,
        77203: 9998,
        77208: 9997,
        77995: 9996,
        69110: 9995,
        70142: 9994,
        62047: 9993,
        69139: 9992,
        68925: 9991,
        68982: 9990,
        65053: 9989,
        68998: 9988,
        58183: 9987,
        59326: 9986,
        65105: 9985,
        59519: 9984,
        62465: 9983,
        56320: 9982,
        56407: 9981,
        56339: 9980,
        56462: 9979,
        52353: 9978,
        65804: 9977,
    },
    "warlock_destruction": {
        77991: 10000,
        78000: 9999,
        77203: 9998,
        77208: 9997,
        77995: 9996,
        69110: 9995,
        62047: 9994,
        69139: 9993,
        68925: 9992,
        68982: 9991,
        65053: 9990,
        68998: 9989,
        59326: 9988,
        65105: 9987,
        59519: 9986,
        62465: 9985,
        58183: 9984,
        56320: 9983,
        56407: 9982,
        56462: 9981,
        56339: 9980,
        52353: 9979,
    },
    "warrior_arms": {
        77992: 10000,
        78002: 9999,
        77997: 9998,
        69167: 9997,
        69113: 9996,
        68972: 9995,
        71617: 9994,
        65072: 9993,
        59461: 9992,
        60572: 9991,
        65118: 9990,
        58180: 9989,
        68712: 9988,
        56393: 9987,
        62049: 9986,
        56100: 9985,
        56345: 9984,
    },
    "warrior_fury": {
        78432: 10000,
        52206: 9999,
        78492: 9998,
        77110: 9997,
        71433: 9996,
        71215: 9995,
        71208: 9994,
        71617: 9993,
        60226: 9992,
        65382: 9991,
        69167: 9990,
        69113: 9989,
        68972: 9988,
        65072: 9987,
        59461: 9986,
        60572: 9985,
        65118: 9984,
        58180: 9983,
        68712: 9982,
        56393: 9981,
    },
    "warrior_protection": {
        78003: 10000,
        77990: 9999,
        77211: 9998,
        77206: 9997,
        77983: 9996,
        77970: 9995,
        69138: 9994,
        69109: 9993,
        68915: 9992,
        71617: 9991,
        72900: 9990,
        68981: 9989,
        77117: 9988,
        77998: 9987,
        65048: 9986,
        65109: 9985,
        70143: 9984,
        68996: 9983,
        69002: 9982,
        62471: 9981,
        68713: 9980,
        58182: 9979,
        59332: 9978,
        59515: 9977,
        56347: 9976,
        58483: 9975,
        52352: 9974,
        50364: 9973,
        56280: 9972,
        56449: 9971,
        62048: 9970,
        56370: 9969,
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
        for phase in ["0", "1", "2", "3", "4"]:   # select items from P0 to P5
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
