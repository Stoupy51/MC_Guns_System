
# Imports
from ..config.stats import DEAGLE, GLOCK17, GLOCK18, M9, M1911, MAKAROV, VZ61, add_item


# Main function should return a database
def main() -> None:

    # Add pistols
    add_item("m1911", stats=M1911, model_path="auto")
    add_item("m1911_zoom", stats=M1911, model_path="auto")
    add_item("m9", stats=M9, model_path="auto")
    add_item("m9_zoom", stats=M9, model_path="auto")
    add_item("deagle", stats=DEAGLE, model_path="auto")
    add_item("deagle_zoom", stats=DEAGLE, model_path="auto")
    add_item("deagle_4", stats=DEAGLE, model_path="auto")
    add_item("deagle_4_zoom", stats=DEAGLE, model_path="auto")
    add_item("makarov", stats=MAKAROV, model_path="auto")
    add_item("makarov_zoom", stats=MAKAROV, model_path="auto")
    add_item("glock17", stats=GLOCK17, model_path="auto")
    add_item("glock17_zoom", stats=GLOCK17, model_path="auto")
    add_item("glock18", stats=GLOCK18, model_path="auto")
    add_item("glock18_zoom", stats=GLOCK18, model_path="auto")
    add_item("vz61", stats=VZ61, model_path="auto")
    add_item("vz61_zoom", stats=VZ61, model_path="auto")

