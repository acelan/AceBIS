from bs4 import BeautifulSoup
import importlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define phases in order of priority (highest to lowest)
PHASES = ["p4", "p3", "p1", "p0"]

# Define class and specialization mappings
CLASS_SPECS = {
    "dk": ["blood", "frost", "unholy"],
    "druid": ["balance", "feral", "guardian", "restoration"],
    "hunter": ["beastmastery", "marksmanship", "survival"],
    "mage": ["arcane", "fire", "frost"],
    "paladin": ["holy", "protection", "retribution"],
    "priest": ["discipline", "holy", "shadow"],
    "rogue": ["assassination", "combat", "subtlety"],
    "shaman": ["elemental", "enhancement", "restoration"],
    "warlock": ["affliction", "demonology", "destruction"],
    "warrior": ["arms", "fury", "protection"]
}

def get_trinket_data():
    """
    Dynamically imports class modules and retrieves trinket data for all phases.

    Returns:
        dict: A dictionary mapping class_spec to a list of trinket data for each phase
    """
    trinkets = {}

    # Import all class modules
    modules = {}
    for class_name in CLASS_SPECS:
        try:
            modules[class_name] = importlib.import_module(f"trinkets.{class_name}")
            logger.info(f"Successfully imported module: trinkets.{class_name}")
        except ImportError as e:
            logger.error(f"Failed to import module trinkets.{class_name}: {e}")
            continue

    # Create trinket dictionary
    for class_name, specs in CLASS_SPECS.items():
        if class_name not in modules:
            continue

        for spec in specs:
            class_spec = f"{class_name}_{spec}"
            trinkets[class_spec] = []

            # Add data for each phase in order
            for phase in PHASES:
                attr_name = f"{spec}_{phase}"
                if hasattr(modules[class_name], attr_name):
                    phase_data = getattr(modules[class_name], attr_name)
                    trinkets[class_spec].append(phase_data)
                    logger.debug(f"Added {attr_name} data for {class_spec}")
                else:
                    logger.warning(f"No {phase} data found for {class_spec}")

    return trinkets

def parse_trinkets(trinkets):
    """
    Parse trinket data and assign scores based on priority.

    Args:
        trinkets (dict): Dictionary of trinket data by class_spec

    Returns:
        dict: Dictionary of scored trinkets by class_spec
    """
    scored_trinkets = {class_spec: {} for class_spec in trinkets.keys()}

    for class_spec, phase_trinkets in trinkets.items():
        score = 10000

        for phase_data in phase_trinkets:
            try:
                soup = BeautifulSoup(phase_data, 'html.parser')

                for trinket_link in soup.find_all('a'):
                    href = trinket_link.get('href')
                    if href and 'item=' in href:
                        try:
                            item_id = href.split('item=')[1].split('/')[0]

                            # Only add item if it hasn't been added before
                            if item_id not in scored_trinkets[class_spec]:
                                scored_trinkets[class_spec][item_id] = score
                                score -= 1
                        except IndexError:
                            logger.warning(f"Failed to extract item ID from {href}")
            except Exception as e:
                logger.error(f"Error parsing trinket data for {class_spec}: {e}")

    return scored_trinkets

def output_trinkets(scored_trinkets):
    """
    Output scored trinkets in the required format.

    Args:
        scored_trinkets (dict): Dictionary of scored trinkets by class_spec
    """
    for class_spec, items in sorted(scored_trinkets.items()):
        print(f"\"{class_spec}\": {{")
        for item_id, score in sorted(items.items(), key=lambda x: -x[1]):
            print(f"    {item_id}: {score},")
        print("},")

def main():
    """Main function to orchestrate the trinket parsing process."""
    trinkets = get_trinket_data()
    scored_trinkets = parse_trinkets(trinkets)
    output_trinkets(scored_trinkets)

if __name__ == "__main__":
    main()
