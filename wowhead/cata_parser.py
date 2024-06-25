import argparse
import os
import os.path
import re
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process presets.ts in a given folder and its subfolders.")
    parser.add_argument("folder", type=str, help="The folder of wowsim cata")
    return parser.parse_args()

def list_files_in_folder(folder):
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f == "presets.ts"]:
            files.append(os.path.join(dirpath, filename))
    return files

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'w') as file:
        return file.write(content)

def convert_key(key):
    match key:
        case "StatStrength":
            return "str"
        case "StatAgility":
            return "agi"
        case "StatStamina":
            return "sta"
        case "StatIntellect":
            return "int"
        case "StatSpirit":
            return "spi"
        case "StatSpellPower":
            return "spldmg"
        case "StatMP5":
            return "manargn"
        case "StatSpellHit":
            return "hitrtng"
        case "StatSpellCrit":
            return "critstrkrtng"
        case "StatSpellHaste":
            return "hastertng"
        #case "StatSpellPenetration":
        #    return ""
        case "StatAttackPower":
            return "mleatkpwr"
        case "StatMeleeHit":
            return "hitrtng"
        case "StatMastery":
            return "mastrtng"
        case "StatMeleeCrit":
            return "critstrkrtng"
        case "StatMeleeHaste":
            return "hastertng"
        case "StatExpertise":
            return "exprtng"
        #case "StatMana":
        #    return ""
        case "StatArmor":
            return "armor"
        case "StatRangedAttackPower":
            return "rgdatkpwr"
        case "StatBlock":
            return "blockrtng"
        case "StatDodge":
            return "dodgertng"
        case "StatParry":
            return "parryrtng"
        case "StatResilience":
            return "resirtng"
        #case "StatHealth":
        #    return ""
        case "PseudoStatMainHandDps":
            return "mledps"
        case "PseudoStatOffHandDps":
            return "mledps"
        case "PseudoStatRangedDps":
            return "rgddps"
        case _:
            print(f"Unknown key: {key}")
            return key

def stripcomments(text):
    return re.sub(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', '', text, flags=re.S)

def extract_stats(content):
    stats_array = {}
    for line in content.split('\n'):
        if "Stat.Stat" in line:
            line = line.replace('[', '').replace(']', '').replace('Stat.', '').replace('PseudoStat.', '').replace(',','')
            line = line.split(":")

            key = line[0].strip()
            key = convert_key(key)
            value = line[1].strip()
            value = stripcomments(value)
            stats_array[key] = value
    return stats_array

def parse_stats_from_file(filename):
    content = read_file(filename)
    stats_array = extract_stats(content)
    
    return stats_array

def main():
    args = parse_arguments()
    folder = args.folder

    files = list_files_in_folder(folder)

    for file in files:
        try:
            stats_instance = parse_stats_from_file(file)
            if not stats_instance:
                continue

            spec = file.split('/')[-2]
            cclass = file.split('/')[-3]
            if cclass == "death_knight":
                cclass = "dk"
            if spec == "beast_mastery":
                spec = "beastmastery"

            filename = f"classes/{cclass}_{spec}.py"
            content = f"{cclass}_{spec} = " + json.dumps(stats_instance, indent=4) + '\n'
            write_file(filename, content)
            #print(f"Parsed {cclass}_{spec}\n\t{stats_instance}")
        except Exception as e:
            print(f"Failed to parse {file}: {e}")

if __name__ == '__main__':
    main()

