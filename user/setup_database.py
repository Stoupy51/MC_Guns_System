
# Import database helper and setup constants
import json
from typing import Any

from python_datapack.utils.database_helper import (
    add_item_model_component,
    add_item_name_and_lore_if_missing,
    add_private_custom_data_for_namespace,
    add_smithed_ignore_vanilla_behaviours_convention,
)

from user.config.stats import CASING_MODEL, MODELS
from user.database.ak47 import main as main_ak47
from user.database.casing import main as main_casing


# Main function should return a database
def main(config: dict) -> dict[str, dict]:
    database: dict[str,dict] = {}
    ns: str = config["namespace"]

    # Add casings
    main_casing(database, ns)

    # Add guns
    main_ak47(database, ns)

    # Adjust guns data
    for item, data in database.items():

        # Get all gun data
        data["custom_data"] = json.loads(json.dumps(data.get("custom_data", {})))
        ns_data: dict[str, Any] = data["custom_data"].get(ns, {})
        gun_stats: dict[str, Any] = ns_data.get("stats", {})
        if ns_data.get("gun"):

            # If has casing, update model
            if gun_stats.get(CASING_MODEL):
                gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"

            # Define normal and zoom models
            normal_model: str = f"{ns}:{item.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

    # Sort items so that zoom models are at the end
    sorted_items: list[str] = sorted(database.keys(), key=lambda x: x.endswith("_zoom"))
    database = {k: database[k] for k in sorted_items}

    # Final adjustments, you definitively should keep them!
    add_item_model_component(config, database)
    add_item_name_and_lore_if_missing(config, database)
    add_private_custom_data_for_namespace(config, database)
    add_smithed_ignore_vanilla_behaviours_convention(database)	# Smithed items convention
    print()

    # Return database
    return database

