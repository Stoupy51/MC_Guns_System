
# Import database helper and setup constants
import json
from typing import Any

from stewbeet import (
    Context,
    Item,
    Mem,
    add_item_model_component,
    add_item_name_and_lore_if_missing,
    add_private_custom_data_for_namespace,
    add_smithed_ignore_vanilla_behaviours_convention,
    export_all_definitions_to_json,
    set_manual_components,
)
from stewbeet import (
    create_gradient_text as new_hex,
)

from .config.stats import CAPACITY, CASING_MODEL, COOLDOWN, DAMAGE, DECAY, MODELS, RELOAD_TIME, REMAINING_BULLETS, SWITCH
from .database.ak47 import main as main_ak47
from .database.all_pistols import main as main_pistols
from .database.ammo import main as main_ammo
from .database.aug import main as main_aug
from .database.casing import main as main_casing
from .database.famas import main as main_famas
from .database.flash import main as main_flash
from .database.fnfal import main as main_fnfal
from .database.g3a3 import main as main_g3a3
from .database.m4a1 import main as main_m4a1
from .database.m16a4 import main as main_m16a4
from .database.m24 import main as main_m24
from .database.m82 import main as main_m82
from .database.m249 import main as main_m249
from .database.m500 import main as main_m500
from .database.m590 import main as main_m590
from .database.mac10 import main as main_mac10
from .database.mosin import main as main_mosin
from .database.mp5 import main as main_mp5
from .database.mp7 import main as main_mp7
from .database.ppsh41 import main as main_ppsh41
from .database.rpg7 import main as main_rpg7
from .database.rpk import main as main_rpk
from .database.scar17 import main as main_scar17
from .database.spas12 import main as main_spas12
from .database.sten import main as main_sten
from .database.svd import main as main_svd


# Main function should return a database
def beet_default(ctx: Context) -> None:
    ns: str = ctx.project_id

    # Add casings and flashes
    main_casing()
    main_flash()
    main_ammo()

    # Rifles
    main_m16a4()
    main_ak47()
    main_fnfal()
    main_aug()
    main_m4a1()
    main_g3a3()
    main_famas()
    main_scar17()

    # Pistols
    main_pistols()

    # SMGs
    main_mp5()
    main_mac10()
    main_mp7()
    main_ppsh41()
    main_sten()

    # Shotguns
    main_spas12()
    main_m500()
    main_m590()

    # Snipers
    main_svd()
    main_m82()
    main_mosin()
    main_m24()

    # Special
    main_rpg7()
    main_rpk()
    main_m249()

    # Adjust guns data
    for item in Mem.definitions.keys():
        obj = Item.from_id(item)

        # Get all gun data
        obj.components["custom_data"] = json.loads(json.dumps(obj.components.get("custom_data", {})))
        ns_data: dict[str, Any] = obj.components["custom_data"].get(ns, {})
        gun_stats: dict[str, Any] = ns_data.get("stats", {})
        if ns_data.get("gun"):

            # Update casing model
            if CASING_MODEL in gun_stats:
                gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"

            # Define normal and zoom models
            normal_model: str = f"{ns}:{item.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

            # Initialize magazine with full capacity
            gun_stats[REMAINING_BULLETS] = gun_stats[CAPACITY]

            # Prepare fire_rate lore
            START_HEX: str = "c24a17"
            END_HEX: str = "c77e36"
            fire_rate_component: list[list[Any]] = []
            if COOLDOWN in gun_stats:
                fire_rate: float = 20 / gun_stats[COOLDOWN]
                fire_rate_unit: str = "shots/s" if fire_rate > 1.0 else "s/shot"
                fire_rate_component.append([*new_hex("Fire Rate             ➤ ", START_HEX, END_HEX), f"{fire_rate:.1f} ", *new_hex(fire_rate_unit, END_HEX, START_HEX, text_length=10)])

            # Set custom lore
            obj.components["lore"] = [
                [*new_hex("Damage Per Bullet  ➤ ", START_HEX, END_HEX),    str(gun_stats[DAMAGE])],
                [*new_hex("Ammo Remaining      ➤ ", START_HEX, END_HEX),   str(gun_stats[REMAINING_BULLETS]),      {"text":"/","color":f"#{END_HEX}"}, str(gun_stats[CAPACITY])],
                [*new_hex("Reloading Time       ➤ ", START_HEX, END_HEX),  f"{gun_stats[RELOAD_TIME] / 20:.1f}",   {"text":"s","color":f"#{END_HEX}"}],
                *fire_rate_component,
                [*new_hex("Damage Decay       ➤ ", START_HEX, END_HEX),    f"{gun_stats[DECAY] * 100:.0f}",        {"text":"%","color":f"#{END_HEX}"}],
                [*new_hex("Switch Time           ➤ ", START_HEX, END_HEX), f"{gun_stats[SWITCH] / 20:.1f}",        {"text":"s","color":f"#{END_HEX}"}],
                "",
            ]

    # Sort items so that zoom models are at the end
    sorted_items: list[str] = sorted(Mem.definitions.keys(), key=lambda x: x.endswith("_zoom"))
    Mem.definitions = {k: Mem.definitions[k] for k in sorted_items}

    # Final adjustments, you definitively should keep them!
    add_item_model_component(black_list=["item_ids","you_don't_want","in_that","list"])
    add_item_name_and_lore_if_missing()
    add_private_custom_data_for_namespace()		# Add a custom namespace for easy item detection
    add_smithed_ignore_vanilla_behaviours_convention()	# Smithed items convention
    set_manual_components(white_list=["item_name", "lore", "custom_name", "damage", "max_damage"]) # Components to include in the manual when hovering items (here is the default list)

    # Debug purposes: export all definitions to a single json file
    export_all_definitions_to_json(f"{Mem.ctx.directory}/definitions_debug.json")

