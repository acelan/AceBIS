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
    33350,
    34139,
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
    47542,
    47543,
    47544,
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
    51804: '2',
    51805: '2',
    51806: '2',
    51807: '2',
    51808: '2',
    54801: '2',     # 54801 ~ 54806 仲夏火焰節
    54802: '2',
    54803: '2',
    54804: '2',
    54805: '2',
    54806: '2',
}

# to better score trinket
rescore = {
    # Mirror of Truth
    40684: {"AssassinationRogue": 1000, "SurvivalHunter": 996, "EnhancementShaman": 1000, "UnholyDK": 996, "FeralDruid": 998, "FuryWarrior": 996, "ArmsWarrior": 996, "RetributionPaladin": 997},
    # Fury of the Five Flights
    40431: {"AssassinationRogue": 998, "RetributionPaladin": 999, "UnholyDK": 997, "FeralDruid": 995, "SurvivalHunter": 998, "EnhancementShaman": 996, "FuryWarrior": 998, "ArmsWarrior": 998},
    # Dying Curse
    40255: {"BalanceDruid": 1000, "ArcaneMage": 1995, "ShadowPriest": 1996, "ElementalShaman": 2998, "AfflictionWarlock": 1993, "RestorationDruid": 992, "EnhancementShaman": 999, "FireMage": 1997},
    # Illustration of the Dragon Soul
    40432: {"BalanceDruid": 999, "ShadowPriest": 1995, "ElementalShaman": 999, "AfflictionWarlock": 2996, "RestorationDruid": 1998, "ArcaneMage": 1996, "DisciplinePriest": 3000, "RestorationShaman": 1000, "FireMage": 1996},
    40682: {"BalanceDruid": 998, "ArcaneMage": 997, "ShadowPriest": 1993, "ElementalShaman": 997, "AfflictionWarlock": 997, "FireMage": 997},
    40373: {"BalanceDruid": 996, "ShadowPriest": 994},
    37873: {"BalanceDruid": 995, "ShadowPriest": 996, "ElementalShaman": 996},
    42395: {"BalanceDruid": 994, "ShadowPriest": 993, "ElementalShaman": 995},
    49076: {"BalanceDruid": 993, "ArcaneMage": 996, "AfflictionWarlock": 996, "FireMage": 996},
    37835: {"BalanceDruid": 992, "RestorationDruid": 996, "DisciplinePriest": 994, "RestorationShaman": 994},
    42988: {"BalanceDruid": 991, "RestorationDruid": 995, "DisciplinePriest": 995},
    37660: {"BalanceDruid": 990},
    44322: {"BalanceDruid": 1988, "RestorationDruid": 997},
    36972: {"BalanceDruid": 988},
    # Darkmoon Card: Greatness(+str)
    42987: {"FeralDruid": 1996, "RetributionPaladin": 2000, "FuryWarrior": 2000, "UnholyDK": 1999, "ProtectionPaladin": 1992, "ArmsWarrior": 2000},
    # Embrace of the Spider
    39229: {"ArcaneMage": 1000, "BalanceDruid": 997, "ShadowPriest": 1994, "ElementalShaman": 998, "RestorationShaman": 998, "AfflictionWarlock": 2994, "FireMage": 998},
    # Figurine - Monarch Crab
    44063: {"ProtectionPaladin": 1998, "ProtectionWarrior": 1998, "ProtectionDK": 1000},
    # Essence of Gossamer
    37220: {"ProtectionPaladin": 1997, "TankDruid": 999, "ProtectionWarrior": 997},
    # Darkmoon Card: Greatness(+agi)
    44253: {"AssassinationRogue": 999, "TankDruid": 1000, "SurvivalHunter": 3000, "EnhancementShaman": 997, "ProtectionWarrior": 998, "FeralDruid": 1994},
    # Meteorite Whetstone
    37390: {"EnhancementShaman": 998, "UnholyDK": 1998, "FeralDruid": 996, "AssassinationRogue": 992},
    # Grim Toll
    40256: {"FuryWarrior": 999, "UnholyDK": 998, "FeralDruid": 1997, "SurvivalHunter": 997, "AssassinationRogue": 993, "ArmsWarrior": 999},
    # Defender's Code
    40257: {"ProtectionWarrior": 1996, "ProtectionPaladin": 1993},
    # Figurine - Ruby Hare
    42341: {"ProtectionDK": 999, "ProtectionWarrior": 996, "ProtectionPaladin": 1996},
    # Essence of Gossamer
    37720: {"ProtectionDK": 998},
    # Valor Medal of the First War
    40683: {"ProtectionDK": 997, "ProtectionPaladin": 993},
    # Seal of the Pantheon
    36993: {"ProtectionDK": 996, "ProtectionWarrior": 994},
    # Sonic Booster
    40767: {"ProtectionDK": 995},
    # Loatheb's Shadow
    39257: {"UnholyDK": 995, "FeralDruid": 997, "SurvivalHunter": 999, "AssassinationRogue": 994, "FuryWarrior": 997, "ArmsWarrior": 997},
    # Incisor Fragment
    37723: {"UnholyDK": 994, "FeralDruid": 994},
    40531: {"FeralDruid": 993, "AssassinationRogue": 997, "EnhancementShaman": 993, "UnholyDK": 1997},
    37111: {"RestorationDruid": 1996, "HolyPaladin": 2999, "RestorationShaman": 999, "RestorationShaman": 1998},
    37675: {"RestorationDruid": 998, "RestorationShaman": 993},
    44254: {"RestorationDruid": 1990, "ShadowPriest": 993},
    40258: {"RestorationDruid": 993, "DisciplinePriest": 993, "RestorationShaman": 996},
    42990: {"ShadowPriest": 996},
    37264: {"ShadowPriest": 995},
    34427: {"AssassinationRogue": 996},
    40371: {"AssassinationRogue": 995, "EnhancementShaman": 994, "RetributionPaladin": 998},
    37166: {"AssassinationRogue": 991, "EnhancementShaman": 995, "FuryWarrior": 995, "ArmsWarrior": 995},
    43573: {"EnhancementShaman": 992},
    37872: {"ProtectionWarrior": 995},
    39292: {"ProtectionWarrior": 993, "ProtectionPaladin": 994},
    44255: {"HolyPaladin": 1998, "DisciplinePriest": 1995},
    42413: {"HolyPaladin": 1997, "DisciplinePriest": 998},
    28823: {"HolyPaladin": 997},
    29387: {"ProtectionPaladin": 995},
    40372: {"ProtectionPaladin": 992},
    42132: {"DisciplinePriest": 999},
    40382: {"DisciplinePriest": 997, "RestorationShaman": 995},
    40685: {"DisciplinePriest": 992, "RestorationShaman": 997},
    37660: {"DisciplinePriest": 991},
    37657: {"DisciplinePriest": 990, "RestorationDruid": 1989},
    37844: {"RestorationShaman": 992},

    # P2
    45466: {"BalanceDruid": 2000, "ShadowPriest": 2997, "ArcaneMage": 1999, "ElementalShaman": 1998, "RestorationShaman": 1999, "AfflictionWarlock": 2999, "FireMage": 2998},
    45518: {"BalanceDruid": 2999, "ShadowPriest": 2999, "ElementalShaman": 2999, "ArcaneMage": 2000, "AfflictionWarlock": 3000, "FireMage": 2999},
    45931: {"FeralDruid": 3000, "SurvivalHunter": 1998, "AssassinationRogue": 2995, "EnhancementShaman": 1996, "ArmsWarrior": 1999, "FuryWarrior": 1999},
    45609: {"FeralDruid": 2997, "UnholyDK": 2000, "AssassinationRogue": 2999, "SurvivalHunter": 1997, "RetributionPaladin": 1999, "EnhancementShaman": 2999, "ArmsWarrior": 1998, "FuryWarrior": 1998},
    45158: {"TankDruid": 2998, "ProtectionPaladin": 2998, "ProtectionWarrior": 2997, "ProtectionDK": 2998},
    46021: {"TankDruid": 1999, "ProtectionPaladin": 2997, "ProtectionWarrior": 2995, "ProtectionDK": 2997},
    45522: {"RetributionPaladin": 1996, "UnholyDK": 1994, "FeralDruid": 1993, "ProtectionPaladin": 1991, "AssassinationRogue": 2996, "EnhancementShaman": 1997},
    46038: {"AssassinationRogue": 2997, "UnholyDK": 1995, "FeralDruid": 2996, "SurvivalHunter": 1999, "RetributionPaladin": 1998, "EnhancementShaman": 1999, "ArmsWarrior": 1997, "FuryWarrior": 1997},
    45490: {"BalanceDruid": 1998, "RestorationDruid": 2996, "ArcaneMage": 1998, "ShadowPriest": 2996, "RestorationShaman": 1997, "AfflictionWarlock": 1997},
    45308: {"BalanceDruid": 1997, "DisciplinePriest": 1998, "ElementalShaman": 1997, "RestorationShaman": 1995, "AfflictionWarlock": 2993, "ArcaneMage": 1997, "ShadowPriest": 2995, "FireMage": 2997},
    45263: {"UnholyDK": 1996, "FeralDruid": 1995, "SurvivalHunter": 1996, "RetributionPaladin": 1997, "AssassinationRogue": 1995, "EnhancementShaman": 1998},
    45286: {"UnholyDK": 1993, "ProtectionPaladin": 1990, "RetributionPaladin": 1995, "AssassinationRogue": 2993},
    45703: {"RestorationDruid": 2997, "DisciplinePriest": 1994},
    45535: {"RestorationDruid": 2999, "DisciplinePriest": 1999, "ShadowPriest": 1992, "RestorationShaman": 2000},
    45929: {"RestorationDruid": 1997, "DisciplinePriest": 1997, "ShadowPriest": 1991, "RestorationShaman": 1996},
    46051: {"RestorationDruid": 2998, "HolyPaladin": 3000, "DisciplinePriest": 1996},
    40430: {"RestorationDruid": 1994},
    19288: {"RestorationDruid": 1993},
    45292: {"RestorationDruid": 1992},
    45148: {"ArcaneMage": 1996, "ShadowPriest": 1998, "AfflictionWarlock": 2992, "FireMage": 1995},
    45313: {"ProtectionPaladin": 1995, "ProtectionWarrior": 1997},
    45507: {"ProtectionPaladin": 1994},
    46132: {"ShadowPriest": 1997},
    45866: {"AfflictionWarlock": 1994},

    # P3
    47464: {"UnholyDK": 3000, "FeralDruid": 2999, "TankDruid": 2999, "SurvivalHunter": 2999, "ProtectionPaladin": 2995, "RetributionPaladin": 3000, "AssassinationRogue": 3000, "ArmsWarrior": 3000, "FuryWarrior": 3000},
    47131: {"UnholyDK": 3000, "FeralDruid": 2999, "TankDruid": 2999, "SurvivalHunter": 2999, "ProtectionPaladin": 2995, "RetributionPaladin": 3000, "AssassinationRogue": 3000, "ArmsWarrior": 3000, "FuryWarrior": 3000},
    47303: {"UnholyDK": 2999, "FeralDruid": 2998, "SurvivalHunter": 2998, "ProtectionPaladin": 2994, "AssassinationRogue": 2998},
    47115: {"UnholyDK": 2999, "FeralDruid": 2998, "SurvivalHunter": 2998, "ProtectionPaladin": 2994, "AssassinationRogue": 2998},
    47088: {"ProtectionDK": 3000, "TankDruid": 3000, "ProtectionPaladin": 3000, "ProtectionWarrior": 3000},
    47451: {"ProtectionDK": 3000, "TankDruid": 3000, "ProtectionPaladin": 3000, "ProtectionWarrior": 3000},
    47808: {"ProtectionDK": 2999},
    47290: {"ProtectionDK": 2999, "ProtectionPaladin": 2999, "ProtectionWarrior": 2999},
    47735: {"ProtectionDK": 2996, "TankDruid": 2997, "ProtectionPaladin": 2995, "ProtectionWarrior": 2998},
    47477: {"BalanceDruid": 3000, "ArcaneMage": 3000, "ShadowPriest": 3000, "ElementalShaman": 3000, "EnhancementShaman": 3000, "AfflictionWarlock": 2998, "FireMage": 3000},
    47188: {"BalanceDruid": 3000, "ArcaneMage": 3000, "ShadowPriest": 3000, "ElementalShaman": 3000, "EnhancementShaman": 3000, "AfflictionWarlock": 2998, "FireMage": 3000},
    47316: {"BalanceDruid": 2998, "ShadowPriest": 2998, "AfflictionWarlock": 2997},
    47182: {"BalanceDruid": 2998, "ShadowPriest": 2998, "AfflictionWarlock": 2997},
    47261: {"TankDruid": 2996},
    47059: {"BalanceDruid": 3000, "DisciplinePriest": 2999, "RestorationShaman": 3000, "AfflictionWarlock": 2991},
    47432: {"BalanceDruid": 3000, "DisciplinePriest": 2999, "RestorationShaman": 3000, "AfflictionWarlock": 2991},
    48724: {"BalanceDruid": 2995, "HolyPaladin": 2998},
    47080: {"ProtectionPaladin": 2999, "ProtectionWarrior": 2999},
    47216: {"ProtectionPaladin": 2996, "ProtectionWarrior": 2996},
    47213: {"ShadowPriest": 2995, "AfflictionWarlock": 2995},
    47734: {"AssassinationRogue": 2994},
    47948: {"AssassinationRogue": 2991},
    48020: {"AssassinationRogue": 2991},
    47725: {"AssassinationRogue": 2990},
    47881: {"AssassinationRogue": 2990},
    47214: {"AssassinationRogue": 2989},
    48722: {"AfflictionWarlock": 2990},
    49487: {"ProtectionWarrior": 2994},

    # P2
    # Sigils for Unholy Death Knight
    45254: {"UnholyDK": 2000},
    42621: {"UnholyDK": 1999},
    # Relics for Blood Death Knight Tank
    45144: {"ProtectionDK": 2000},
    # Idols for Balance Druid DPS
    # Idols for Feral Druid DPS
    # Idols for Feral Druid Tank
    45509: {"TankDruid": 3000},
    # Idols for Restoration Druid Healer
    46138: {"RestorationDruid": 1997},
    # Librams for Holy Paladin Healer
    # Librams for Protection Paladin Tank
    45145: {"ProtectionPaladin": 2000},
    # Librams for Retribution Paladin
    42853: {"RetributionPaladin": 2000},
    # Totems for Elemental Shaman DPS
    # Totems for Enhancement Shaman DPS
    42608: {"EnhancementShaman": 2000},
    # Totems for Restoration Shaman Healer
    45114: {"RestorationShaman": 2999},

    # Sigils for Unholy Death Knight
    42620: {"UnholyDK": 1000},
    40207: {"UnholyDK": 999, "ProtectionDK": 999},
    40867: {"UnholyDK": 998},
    # Relics for Blood Death Knight Tank
    40714: {"ProtectionDK": 1000},
    40822: {"ProtectionDK": 998},
    40715: {"ProtectionDK": 997},
    # Idols for Balance Druid DPS
    40321: {"BalanceDruid": 1000},
    40712: {"BalanceDruid": 999},
    32387: {"BalanceDruid": 998},
    27518: {"BalanceDruid": 997},
    38360: {"BalanceDruid": 996},
    # Idols for Feral Druid DPS
    39757: {"FeralDruid": 1000},
    40713: {"FeralDruid": 999},
    38295: {"FeralDruid": 998},
    # Idols for Feral Druid Tank
    38365: {"TankDruid": 2999},
    33509: {"TankDruid": 999},
    # Idols for Restoration Druid Healer
    40342: {"RestorationDruid": 3000},
    33508: {"RestorationDruid": 1999},
    25643: {"RestorationDruid": 1998},
    # Librams for Holy Paladin Healer
    40705: {"HolyPaladin": 3000},
    # Librams for Protection Paladin Tank
    40707: {"ProtectionPaladin": 1000},
    # Librams for Retribution Paladin
    42852: {"RetributionPaladin": 1000},
    42851: {"RetributionPaladin": 999},
    42611: {"RetributionPaladin": 998},
    # Totems for Elemental Shaman DPS
    40267: {"ElementalShaman": 1000},
    40708: {"ElementalShaman": 999, "EnhancementShaman": 999},
    32330: {"ElementalShaman": 998},
    # Totems for Enhancement Shaman DPS
    40322: {"EnhancementShaman": 1000},
    33507: {"EnhancementShaman": 997},
    37575: {"EnhancementShaman": 996},
    # Totems for Restoration Shaman Healer
    40709: {"RestorationShaman": 2998},
    38368: {"RestorationShaman": 999},

    # P3
    # Sigils for Unholy Death Knight DPS Phase 3
    47528: {"UnholyDK": 3000},
    47526: {"UnholyDK": 3000},
    47475: {"UnholyDK": 2999},
    47156: {"UnholyDK": 2999},
    48513: {"UnholyDK": 2998},
    47472: {"UnholyDK": 2997},
    47001: {"UnholyDK": 2997},
    46097: {"UnholyDK": 2996},
    45947: {"UnholyDK": 2995},
    48050: {"UnholyDK": 2994},
    47973: {"UnholyDK": 2994},
    # Relics for Blood Death Knight Tanks in Phase 3
    47672: {"ProtectionDK": 3000},
    # Idols for Balance Druid DPS Phase 3
    47670: {"BalanceDruid": 1000},
    # Idols for Feral Druid DPS Phase 3
    47668: {"FeralDruid": 3000},
    # Idols for Feral Druid Tank Phase 3
    47668: {"TankDruid": 2998},
    # Idols for Restoration Druid Healer Phase 3
    47671: {"RestorationDruid": 2999},
    # Librams for Holy Paladin Healer Phase 3
    # Librams for Protection Paladin Tank Phase 3
    47664: {"ProtectionPaladin": 3000},
    47661: {"ProtectionPaladin": 2999, "RetributionPaladin": 3000},
    # Librams for Retribution Paladin
    42854: {"RetributionPaladin": 2999},
    # Totems for Elemental Shaman DPS in Phase 3
    47666: {"ElementalShaman": 3000, "EnhancementShaman": 3000},
    # Totems for Enhancement Shaman DPS in Phase 3
    # Totems for Restoration Shaman Healer in Phase 3
    47665: {"RestorationShaman": 3000},


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
                for i in {'dk_unholy', 'dk_protection', 'druid_balance', 'druid_feral', 'druid_restoration', 'druid_tank', 'hunter_survival', 'mage_arcane', 'mage_fire', 'paladin_holy', 'paladin_protection', 'paladin_retribution', 'priest_discipline', 'priest_shadow', 'rogue_assassination', 'rogue_combat', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_affliction', 'warrior_arms', 'warrior_fury', 'warrior_protection'}:
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

                    # item is only for Ally or Horde
                    side = "Neutral"
                    if "side" in item:
                        side = sides[int(item["side"])]

                    spec = i.split("_")[1].capitalize()

                    if itemid in rescore:
                        if spec + cclass in rescore[itemid]:
                            score = rescore[itemid][spec + cclass]

                    itemclass = ""
                    itemsubclass = ""
                    itemtype = ""
                    try:
                        itemclass = item_class[int(item["class"]["@id"])]
                        itemtype = inv_type[int(item["inventorySlot"]["@id"])]

                        if int(item["subclass"]) >= 0:
                            if (int(item["class"]["@id"]) == 2) or (int(item["class"]["@id"]) == 0):
                                itemsubclass = item2_subclass[int(item["subclass"])]
                            elif int(item["class"]["@id"]) == 4:
                                itemsubclass = item4_subclass[int(item["subclass"])]
                            #else:
                            #    print("Invalid subclass id: %s - type = %s, class = %s, subclass = %s" % (itemid, item["inventorySlot"]["@id"], item["class"]["@id"], item["subclass"]))

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
                        if score == 0:
                            score = itemid/100
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

                    if itemtype in ["MainHand", "OneHand", "OffHand", "TwoHand"]:
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
                        if cclass in ["DK"]:
                            if itemsubclass in ["Staff", "Fist"]:
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

                    # For Warrior, Paladin, and DK
                    if spec == "Protection" and itemclass == "Armor":
                            if itemsubclass in ["Cloth", "Leather", "Mail"]:
                                continue

                    if spec == "Protection" and "defrtng" not in item and "dodgertng" not in item and "parryrtng" not in item and "blockrtng" not in item and "blockamount" not in item:
                        if itemclass == "Armor" and itemtype not in ["Amulet", "Trinket", "Ranged"]:
                            continue
                        # Only Warrior's weapon requires those attributes
                        if itemclass == "Weapon" and itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"] and cclass == "Warrior":
                            continue
                        if itemclass == "Weapon" and cclass == "Paladin" and "agi" in item:
                            score = score + int(item["agi"])

                    # special setting for current assassination rogue weapon
                    if cclass == "Rogue" and spec == "Assassination":
                        if itemsubclass  == "Dagger":
                            if float(item["speed"]) > 1.4:          # slow weapon should equip in off hand
                                if itemtype == "OneHand":
                                    itemtype = "OffHand"
                            elif float(item["speed"]) == 1.3:       # for fastest weapon
                                score = score * 1.3
                            score = score + int(item["mledps"])

                    item_tmp = {"id": itemid, "phase": phase, "class": cclass, "spec": spec, "slot": s, "type": itemtype, "itemclass": itemclass, "subclass": itemsubclass, "score": score, "side": side}
                    if itemtype == "Head":
                        itemtype = "Helm"
                    elif itemtype == "Wrist":
                        itemtype = "Bracers"
                    elif itemtype == "Legs":
                        itemtype = "Pants"
                    elif itemtype == "Feet":
                        itemtype = "Boots"

                    # Fury Warrior can use TwoHand weapon as MainHand and OffHand weapon, so treat it as OneHand
                    if cclass == "Warrior" and spec == "Fury":
                        if itemtype == "TwoHand":
                            #bis_list[cclass][spec][phase][itemtype][itemid] = item_tmp
                            itemtype = "OneHand"
                        elif itemtype in ["MainHand", "OneHand"]:
                            continue

                    bis_list[cclass][spec][phase][itemtype][itemid] = item_tmp

                    #if itemtype == "Trinket" and cclass == "Warlock" and spec == "Affliction":
                    #    print("after %s %s" % (itemid, score))
                    #if itemid in [54801, 54802, 54803, 54804, 54805]:
                    #if itemid in [47569]:
                        #print("%s %s %s %s %s" % (spec, cclass, itemid, score, phase))
                        #print("after %s %s" % (itemid, score))

    #print(list(bis_list["Warrior"]["Fury"]["1"]))
    return bis_list

bis_list = build_list()

for cclass in classs.values():
    for spec in bis_list[cclass].keys():
        print("%s - %s" % (cclass, spec))
        output = ""
        for phase in {"0", "1", "2", "3", "4"}:   # select items from P0 to P5
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
                    elif "OffHand" not in bis_list[cclass][spec][phase]:
                        s = "OffHand"
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
                    #if itemid == 47569:
                    #    print("%s %s %s %s %s #%s" % (spec, cclass, itemid, items[itemid]["score"], p, index))
                    #print(output)
                    index += 1
                    if index > 30:
                        break
        write_file(spec + cclass, output)
