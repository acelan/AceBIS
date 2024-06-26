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
    65743,
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
    # Mirror of Truth
    40684: {"AssassinationRogue": 1000, "SurvivalHunter": 996, "EnhancementShaman": 1000, "UnholyDK": 996, "FeralDruid": 998, "FuryWarrior": 996, "ArmsWarrior": 996, "RetributionPaladin": 3991},
    # Fury of the Five Flights
    40431: {"AssassinationRogue": 998, "RetributionPaladin": 999, "UnholyDK": 997, "FeralDruid": 995, "SurvivalHunter": 998, "EnhancementShaman": 996, "FuryWarrior": 998, "ArmsWarrior": 998},
    # Dying Curse
    40255: {"BalanceDruid": 1000, "ArcaneMage": 1995, "ShadowPriest": 1996, "ElementalShaman": 2998, "AfflictionWarlock": 1993, "RestorationDruid": 992, "EnhancementShaman": 999, "FireMage": 1997},
    # Illustration of the Dragon Soul
    40432: {"BalanceDruid": 999, "ShadowPriest": 1995, "ElementalShaman": 999, "AfflictionWarlock": 2996, "RestorationDruid": 1998, "ArcaneMage": 1996, "DisciplinePriest": 3998, "RestorationShaman": 3991, "FireMage": 1996},
    40682: {"BalanceDruid": 998, "ArcaneMage": 997, "ShadowPriest": 1993, "ElementalShaman": 997, "AfflictionWarlock": 997, "FireMage": 997},
    40373: {"BalanceDruid": 996, "ShadowPriest": 994},
    37873: {"BalanceDruid": 995, "ShadowPriest": 996, "ElementalShaman": 996},
    42395: {"BalanceDruid": 994, "ShadowPriest": 993, "ElementalShaman": 995},
    49076: {"BalanceDruid": 993, "ArcaneMage": 996, "AfflictionWarlock": 996, "FireMage": 996},
    37835: {"BalanceDruid": 992, "RestorationDruid": 996, "DisciplinePriest": 994, "RestorationShaman": 994},
    42988: {"BalanceDruid": 991, "RestorationDruid": 995, "DisciplinePriest": 995},
    37660: {"BalanceDruid": 990, "DisciplinePriest": 991},
    44322: {"BalanceDruid": 1988, "RestorationDruid": 997},
    36972: {"BalanceDruid": 988},
    # Darkmoon Card: Greatness(+str)
    42987: {"FeralDruid": 1996, "RetributionPaladin": 3996, "FuryWarrior": 2000, "UnholyDK": 3994, "ProtectionPaladin": 3991, "ArmsWarrior": 2000},
    # Embrace of the Spider
    39229: {"ArcaneMage": 1000, "BalanceDruid": 997, "ShadowPriest": 1994, "ElementalShaman": 998, "RestorationShaman": 998, "AfflictionWarlock": 2994, "FireMage": 998},
    # Figurine - Monarch Crab
    44063: {"ProtectionPaladin": 1998, "ProtectionWarrior": 1998, "ProtectionDK": 1000},
    # Essence of Gossamer
    37220: {"ProtectionPaladin": 1997, "TankDruid": 999, "ProtectionWarrior": 997},
    # Darkmoon Card: Greatness(+agi)
    44253: {"AssassinationRogue": 999, "TankDruid": 1000, "SurvivalHunter": 3996, "EnhancementShaman": 997, "ProtectionWarrior": 998, "FeralDruid": 1994},
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
    37111: {"RestorationDruid": 3995, "HolyPaladin": 3999, "RestorationShaman": 1998},
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
    44255: {"HolyPaladin": 3996, "DisciplinePriest": 3992},
    42413: {"HolyPaladin": 1997, "DisciplinePriest": 998},
    28823: {"HolyPaladin": 997},
    29387: {"ProtectionPaladin": 995},
    40372: {"ProtectionPaladin": 992},
    42132: {"DisciplinePriest": 999},
    40382: {"DisciplinePriest": 997, "RestorationShaman": 995},
    40685: {"DisciplinePriest": 992, "RestorationShaman": 997},
    37657: {"DisciplinePriest": 990, "RestorationDruid": 1989},
    37844: {"RestorationShaman": 992},

    # P2
    45466: {"BalanceDruid": 2000, "ShadowPriest": 3995, "ArcaneMage": 1999, "ElementalShaman": 1998, "RestorationShaman": 3996, "AfflictionWarlock": 3996, "FireMage": 2998},
    45518: {"BalanceDruid": 3994, "ShadowPriest": 3998, "ElementalShaman": 3996, "ArcaneMage": 3996, "AfflictionWarlock": 3994, "FireMage": 3996},
    45931: {"FeralDruid": 3000, "SurvivalHunter": 3992, "AssassinationRogue": 3987, "EnhancementShaman": 1996, "ArmsWarrior": 1999, "FuryWarrior": 1999, "CombatRogue": 3990},
    45609: {"FeralDruid": 3993, "UnholyDK": 3997, "AssassinationRogue": 3994, "SurvivalHunter": 1997, "RetributionPaladin": 3995, "EnhancementShaman": 3994, "ArmsWarrior": 3996, "FuryWarrior": 3996, "CombatRogue": 3997},
    45158: {"TankDruid": 3993, "ProtectionPaladin": 3995, "ProtectionWarrior": 3997, "ProtectionDK": 2998},
    46021: {"TankDruid": 1999, "ProtectionPaladin": 3994, "ProtectionWarrior": 2995, "ProtectionDK": 2997},
    45522: {"RetributionPaladin": 1996, "UnholyDK": 1994, "FeralDruid": 1993, "ProtectionPaladin": 1991, "AssassinationRogue": 3989, "EnhancementShaman": 1997, "CombatRogue": 3988},
    46038: {"AssassinationRogue": 3990, "UnholyDK": 1995, "FeralDruid": 2996, "SurvivalHunter": 3993, "RetributionPaladin": 3993, "EnhancementShaman": 3991, "ArmsWarrior": 1997, "FuryWarrior": 1997, "CombatRogue": 3989},
    45490: {"BalanceDruid": 1998, "RestorationDruid": 2996, "ArcaneMage": 1998, "ShadowPriest": 2996, "RestorationShaman": 3994, "AfflictionWarlock": 1997},
    45308: {"BalanceDruid": 1997, "DisciplinePriest": 1998, "ElementalShaman": 1997, "RestorationShaman": 3992, "AfflictionWarlock": 2993, "ArcaneMage": 1997, "ShadowPriest": 2995, "FireMage": 2997},
    45263: {"UnholyDK": 1996, "FeralDruid": 1995, "SurvivalHunter": 1996, "RetributionPaladin": 3992, "AssassinationRogue": 1995, "EnhancementShaman": 1998},
    45286: {"UnholyDK": 1993, "ProtectionPaladin": 1990, "RetributionPaladin": 1995, "AssassinationRogue": 2993},
    45703: {"RestorationDruid": 3994, "DisciplinePriest": 3991},
    45535: {"RestorationDruid": 3995, "DisciplinePriest": 3994, "ShadowPriest": 1992, "RestorationShaman": 3997},
    45929: {"RestorationDruid": 1997, "DisciplinePriest": 1997, "ShadowPriest": 1991, "RestorationShaman": 3993},
    46051: {"RestorationDruid": 3996, "HolyPaladin": 4000, "DisciplinePriest": 3993},
    40430: {"RestorationDruid": 1994},
    19288: {"RestorationDruid": 1993},
    45292: {"RestorationDruid": 1992},
    45148: {"ArcaneMage": 1996, "ShadowPriest": 1998, "AfflictionWarlock": 2992, "FireMage": 1995},
    45313: {"ProtectionPaladin": 1995, "ProtectionWarrior": 1997},
    45507: {"ProtectionPaladin": 1994},
    46132: {"ShadowPriest": 1997},
    45866: {"AfflictionWarlock": 1994},

    # P3
    47464: {"UnholyDK": 3999, "FeralDruid": 3997, "TankDruid": 2999, "SurvivalHunter": 3999, "ProtectionPaladin": 3993, "RetributionPaladin": 3999, "AssassinationRogue": 3992, "ArmsWarrior": 3997, "FuryWarrior": 3997, "CombatRogue": 3996},
    47131: {"UnholyDK": 3999, "FeralDruid": 3997, "TankDruid": 2999, "SurvivalHunter": 3999, "ProtectionPaladin": 3993, "RetributionPaladin": 3999, "AssassinationRogue": 3992, "ArmsWarrior": 3997, "FuryWarrior": 3997, "CombatRogue": 3996},
    47303: {"UnholyDK": 3998, "FeralDruid": 3994, "SurvivalHunter": 2998, "ProtectionPaladin": 3992, "AssassinationRogue": 3991, "CombatRogue": 3991},
    47115: {"UnholyDK": 3998, "FeralDruid": 3994, "SurvivalHunter": 2998, "ProtectionPaladin": 3992, "AssassinationRogue": 3991, "CombatRogue": 3991},
    47088: {"ProtectionDK": 3998, "TankDruid": 4000, "ProtectionPaladin": 3999, "ProtectionWarrior": 3998},
    47451: {"ProtectionDK": 3998, "TankDruid": 4000, "ProtectionPaladin": 3999, "ProtectionWarrior": 3998},
    47080: {"ProtectionDK": 2999, "ProtectionPaladin": 3995, "ProtectionWarrior": 2999, "TankDruid": 3998},
    47290: {"ProtectionDK": 2999, "ProtectionPaladin": 3995, "ProtectionWarrior": 2999, "TankDruid": 3998},
    47735: {"ProtectionDK": 2996, "TankDruid": 2997, "ProtectionPaladin": 2995, "ProtectionWarrior": 3995},
    47477: {"BalanceDruid": 3997, "ArcaneMage": 3999, "ShadowPriest": 3993, "ElementalShaman": 3997, "EnhancementShaman": 3995, "AfflictionWarlock": 3993, "FireMage": 3997},
    47188: {"BalanceDruid": 3997, "ArcaneMage": 3999, "ShadowPriest": 3993, "ElementalShaman": 3997, "EnhancementShaman": 3995, "AfflictionWarlock": 3993, "FireMage": 3997},
    47316: {"BalanceDruid": 2998, "ShadowPriest": 2998, "AfflictionWarlock": 3991, "ArcaneMage": 3998, "FireMage": 3995, "ElementalShaman": 3995, "EnhancementShaman": 3993},
    47182: {"BalanceDruid": 2998, "ShadowPriest": 2998, "AfflictionWarlock": 3991, "ArcaneMage": 3998, "FireMage": 3995, "ElementalShaman": 3995, "EnhancementShaman": 3993},
    47261: {"TankDruid": 2996},
    47059: {"BalanceDruid": 4000, "DisciplinePriest": 3999, "RestorationShaman": 3999, "AfflictionWarlock": 2991},
    47432: {"BalanceDruid": 4000, "DisciplinePriest": 3999, "RestorationShaman": 3999, "AfflictionWarlock": 2991},
    48724: {"BalanceDruid": 2995, "HolyPaladin": 3998},
    47216: {"ProtectionPaladin": 2996, "ProtectionWarrior": 2996},
    47213: {"ShadowPriest": 2995, "AfflictionWarlock": 2995},
    47734: {"AssassinationRogue": 3988, "FeralDruid": 3996, "CombatRogue": 3987},
    47948: {"AssassinationRogue": 2991},
    48020: {"AssassinationRogue": 2991},
    47725: {"AssassinationRogue": 2990},
    47881: {"AssassinationRogue": 2990},
    47214: {"AssassinationRogue": 2989},
    48722: {"AfflictionWarlock": 2990, "FeralDruid": 3996},
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
    40705: {"HolyPaladin": 4000},
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
    40709: {"RestorationShaman": 3999},
    38368: {"RestorationShaman": 999},

    # P3
    # Sigils for Unholy Death Knight DPS Phase 3
    47673: {"UnholyDK": 3999},
    # Relics for Blood Death Knight Tanks in Phase 3
    47672: {"ProtectionDK": 3000},
    # Idols for Balance Druid DPS Phase 3
    47670: {"BalanceDruid": 1000},
    # Idols for Feral Druid DPS Phase 3
    47668: {"FeralDruid": 3000, "TankDruid": 2998},
    # Idols for Feral Druid Tank Phase 3
    # Idols for Restoration Druid Healer Phase 3
    47671: {"RestorationDruid": 2999},
    # Librams for Holy Paladin Healer Phase 3
    # Librams for Protection Paladin Tank Phase 3
    47664: {"ProtectionPaladin": 3998},
    47661: {"ProtectionPaladin": 4000, "RetributionPaladin": 3000},
    # Librams for Retribution Paladin
    42854: {"RetributionPaladin": 2999},
    # Totems for Elemental Shaman DPS in Phase 3
    47666: {"ElementalShaman": 3000, "EnhancementShaman": 3000},
    # Totems for Enhancement Shaman DPS in Phase 3
    # Totems for Restoration Shaman Healer in Phase 3
    47665: {"RestorationShaman": 4000},

    # P4
    # Trinket options for Blood Death Knight Tanks in Phase 4
    50364: {"ProtectionDK": 4000, "TankDruid": 3999, "ProtectionPaladin": 4000, "ProtectionWarrior": 4000},
    50344: {"ProtectionDK": 3999, "TankDruid": 3996, "ProtectionPaladin": 3996, "ProtectionWarrior": 3999},
    50356: {"ProtectionDK": 3997, "TankDruid": 3995, "ProtectionPaladin": 3997, "ProtectionWarrior": 3996},
    # Sigil options for Blood Death Knight Tanks in Phase 4
    50462: {"ProtectionDK": 4000},
    # Trinkets for Unholy Death Knight DPS Phase 4
    50363: {"UnholyDK": 4000, "SurvivalHunter": 4000, "CombatRogue": 4000, "EnhancementShaman": 4000, "ArmsWarrior": 4000, "FuryWarrior": 4000, "FeralDruid": 4000, "RetributionPaladin": 3997, "AssassinationRogue": 4000},
    50343: {"UnholyDK": 3996, "FeralDruid": 3998, "SurvivalHunter": 3997, "RetributionPaladin": 3998, "AssassinationRogue": 3998, "CombatRogue": 3999, "EnhancementShaman": 3999, "ArmsWarrior": 3998, "FuryWarrior": 3998},
    50355: {"UnholyDK": 3995, "FeralDruid": 3994, "SurvivalHunter": 3995, "AssassinationRogue": 3997, "CombatRogue": 3995, "EnhancementShaman": 3996},
    # Sigils for Unholy Death Knight DPS Phase 4
    50459: {"UnholyDK": 4000},
    # Trinkets for Balance Druid DPS Phase 4
    50348: {"BalanceDruid": 4000, "ArcaneMage": 4000, "FireMage": 4000, "ShadowPriest": 3999, "ElementalShaman": 4000, "AfflictionWarlock": 3999},
    50365: {"BalanceDruid": 3999, "FireMage": 3999, "ShadowPriest": 4000, "ElementalShaman": 3999, "EnhancementShaman": 3998, "AfflictionWarlock": 4000},
    50360: {"BalanceDruid": 3998, "AfflictionWarlock": 3998},
    50353: {"BalanceDruid": 3996, "AfflictionWarlock": 3997},
    50345: {"BalanceDruid": 3995, "ArcaneMage": 3997, "FireMage": 3998, "ShadowPriest": 3997, "ElementalShaman": 3998, "AfflictionWarlock": 3995},
    # Idols for Balance Druid DPS Phase 4
    50457: {"BalanceDruid": 4000},
    # Trinkets for Feral Druid DPS Phase 4
    50362: {"FeralDruid": 3999, "SurvivalHunter": 3998, "AssassinationRogue": 3995, "CombatRogue": 3998, "ArmsWarrior": 3999, "FuryWarrior": 3999},
    50342: {"FeralDruid": 3995, "AssassinationRogue": 3993, "CombatRogue": 3994},
    # Idols for Feral Druid DPS Phase 4
    50456: {"FeralDruid": 4000, "TankDruid": 4000},
    # Trinkets for Feral Druid Tank Phase 4
    50361: {"TankDruid": 3997, "ProtectionPaladin": 3998},
    50341: {"TankDruid": 3993},
    # Idols for Feral Druid Tank Phase 4
    # Trinkets for Restoration Druid Healer Phase 4
    50366: {"RestorationDruid": 3999, "DisciplinePriest": 4000, "RestorationShaman": 4000},
    50358: {"RestorationDruid": 3998, "DisciplinePriest": 3995},
    50346: {"RestorationDruid": 3997, "DisciplinePriest": 3996},
    # Idols for Restoration Druid Healer Phase 4
    50454: {"RestorationDruid": 4000},
    # Trinkets for Survival Hunter DPS Phase 4
    # Trinkets for Arcane Mage DPS Phase 4
    # Rings for Fire Mage DPS Phase 4
    50398: {"FireMage": 4000},
    50664: {"FireMage": 3999},
    50614: {"FireMage": 3998},
    50644: {"FireMage": 3997},
    50714: {"FireMage": 3996},
    50636: {"FireMage": 3995},
    51849: {"FireMage": 3994},
    47489: {"FireMage": 3993},
    47237: {"FireMage": 3993},
    45495: {"FireMage": 3992},
    46046: {"FireMage": 3991},
    47372: {"FireMage": 3990},
    47054: {"FireMage": 3990},
    # Trinkets for Fire Mage DPS Phase 4
    # Trinkets for Holy Paladin Healer Phase 4
    # Librams for Holy Paladin Healer Phase 4
    47662: {"HolyPaladin": 3999},
    # Trinkets for Protection Paladin Tank Phase 4
    50706: {"ProtectionPaladin": 3993, "RetributionPaladin": 4000, "AssassinationRogue": 3999, "CombatRogue": 3993},
    # Librams for Protection Paladin Tank Phase 4
    50461: {"ProtectionPaladin": 3999},
    # Trinkets for Retribution Paladin Phase 4
    # Libram
    50455: {"RetributionPaladin": 4000},
    # Trinkets for Discipline Priest Healer Phase 4
    47041: {"DisciplinePriest": 3997, "RestorationShaman": 3998},
    47271: {"DisciplinePriest": 3997, "RestorationShaman": 3998},
    # Trinkets for Shadow Priest DPS Phase 4
    50259: {"ShadowPriest": 3996, "AfflictionWarlock": 3990},
    50357: {"ShadowPriest": 3994, "EnhancementShaman": 3997},
    # Trinkets for Assassination Rogue DPS Phase 4
    50351: {"AssassinationRogue": 3996, "CombatRogue": 3992},
    # Trinkets for Combat Rogue DPS Phase 4
    # Trinket for Elemental Shaman DPS in Phase 4
    # Totems for Elemental Shaman DPS in Phase 4
    50458: {"ElementalShaman": 4000, "EnhancementShaman": 4000},
    # Trinket for Enhancement Shaman DPS in Phase 4
    # Totems for Enhancement Shaman DPS in Phase 4
    # Trinket for Restoration Shaman Healer in Phase 4
    # Totems for Restoration Shaman Healer in Phase 4
    50375: {"AfflictionWarlock": 3992},
    # Trinkets for Arms Warrior DPS in Phase 4
    # Trinkets for Fury Warrior DPS in Phase 4
    # Trinkets for Protection Warrior Tank in Phase 4
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

            if itemid in blacklist \
                or 51440 <= itemid <= 51448 \
                or 51516 <= itemid <= 51529 \
                or 57682 <= itemid <= 57754 \
                or 58504 <= itemid <= 58778 \
                or 61635 <= itemid <= 61919 \
                or 69255 <= itemid <= 69263:
                continue

            item_tmp = {}
            #print("id = %s" % item["id"])
            #print("subclass = %s" % item["subclass"])
            #print("inventorySlot = %s" % item["inventorySlot"])
            for i in {'dk_unholy', 'dk_blood', 'dk_frost', 'druid_balance', 'druid_feral', 'druid_restoration', 'druid_guardian', 'hunter_survival', 'hunter_beastmastery', 'hunter_marksmanship', 'mage_arcane', 'mage_fire', 'mage_frost', 'paladin_holy', 'paladin_protection', 'paladin_retribution', 'priest_discipline', 'priest_shadow', 'priest_holy', 'rogue_assassination', 'rogue_combat', 'rogue_subtlety', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_affliction', 'warlock_demonology', 'warlock_destruction', 'warrior_arms', 'warrior_fury', 'warrior_protection'}:
                score = item[i]

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
                    if int(item["subclass"]) == -5 and int(item["class"]["@id"]) == 4:
                        itemclass = "Weapon"
                        itemtype = "OffHand"
                        itemsubclass = "OffHand"

                    #else:
                    #    print("Invalid subclass id: %s - type = %s, class = %s, subclass = %s" % (itemid, item["inventorySlot"]["@id"], item["class"]["@id"], item["subclass"]))
                except Exception as err:
                    print(f"Unexpected {err=}, {type(err)=}")
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

                if itemclass == "Armor" and itemtype not in ["Back", "Finger", "Neck", "Trinket"]:
                    if cclass in ["Mage", "Priest", "Warlock"]:
                        if itemsubclass not in ["Cloth"]:
                            continue
                    if cclass in ["Rogue", "Druid"]:
                        if itemsubclass not in ["Leather"]:
                            continue
                    if cclass in ["Hunter", "Shaman"]:
                        if itemsubclass not in ["Mail"]:
                            continue
                    if cclass in ["Paladin", "Warrior", "DK"]:
                        if itemsubclass not in ["Plate"]:
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
                        if itemsubclass in ["Sword", "Axe"]:
                            continue
                    if cclass in ["Hunter"]:
                        if itemsubclass in ["Mace"]:
                            continue

                if itemtype in ["MainHand", "OneHand", "OffHand", "TwoHand"]:
                    if cclass in ["Rogue", "Druid"]:
                        if itemsubclass in ["Axe"] and cclass in ["Druid"]:
                            continue
                        if itemsubclass in ["Sword"] and cclass in ["Druid"]:
                            continue
                        if spec in ["Assassination"] and itemsubclass not in ["Dagger"]:
                            continue
                        if spec in ["Combat"] and itemsubclass in ["Dagger"]:
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

                #if itemid == 60470:
                #    print("%s" % (item.keys()))
                if "mleatkpwr" in item or "agi" in item or "str" in item:
                    if cclass in ["Priest", "Mage", "Warlock"]:
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
                    if cclass in ["Hunter"]:
                        if itemsubclass in ["Thrown"]:
                            continue

                # For Warrior, Paladin, and DK
                if spec == "Protection" and itemclass == "Armor":
                        if itemsubclass in ["Cloth", "Leather", "Mail"]:
                            continue

                if spec == "Protection" and "dodgertng" not in item and "parryrtng" not in item and "blockrtng" not in item:
                    if itemclass == "Armor" and itemtype not in ["Amulet", "Trinket", "Ranged"]:
                        continue
                    # Only Warrior's weapon requires those attributes
                    if itemclass == "Weapon" and itemsubclass not in ["Gun", "Bow", "Crossbow", "Thrown"] and cclass == "Warrior":
                        continue
                    if itemclass == "Weapon" and cclass == "Paladin" and "agi" in item:
                        score = score + int(item["agi"])

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
                #if itemid in [61472]:
                    #print("%s %s %s %s %s" % (spec, cclass, itemid, score, phase))
                    #print("after %s %s" % (itemid, score))

    #print(list(bis_list["Warrior"]["Fury"]["1"]))
    return bis_list

bis_list = build_list()

for cclass in classs.values():
    for spec in bis_list[cclass].keys():
        print("%s - %s" % (cclass, spec))
        output = ""
        for phase in ["0", "1"]:   # select items from P0 to P5
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
                        if cclass == "Shaman":
                            if spec == "Enhancement":
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
