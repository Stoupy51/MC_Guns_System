
# Import database helper and setup constants
import json
from typing import Any

from python_datapack.utils.database_helper import add_item_model_component, add_item_name_and_lore_if_missing, add_private_custom_data_for_namespace, add_smithed_ignore_vanilla_behaviours_convention
from python_datapack.utils.database_helper import create_gradient_text as new_hex

from user.config.stats import CAPACITY, CASING_MODEL, COOLDOWN, DAMAGE, DECAY, MODELS, RELOAD_TIME, REMAINING_BULLETS, SWITCH
from user.database.ak47 import main as main_ak47
from user.database.aug import main as main_aug
from user.database.casing import main as main_casing
from user.database.fnfal import main as main_fnfal
from user.database.glock18 import main as main_glock18
from user.database.m16a4 import main as main_m16a4
from user.database.m24 import main as main_m24
from user.database.m82 import main as main_m82
from user.database.m249 import main as main_m249
from user.database.m500 import main as main_m500
from user.database.m590 import main as main_m590
from user.database.mac10 import main as main_mac10
from user.database.mosin import main as main_mosin
from user.database.mp5 import main as main_mp5
from user.database.mp7 import main as main_mp7
from user.database.ppsh41 import main as main_ppsh41
from user.database.rpg7 import main as main_rpg7
from user.database.rpk import main as main_rpk
from user.database.spas12 import main as main_spas12
from user.database.sten import main as main_sten
from user.database.svd import main as main_svd
from user.database.vz61 import main as main_vz61


# Main function should return a database
def main(config: dict) -> dict[str, dict]:
    database: dict[str,dict] = {}
    ns: str = config["namespace"]

    # Add casings
    main_casing(database, ns)

    # Rifles
    main_m16a4(database, ns)
    main_ak47(database, ns)
    main_fnfal(database, ns)
    main_aug(database, ns)

    # Pistols
    main_glock18(database, ns)
    main_vz61(database, ns)

    # SMGs
    main_mp5(database, ns)
    main_mac10(database, ns)
    main_mp7(database, ns)
    main_ppsh41(database, ns)
    main_sten(database, ns)

    # Shotguns
    main_spas12(database, ns)
    main_m500(database, ns)
    main_m590(database, ns)

    # Snipers
    main_svd(database, ns)
    main_m82(database, ns)
    main_mosin(database, ns)
    main_m24(database, ns)

    # Special
    main_rpg7(database, ns)
    main_rpk(database, ns)
    main_m249(database, ns)

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

