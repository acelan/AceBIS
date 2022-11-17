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
    54592,
    54848,
}

# items do not exist in current phase, need to check them later
invalid = {
34243, 
35639,
44901,
35732,
35061,
44742,
35029,
41148,
44695,
40930,
41149,
37062,
43800,
35044,
43280,
40931,
41150,
39628, 
43763, 
41160, 
42726, 
44296, 
40932, 
40936, 
39602, 
35045, 
37717, 
42728, 
40571, 
40937, 
40521, 
41162, 
34167, 
35185, 
41320, 
35030, 
35185, 
35079, 
41198, 
44345, 
43870, 
41319, 
35062, 
43870, 
41010, 
43776, 
35678, 
41388, 
41269, 
41297, 
44741, 
46218, 
41388, 
35050, 
39603, 
41126, 
44046, 
40461, 
41296, 
38445, 
45371, 
44046, 
41011, 
40522, 
44677, 
37182, 
42730, 
39531, 
41270, 
35184, 
40938, 
40975, 
37182, 
41016, 
41023, 
40363, 
44949, 
43405, 
35023, 
35024, 
44671, 
43455, 
43163, 
40973, 
44949, 
44740, 
41012, 
35080, 
44123, 
44369, 
39760, 
43588, 
35112, 
35113, 
43162, 
37857, 
44123, 
44369, 
39760, 
37056, 
44676, 
44732, 
45412, 
35051,
44239,
44691,
44411,
35603,

43749,
43755,
43456,
34402,

41346,
40982,
46220,
35145,

44170,
44440,
41025,
34567,
34402,
39293,
50332,
39260,
43176,

41324,
41301,
44669,
35672,
42766,
36986,

39293,

40972,
45372,
35140,
43261,
43271,
44669,

44904,
42766,
41030,
37650,
50331,
41350,
42767,

44906,
39539,

38444,
34355,
44030,
37155,
43798,
36977,
41350,

42767,
37149,
43201,

34439,
34355,

44445,
41026,
40310,
50330,
40442,

41394,
40462,
44696,
44907,
44442,
34383,
37777,
38390,
43595,

39630,
34432,
40818,
44894,


37616,
44696,

35620,
44442,
34383,
44368,
37592,
43451,
37362,
50329,
40817,
41128,

41302,
41624,
41325,
43273,
44305,
39679,
38389,
43592,

40572,
35175,
35090,
41128,

35577,
41624,
35183,
43273,
44305,

39679,
41017,
43273,
39174,
35604,
40298,

40320,
41303,
41332,
45346,
41620,
43495,
43452,
38388,
35650,

40838,
35170,
43795,
40320,

34384,
41332,
34245,
41620,
41031,
43452,

43132,
37244,
40837,
42723,
40293,
40313,

43760,
41264,
41326,
41331,
44443,
43264,
38387,
41049,

35091,
42723,

39640,
40313,
43161,
41264,
34403,
41331,
45416,
34438,
44110,
41049,
41347,
43864,
34345,
39369,

39546,
35665,
45350,
37640,
35619,
35615,
34356,
41054,

43802,
43864,

46215,
34559,
34169,
35665,
39240,
37640,
34186,
37138,
39240,

41054,
44667,

43816,
39235,
40292,
37632,

45347,
35180,
46313,
34571,
37818,
37724,
41154,
35147,

44667,
39641,
39235,

45382,
37632,
43991,
35180,
37180,
35641,
39191,
37724,

41018,
43502,
44667,
41112,

39626,
44197,
37237,
40592,

40468,
34445,
39545,
44892,
44436,

35177,
34992,
35143,
41112,

40842,
37288,
40821,
37847,

37083,
35169,
35182,
35150,
44122,
44258,
34332,
44896,

35004,
40673,
39175,
48945,
40443,
37590,
43812,
40745,
37389,
44339,
40467,
44891,
44344,
35173,
44045,
43173,
35097,
39178,
37240,
35638,
34560,

37389,
44339,
35033,
35139,
41032,
41047,
42555,
34565,

35005,
35010,
43353,
37787,
35572,
43160,

40567,
40332,
39625,
41348,
45353,
34446,
41675,
34572,
34993,
37771,
44410,
41073,

35174,
35572,
35100,
40583,
34433,
43311,
41348,

44194,
37771,
41644,
41633,
43770,

41059,
42554,
40749,
35174,
35572,
35013,
40295,
42768,
40674,
35181,
30912,

37066,
35176,

45336,
44361,
35000,
41638,
34999,
41634,
43202,
35172,
43447,
37105,
35635,
35168,
41943,
40846,
35176,

40581,
35148,
35034,
41638,
43403,
41634,
39595,
40739,
44905,
34566,

42002,
35168,
41990,
34357,
40671,
43203,
42093,
44674,
40290,
44673,
40841,
40735,
34354,
35146,
34385,
41639,
35634,
43700,
41202,
35166,
44109,
35142,
41956,
35179,
40758,
35144,
46223,
35178,
37793,
37712,
39177,
41639,
41829,
43700,
45403,
34437,
40340,
41074,
42093,
35179,
41984,
35144,
34381,
34400,
34568,
35654,
32525,
43585,
43313,
39680,
40820,
40755,
30903,
41664,
37000,
44908,
37070,
41844,
34333,
35136,
43448,
35654,
35679,
35138,
35673,
46222,
41844,
40825,
40755,
41645,
37000,
37767,
37070,
40285,
37069,
44248,
40270,

35654,
32525,
35138,
44343,
41345,
44040,

46335,
39676,
34405,
35596,
34170,

44038,
35670,
44031,
40204,

38591,
35171,
44044,
35141,
34443,
37188,
44360,
34168,

35682,
34405,
35657,
34170,
45384,
44037,
37188,

35600,
38591,
35171,
41670,
35141,
43771,
37365,
40304,
44897,

35682,
34405,
35657,
34170,
34382,
37135,
46334,
44016,
34847,
42760,
39176,

40274,
40565,
40187,
35637,

44342,
44367,
34404,
35137,
43444,
41155,
43443,
36992,
44016,
37294,
35149,
37189,
37221,
43444,
44902,
34561,
43286,
44367,
34353,
42762,
39589,
37634,
36948,
39189,
44016,
37684,
42760,
37189,
44240,
37633,
46331,
44366,
43971,
42096,
36976,
41354,
42552,
37150,
40845,
34188,
34444,
41676,
35659,
35640,
36971,
36999,
35585,
36945,
41944,
42096,
36976,
35676,
35640,
36971,
43174,
37768,
35579,
40291,
35659,
39217,
41063,
43768,
43996,
44366,
41991,
42096,
36976,
37688,
41116,
32521,
46329,
    32235,
    34180,
    34181,
    34244,
    34339,
    34340,
    34386,
    34401,
    34431,
    34436,
    34442,
    34447,
    34448,
    34564,
    34570,
    34573,
    34574,
    34575,
    35167,
    35593,
    35614,
    35695,
    36954,
    36969,
    36985,
    36996,
    37040,
    37068,
    37082,
    37113,
    37117,
    37167,
    37170,
    37175,
    37176,
    37183,
    37193,
    37217,
    37218,
    37245,
    37262,
    37263,
    37292,
    37293,
    37361,
    37366,
    37367,
    37369,
    37370,
    37374,
    37594,
    37613,
    37618,
    37620,
    37622,
    37629,
    37636,
    37644,
    37654,
    37656,
    37666,
    37668,
    37669,
    37675,
    37682,
    37695,
    37696,
    37715,
    37725,
    37726,
    37730,
    37731,
    37760,
    37766,
    37788,
    37791,
    37841,
    37849,
    37853,
    37854,
    37867,
    37870,
    37876,
    37884,
    37890,
    37891,
    38590,
    39139,
    39195,
    39196,
    39215,
    39224,
    39234,
    39236,
    39247,
    39254,
    39252,
    39258,
    39259,
    39263,
    39273,
    39278,
    39280,
    39283,
    39294,
    39295,
    39307,
    39309,
    39390,
    39395,
    39399,
    39403,
    39405,
    39408,
    39409,
    39467,
    39491,
    39493,
    39496,
    39498,
    39553,
    39555,
    39561,
    39564,
    39578,
    39580,
    39583,
    39594,
    39610,
    39612,
    39619,
    39620,
    39635,
    39636,
    39657,
    39678,
    39701,
    39702,
    39706,
    39717,
    39720,
    39722,
    39723,
    39729,
    39731,
    39732,
    39734,
    39764,
    39765,
    39761,
    39765,
    39768,
    40060,
    40184,
    40186,
    40196,
    40197,
    40198,
    40201,
    40206,
    40209,
    40235,
    40236,
    40237,
    40240,
    40243,
    40246,
    40247,
    40269,
    40282,
    40287,
    40294,
    40296,
    40297,
    40306,
    40307,
    40318,
    40323,
    40324,
    40325,
    40326,
    40328,
    40329,
    40330,
    40331,
    40333,
    40338,
    40339,
    40342,
    40344,
    40352,
    40366,
    40367,
    40376,
    40379,
    40397,
    40398,
    40409,
    40416,
    40417,
    40420,
    40421,
    40422,
    40428,
    40446,
    40451,
    40473,
    40490,
    40493,
    40499,
    40500,
    40505,
    40506,
    40510,
    40512,
    40516,
    40517,
    40519,
    40543,
    40546,
    40547,
    40549,
    40554,
    40556,
    40558,
    40560,
    40562,
    40576,
    40577,
    40589,
    40591,
    40733,
    40734,
    40736,
    40737,
    40738,
    40740,
    40741,
    40742,
    40743,
    40746,
    40747,
    40748,
    40750,
    40751,
    40757,
    40824,
    40878,
    40880,
    40887,
    40888,
    41064,
    41156,
    41190,
    41203,
    41204,
    41223,
    41224,
    41228,
    41229,
    41344,
    41355,
    41386,
    41387,
    41391,
    41392,
    41553,
    41555,
    41635,
    41653,
    41654,
    41665,
    41666,
    41671,
    41677,
    41828,
    41830,
    41835,
    41839,
    41878,
    41879,
    41884,
    41892,
    41901,
    41902,
    41907,
    41908,
    41945,
    41957,
    41958,
    41985,
    41992,
    42003,
    42004,
    42549,
    42550,
    42551,
    42553,
    42731,
    43131,
    43171,
    43172,
    43200,
    43256,
    43260,
    43312,
    43375,
    43402,
    43435,
    43438,
    43439,
    43458,
    43459,
    43469,
    43475,
    43500,
    43729,
    43730,
    43735,
    43736,
    43742,
    43745,
    43753,
    43756,
    43769,
    43777,
    43779,
    43787,
    43789,
    43801,
    43803,
    43815,
    43817,
    43970,
    43974,
    43975,
    43994,
    43995,
    44006,
    44007,
    44008,
    44011,
    44019,
    44021,
    44024,
    44036,
    44117,
    44179,
    44182,
    44200,
    44201,
    44202,
    44203,
    44205,
    44243,
    44247,
    44297,
    44306,
    44333,
    44338,
    44340,
    44341,
    44358,
    44359,
    44386,
    44408,
    44409,
    44412,
    44438,
    44859,
    44885,
    44893,
    44895,
    44898,
    44899,
    44900,
    44903,
    44909,
    44910,
    44930,
    44931,
    45338,
    45342,
    45343,
    45365,
    45367,
    45377,
    45379,
    45398,
    45399,
    45402,
    45408,
    45409,
    45417,
    45420,
    45425,
    45427,
    45499,
    46221,
    46224,
    46326,
    49126,
    49809,
    49811,
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
                for i in {'dk_unholy', 'druid_balance', 'druid_feral', 'hunter', 'mage_arcane', 'paladin_protection', 'paladin_retribution', 'priest_shadow', 'rogue', 'shaman_elemental', 'shaman_enhancement', 'shaman_restoration', 'warlock_afflication', 'warrior_arm', 'warrior_fury', 'warrior_protection'}:
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
                            if "mleatkpwr" in item:
                                continue
                        if cclass in ["Priest"]:
                            if itemsubclass in ["Axe", "Sword", "Fist"]:
                                continue
                            if "mleatkpwr" in item:
                                continue
                        if cclass in ["Shaman"]:
                            if itemsubclass in ["Sword"]:
                                continue
                        if cclass in ["Hunter"]:
                            if itemsubclass in ["Mace"]:
                                continue

                    if itemtype in ["OffHand"]:
                        if cclass in ["Priest", "Mage", "Warlock"]:
                            if itemsubclass in ["Axe", "Sword", "Mace", "Dagger", "Fist"]:
                                continue
                            if "mleatkpwr" in item:
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

    #print(list(bis_list["Warrior"]["Fury"]["1"]))
    return bis_list

bis_list = build_list()

for cclass in classs.values():
    for spec in bis_list[cclass].keys():
        print("%s - %s" % (cclass, spec))
        output = ""
        for phase in {"1"}:   # select items from P0 to P5
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
                    #if cclass == "Priest" and s == "Helm":
                    #    print("%s %s %s %s %s #%s" % (spec, cclass, itemid, items[itemid]["score"], p, index))
                    #print(output)
                    index += 1
                    if index > 15:
                        break
        write_file(spec + cclass, output)
