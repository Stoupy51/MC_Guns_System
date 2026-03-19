
# Imports
import json

import stouputils as stp
from stewbeet import (
    Context,
    Item,
    JsonDict,
    Mem,
    TextComponent,
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

from .config.catalogs import GRENADE_TYPES, PRIMARY_WEAPONS, SCOPE_NAMES, SECONDARY_WEAPONS
from .config.stats import (
    CAPACITY,
    CASING_MODEL,
    COOLDOWN,
    DAMAGE,
    DECAY,
    END_HEX,
    EXPLOSION_DAMAGE,
    EXPLOSION_RADIUS,
    GRENADE_FUSE,
    GRENADE_TYPE,
    MODELS,
    PELLET_COUNT,
    RELOAD_TIME,
    REMAINING_BULLETS,
    START_HEX,
    SWITCH,
)
from .database.ak47 import main as main_ak47
from .database.all_pistols import main as main_pistols
from .database.ammo import main as main_ammo
from .database.aug import main as main_aug
from .database.casing import main as main_casing
from .database.famas import main as main_famas
from .database.fnfal import main as main_fnfal
from .database.g3a3 import main as main_g3a3
from .database.grenades import main as main_grenades
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
@stp.measure_time(printer=stp.progress, message="Set up item definitions")
def beet_default(ctx: Context) -> None:
    ns: str = ctx.project_id

    # Add casings and flashes
    main_casing()
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

    # Grenades
    main_grenades()

    # Multiplayer class menu item (right-click to open class selection)
    Item(
        id="class_menu",
        base_item="minecraft:warped_fungus_on_a_stick",
        components={
            "max_stack_size": 1,
            "custom_data": {ns: {"class_menu": True}},
            "rarity": "common",
            "item_name": [{"text": "Class Menu", "color": "gold", "italic": False}],
            "item_model": "minecraft:nether_star",
        },
    )

    # Name maps sourced from shared loadout catalogs
    weapon_display_names: dict[str, str] = {
        **{item_id: display for item_id, display, *_ in PRIMARY_WEAPONS},
        **{item_id: display for item_id, display, *_ in SECONDARY_WEAPONS},
    }
    grenade_display_names: dict[str, str] = {
        item_id: display for item_id, display in GRENADE_TYPES if item_id
    }

    # Adjust guns data
    for item in Mem.definitions.keys():
        obj = Item.from_id(item)

        # Get all gun data
        obj.components["custom_data"] = json.loads(json.dumps(obj.components.get("custom_data", {})))
        ns_data: JsonDict = obj.components["custom_data"].get(ns, {})
        if ns_data.get("gun"):
            gun_stats: JsonDict = ns_data.get("stats", {})

            # Resolve catalog display name + optional scope suffix
            base_name: str = item.replace("_zoom", "")
            scope_suffix: str = ""
            for candidate in ("_1", "_2", "_3", "_4"):
                if base_name.endswith(candidate):
                    scope_suffix = candidate
                    break
            base_weapon_id: str = base_name[:-2] if scope_suffix else base_name

            display_name: str | None = weapon_display_names.get(base_weapon_id)
            if not display_name:
                display_name = grenade_display_names.get(base_weapon_id)
            if not display_name and GRENADE_TYPE in gun_stats:
                grenade_key = str(gun_stats[GRENADE_TYPE])
                display_name = (
                    grenade_display_names.get(grenade_key)
                    or grenade_display_names.get(f"{grenade_key}_grenade")
                    or grenade_key.replace("_", " ").title()
                )

            if display_name:
                scope_name: str | None = SCOPE_NAMES.get(scope_suffix)
                if scope_suffix and scope_name:
                    display_name = f"{display_name} ({scope_name})"
                obj.components["item_name"] = [{"text": display_name, "color": "gold", "italic": False}]

            # Update casing model
            if CASING_MODEL in gun_stats:
                gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"

            # Define normal and zoom models
            normal_model: str = f"{ns}:{item.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

            # Initialize magazine with full capacity
            gun_stats[REMAINING_BULLETS] = gun_stats[CAPACITY]

            # Mark weapons with scopes: _3 variants get x3 zoom, _4 variants get x4 zoom
            if scope_suffix == "_3":
                ns_data["scope_level"] = 3
            elif scope_suffix == "_4":
                ns_data["scope_level"] = 4

            # Add consumable and use_effects components for tick-perfect right-click detection
            obj.components["consumable"] = {
                "consume_seconds": 1_000_000,  # Very high value to avoid actual consumption
                "animation": "spear",   # Not "none" because of "use" animation still present, but "spear" has minimal animation
                "sound": "minecraft:intentionally_empty",
                "has_consume_particles": False
            }
            obj.components["use_effects"] = {
                "can_sprint": True,
                "speed_multiplier": 1.0,
                "interact_vibrations": False
            }
            obj.components["food"] = {"saturation":0,"nutrition":0,"can_always_eat":True}

            # Prepare fire_rate lore
            fire_rate_component: list[TextComponent] = []
            if COOLDOWN in gun_stats:
                fire_rate: float = 20 / gun_stats[COOLDOWN]
                fire_rate_unit: str = "shots/s" if fire_rate > 1.0 else "s/shot"
                fire_rate_component.append([*new_hex("Fire Rate             ➤ ", START_HEX, END_HEX), f"{fire_rate:.1f} ", *new_hex(fire_rate_unit, END_HEX, START_HEX, text_length=10)])

            # Prepare pellet count lore
            pellet_component: list[TextComponent] = []
            if PELLET_COUNT in gun_stats:
                pellet_component.append([*new_hex("Pellets Per Shot    ➤ ", START_HEX, END_HEX), str(gun_stats[PELLET_COUNT])])

            # Grenades have different lore than regular guns
            if GRENADE_TYPE in gun_stats:
                # Grenades can stack (not limited to 1)
                obj.components["max_stack_size"] = 16

                grenade_type_display: str = gun_stats[GRENADE_TYPE].replace("_", " ").title()
                fuse_seconds: float = gun_stats.get(GRENADE_FUSE, 0) / 20
                lore: list[TextComponent] = [
                    [*new_hex("Type                  ➤ ", START_HEX, END_HEX), grenade_type_display],
                    [*new_hex("Fuse Time            ➤ ", START_HEX, END_HEX), f"{fuse_seconds:.1f}", {"text":"s","color":f"#{END_HEX}"}],
                ]
                if EXPLOSION_DAMAGE in gun_stats:
                    lore.insert(-1,
                        [*new_hex("Explosion Damage  ➤ ", START_HEX, END_HEX), str(gun_stats[EXPLOSION_DAMAGE])]
                    )
                if EXPLOSION_RADIUS in gun_stats:
                    lore.insert(-1,
                        [*new_hex("Explosion Radius   ➤ ", START_HEX, END_HEX), str(gun_stats[EXPLOSION_RADIUS])," ",{"text":"blocks","color":f"#{END_HEX}"}]
                    )
                obj.components["lore"] = [*lore, ""]
            else:
                # Set custom lore for regular guns
                obj.components["lore"] = [
                    [*new_hex("Damage Per Bullet  ➤ ", START_HEX, END_HEX),    str(gun_stats[DAMAGE])],
                    [*new_hex("Ammo Remaining      ➤ ", START_HEX, END_HEX),   str(gun_stats[REMAINING_BULLETS]),      {"text":"/","color":f"#{END_HEX}"}, str(gun_stats[CAPACITY])],
                    [*new_hex("Reloading Time       ➤ ", START_HEX, END_HEX),  f"{gun_stats[RELOAD_TIME] / 20:.1f}",   {"text":"s","color":f"#{END_HEX}"}],
                    *fire_rate_component,
                    *pellet_component,
                    [*new_hex("Damage Decay       ➤ ", START_HEX, END_HEX),    f"{gun_stats[DECAY] * 100:.0f}",        {"text":"%","color":f"#{END_HEX}"}],
                    [*new_hex("Switch Time           ➤ ", START_HEX, END_HEX), f"{gun_stats[SWITCH] / 20:.1f}",        {"text":"s","color":f"#{END_HEX}"}],
                    "",
                ]

        # Adjust magazines data
        if ns_data.get("magazine"):
            bullets: int = ns_data["stats"][REMAINING_BULLETS]

            # Get magazine's capacity
            capacity: int = ns_data["stats"]["capacity"]

            # Set magazine lore
            obj.components["lore"] = [
                [*new_hex("Ammo Remaining ➤ ", START_HEX, END_HEX), str(bullets), {"text": "/", "color": f"#{END_HEX}"}, str(capacity)],
            ]

    # Sort items so that zoom models are at the end
    def sorter(k: str) -> int:
        obj = Item.from_id(k)
        ns_data: JsonDict = obj.components.get("custom_data", {}).get(ns, {})
        if ns_data.get("casing"):
            return 4
        if k.endswith("_zoom"):
            return 2
        if k.endswith("_mag_empty"):
            return 1
        return 0
    sorted_items: list[str] = sorted(Mem.definitions.keys(), key=sorter)
    Mem.definitions = {k: Mem.definitions[k] for k in sorted_items}

    # Final adjustments, you definitively should keep them!
    add_item_model_component(black_list=["item_ids","you_don't_want","in_that","list"])
    add_item_name_and_lore_if_missing()
    add_private_custom_data_for_namespace()		# Add a custom namespace for easy item detection
    add_smithed_ignore_vanilla_behaviours_convention()	# Smithed items convention
    set_manual_components(white_list=["item_name", "lore", "custom_name", "damage", "max_damage"]) # Components to include in the manual when hovering items (here is the default list)

    # Debug purposes: export all definitions to a single json file
    return
    export_all_definitions_to_json(f"{Mem.ctx.directory}/definitions_debug.json", Mem.definitions)

