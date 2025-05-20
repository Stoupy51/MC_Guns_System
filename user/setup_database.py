
# Import database helper and setup constants
import json
from typing import Any

from python_datapack.utils.database_helper import add_item_model_component, add_item_name_and_lore_if_missing, add_private_custom_data_for_namespace, add_smithed_ignore_vanilla_behaviours_convention
from python_datapack.utils.database_helper import create_gradient_text as new_hex

from user.config.stats import CAPACITY, CASING_MODEL, COOLDOWN, DAMAGE, DECAY, MODELS, RELOAD_TIME, REMAINING_BULLETS, SWITCH
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

            # Update casing model
            gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"

            # Define normal and zoom models
            normal_model: str = f"{ns}:{item.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

            # Compute attack speed based of 'switch' stats
            # Formula: [attack_speed = (20.0 / switch_ticks) - 4.0] <- where 4.0 is default attack speed
            if gun_stats.get(SWITCH):
                attack_speed: float = (20.0 / gun_stats[SWITCH]) - 4.0
                data["attribute_modifiers"] = [{"type": "attack_speed", "amount": attack_speed, "operation": "add_value", "slot": "mainhand", "id": "minecraft:base_attack_speed"}]
                data["tooltip_display"] = {"hide_tooltip": False, "hidden_components": ["minecraft:attribute_modifiers"]}

            # Initialize magazine with full capacity
            gun_stats[REMAINING_BULLETS] = gun_stats[CAPACITY]

            # Set custom lore
            start_hex: str = "c24a17"
            end_hex: str = "c77e36"
            fire_rate: float = 20 / gun_stats[COOLDOWN]
            fire_rate_unit: str = "shots/s" if fire_rate > 1.0 else "s/shot"
            data["lore"] = [
                [*new_hex("Damage Per Bullet  ➤ ", start_hex, end_hex),    str(gun_stats[DAMAGE])],
                [*new_hex("Ammo Remaining      ➤ ", start_hex, end_hex),   str(gun_stats[REMAINING_BULLETS]),      {"text":"/","color":f"#{end_hex}"}, str(gun_stats[CAPACITY])],
                [*new_hex("Reloading Time       ➤ ", start_hex, end_hex),  f"{gun_stats[RELOAD_TIME] / 20:.1f}",   {"text":"s","color":f"#{end_hex}"}],
                [*new_hex("Fire Rate             ➤ ", start_hex, end_hex), f"{fire_rate:.1f} ",                    *new_hex(fire_rate_unit, end_hex, start_hex, text_length=10)],
                [*new_hex("Damage Decay       ➤ ", start_hex, end_hex),    f"{gun_stats[DECAY] * 100:.0f}",        {"text":"%","color":f"#{end_hex}"}],
                [*new_hex("Switch Time           ➤ ", start_hex, end_hex), f"{gun_stats[SWITCH] / 20:.1f}",        {"text":"s","color":f"#{end_hex}"}],
                "",
            ]

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

