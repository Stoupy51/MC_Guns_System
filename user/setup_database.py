
# Import database helper and setup constants
from python_datapack.utils.database_helper import (
    add_item_model_component,
    add_item_name_and_lore_if_missing,
    add_private_custom_data_for_namespace,
    add_smithed_ignore_vanilla_behaviours_convention,
)

from user.database.ak47 import main as main_ak47
from user.database.casing import main as main_casing


# Main function should return a database
def main(config: dict) -> dict[str, dict]:
    database: dict[str,dict] = {}
    ns: str = config["namespace"]

    # Add casings
    main_casing(database, ns)

    # Add weapons
    main_ak47(database, ns)

    # Final adjustments, you definitively should keep them!
    add_item_model_component(config, database)
    add_item_name_and_lore_if_missing(config, database)
    add_private_custom_data_for_namespace(config, database)
    add_smithed_ignore_vanilla_behaviours_convention(database)	# Smithed items convention
    print()

    # Return database
    return database

