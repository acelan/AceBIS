from bs4 import BeautifulSoup
import json
from trinkets import dk
from trinkets import druid
from trinkets import hunter
from trinkets import mage
from trinkets import paladin
from trinkets import priest
from trinkets import rogue
from trinkets import shaman
from trinkets import warlock
from trinkets import warrior

trinkets = {
        "dk_blood": [dk.blood_p3, dk.blood_p1, dk.blood_p0],
        "dk_frost": [dk.frost_p3, dk.frost_p1, dk.frost_p0],
        "dk_unholy": [dk.unholy_p3, dk.unholy_p1, dk.unholy_p0],
        "druid_balance": [druid.balance_p3, druid.balance_p1, druid.balance_p0],
        "druid_feral": [druid.feral_p3, druid.feral_p1, druid.feral_p0],
        "druid_guardian": [druid.guardian_p3, druid.guardian_p1, druid.guardian_p0],
        "druid_restoration": [druid.restoration_p3, druid.restoration_p1, druid.restoration_p0],
        "hunter_beastmastery": [hunter.beastmastery_p3, hunter.beastmastery_p1, hunter.beastmastery_p0],
        "hunter_marksmanship": [hunter.marksmanship_p3, hunter.marksmanship_p1, hunter.marksmanship_p0],
        "hunter_survival": [hunter.survival_p3, hunter.survival_p1, hunter.survival_p0],
        "mage_arcane": [mage.arcane_p3, mage.arcane_p1, mage.arcane_p0],
        "mage_fire": [mage.fire_p3, mage.fire_p1, mage.fire_p0],
        "mage_frost": [mage.frost_p3, mage.frost_p1, mage.frost_p0],
        "paladin_holy": [paladin.holy_p3, paladin.holy_p1, paladin.holy_p0],
        "paladin_protection": [paladin.protection_p3, paladin.protection_p1, paladin.protection_p0],
        "paladin_retribution": [paladin.retribution_p3, paladin.retribution_p1, paladin.retribution_p0],
        "priest_discipline": [priest.discipline_p3, priest.discipline_p1, priest.discipline_p0],
        "priest_holy": [priest.holy_p3, priest.holy_p1, priest.holy_p0],
        "priest_shadow": [priest.shadow_p3, priest.shadow_p1, priest.shadow_p0],
        "rogue_assassination": [rogue.assassination_p3, rogue.assassination_p1, rogue.assassination_p0],
        "rogue_combat": [rogue.combat_p3, rogue.combat_p1, rogue.combat_p0],
        "rogue_subtlety": [rogue.subtlety_p3, rogue.subtlety_p1, rogue.subtlety_p0],
        "shaman_elemental": [shaman.elemental_p3, shaman.elemental_p1, shaman.elemental_p0],
        "shaman_enhancement": [shaman.enhancement_p3, shaman.enhancement_p1, shaman.enhancement_p0],
        "shaman_restoration": [shaman.restoration_p3, shaman.restoration_p1, shaman.restoration_p0],
        "warlock_affliction": [warlock.affliction_p3, warlock.affliction_p1, warlock.affliction_p0],
        "warlock_demonology": [warlock.demonology_p3, warlock.demonology_p1, warlock.demonology_p0],
        "warlock_destruction": [warlock.destruction_p3, warlock.destruction_p1, warlock.destruction_p0],
        "warrior_arms": [warrior.arms_p3, warrior.arms_p1, warrior.arms_p0],
        "warrior_fury": [warrior.fury_p3, warrior.fury_p1, warrior.fury_p0],
        "warrior_protection": [warrior.protection_p3, warrior.protection_p1, warrior.protection_p0],
        }

scored_trickets = {class_spec: {} for class_spec in trinkets.keys()}

for class_spec, ptrinkets in trinkets.items():
    score = 10000
    for phase_trinket in ptrinkets:
        soup = BeautifulSoup(phase_trinket, 'html.parser')
        for phase_trinket in soup.find_all('a'):
            href = phase_trinket.get('href')
            if href and 'item=' in href:
                item_id = href.split('item=')[1].split('/')[0]
                if item_id not in scored_trickets[class_spec]:
                    scored_trickets[class_spec][item_id] = score
                    score -= 1

for class_spec, strinkets in scored_trickets.items():
    print("\"%s\": {" % class_spec)
    for itemid, score in strinkets.items():
        print(f"    {itemid}: {score},")
    print("},")
