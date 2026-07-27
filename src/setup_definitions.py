""" Item definition setup: registers every item, then derives names, lore and components. """
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
    SPEED_MULTIPLY_BASE,
    START_HEX,
    SWITCH,
)
from .database.camo import main as camo_main
from .database.items import main as main_items

EMPTY_LORE_LINE: JsonDict = {"text": "", "italic": False}
""" Blank lore separator. NOT a bare "": that is a StringTag while the styled stat lines are
CompoundTags, and NBT lists are homogeneous, so the mix makes NbtOps wrap every line as
{"": <line>}, which zombies/pap re-parses and renders blank. A style keeps it a CompoundTag. """

@stp.measure_time(printer=stp.progress, message="Set up item definitions")
def beet_default(ctx: Context) -> None:
    ns: str = ctx.project_id

    # Registration order matters
    main_items()

    # Multiplayer class menu item
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

    weapon_display_names: dict[str, str] = {
        **{w.item_id: w.display_name for w in PRIMARY_WEAPONS},
        **{w.item_id: w.display_name for w in SECONDARY_WEAPONS},
    }
    grenade_display_names: dict[str, str] = {
        g.item_id: g.display_name for g in GRENADE_TYPES if g.item_id
    }

    for item in Mem.definitions.keys():
        obj = Item.from_id(item)

        obj.components["custom_data"] = json.loads(json.dumps(obj.components.get("custom_data", {})))
        ns_data: JsonDict = obj.components["custom_data"].get(ns, {})
        if ns_data.get("gun"):
            gun_stats: JsonDict = ns_data.get("stats", {})

            # Resolve the catalog display name and optional scope suffix
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

            if CASING_MODEL in gun_stats:
                gun_stats[CASING_MODEL] = f"{ns}:{gun_stats[CASING_MODEL]}"

            normal_model: str = f"{ns}:{item.replace('_zoom', '')}"
            zoom_model: str = normal_model + "_zoom"
            gun_stats[MODELS] = {"normal": normal_model, "zoom": zoom_model}

            # Start with a full magazine
            gun_stats[REMAINING_BULLETS] = gun_stats[CAPACITY]

            # _3 variants get x3 zoom, _4 variants x4
            if scope_suffix == "_3":
                gun_stats["scope_level"] = 3
            elif scope_suffix == "_4":
                gun_stats["scope_level"] = 4

            # consumable + use_effects give tick-perfect right-click detection
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

            # Held-weapon movement penalty
            if SPEED_MULTIPLY_BASE in gun_stats:
                speed_multiply_base: float = gun_stats[SPEED_MULTIPLY_BASE]
                attribute_modifiers: list[JsonDict] = obj.components.setdefault("attribute_modifiers", [])
                attribute_modifiers.append({
                    "type": "movement_speed",
                    "amount": speed_multiply_base,
                    "operation": "add_multiplied_base",
                    "slot": "mainhand",
                    "id": f"{ns}:weapon_weight_speed",
                })

            fire_rate_component: list[TextComponent] = []
            if COOLDOWN in gun_stats:
                fire_rate: float = 20 / gun_stats[COOLDOWN]
                fire_rate_unit: str = "shots/s" if fire_rate > 1.0 else "s/shot"
                fire_rate_component.append([*new_hex("Fire Rate             ➤ ", START_HEX, END_HEX), f"{fire_rate:.1f} ", *new_hex(fire_rate_unit, END_HEX, START_HEX, text_length=10)])

            pellet_component: list[TextComponent] = []
            if PELLET_COUNT in gun_stats:
                pellet_component.append([*new_hex("Pellets Per Shot    ➤ ", START_HEX, END_HEX), str(gun_stats[PELLET_COUNT])])

            # Grenades get their own lore, and stack
            if GRENADE_TYPE in gun_stats:
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
                obj.components["lore"] = [*lore, EMPTY_LORE_LINE]
            else:
                obj.components["lore"] = [
                    [*new_hex("Damage Per Bullet  ➤ ", START_HEX, END_HEX),    str(gun_stats[DAMAGE])],
                    [*new_hex("Ammo Remaining      ➤ ", START_HEX, END_HEX),   str(gun_stats[REMAINING_BULLETS]),      {"text":"/","color":f"#{END_HEX}"}, str(gun_stats[CAPACITY])],
                    [*new_hex("Reloading Time       ➤ ", START_HEX, END_HEX),  f"{gun_stats[RELOAD_TIME] / 20:.1f}",   {"text":"s","color":f"#{END_HEX}"}],
                    *fire_rate_component,
                    *pellet_component,
                    [*new_hex("Damage Decay       ➤ ", START_HEX, END_HEX),    f"{gun_stats[DECAY] * 100:.0f}",        {"text":"%","color":f"#{END_HEX}"}],
                    [*new_hex("Switch Time           ➤ ", START_HEX, END_HEX), f"{gun_stats[SWITCH] / 20:.1f}",        {"text":"s","color":f"#{END_HEX}"}],
                    EMPTY_LORE_LINE,
                ]

        if ns_data.get("magazine"):
            bullets: int = ns_data["stats"][REMAINING_BULLETS]
            capacity: int = ns_data["stats"]["capacity"]
            obj.components["lore"] = [
                [*new_hex("Ammo Remaining ➤ ", START_HEX, END_HEX), str(bullets), {"text": "/", "color": f"#{END_HEX}"}, str(capacity)],
            ]

    # Camo variants per weapon
    camo_main()

    # Zoom models sort to the end
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

    # Keep these out of the give_all chests
    for item in Mem.definitions.keys():
        obj = Item.from_id(item)
        if item.endswith(("_zoom", "_mag_empty")):
            obj.skip_gives = True

    # Final adjustments, keep them
    add_item_model_component(black_list=["item_ids","you_don't_want","in_that","list"])
    add_item_name_and_lore_if_missing()
    add_private_custom_data_for_namespace()		# Add a custom namespace for easy item detection
    add_smithed_ignore_vanilla_behaviours_convention()	# Smithed items convention
    set_manual_components(white_list=["item_name", "lore", "custom_name", "damage", "max_damage"]) # Components to include in the manual when hovering items (here is the default list)

