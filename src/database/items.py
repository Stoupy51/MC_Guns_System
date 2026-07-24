
# Every item definition except camos (camo.py). Registration order sets Mem.definitions order.
from stewbeet import Item, JsonDict, Mem

from ..config.catalogs import SCOPE_VARIANTS
from ..config.stats import (
    AK47,
    AUG,
    CAPACITY,
    CASING_9X18MM,
    CASING_9X19MM,
    CASING_12GA3IN,
    CASING_12GA275IN,
    CASING_32ACP,
    CASING_45ACP,
    CASING_46X30MM,
    CASING_50AE,
    CASING_50BMG,
    CASING_338LAPUA,
    CASING_556X45MM,
    CASING_762X25MM,
    CASING_762X39MM,
    CASING_762X51MM,
    CASING_762X54MM,
    DEAGLE,
    FAMAS,
    FLASH_GRENADE,
    FNFAL,
    FRAG_GRENADE,
    G3A3,
    GLOCK17,
    GLOCK18,
    M4A1,
    M9,
    M16A4,
    M24,
    M82,
    M249,
    M500,
    M590,
    M1911,
    MAC10,
    MAKAROV,
    MONKEY_BOMB,
    MOSIN,
    MP5,
    MP7,
    PPSH41,
    RAY_GUN,
    REMAINING_BULLETS,
    RPG7,
    RPK,
    SCAR17,
    SEMTEX,
    SMOKE_GRENADE,
    SPAS12,
    STEN,
    SVD,
    VZ61,
    WEB_GRENADE,
    add_item,
    get_model_path,
    load_model,
)

# Weapon ID -> stats dict
WEAPON_STATS: dict[str, JsonDict] = {
    "ak47": AK47, "aug": AUG, "famas": FAMAS, "fnfal": FNFAL, "g3a3": G3A3,
    "m4a1": M4A1, "m16a4": M16A4, "m24": M24, "m82": M82, "m249": M249,
    "m500": M500, "m590": M590, "mac10": MAC10, "mosin": MOSIN, "mp5": MP5,
    "mp7": MP7, "ppsh41": PPSH41, "rpk": RPK, "scar17": SCAR17, "spas12": SPAS12,
    "sten": STEN, "svd": SVD,
    # Pistols
    "m1911": M1911, "m9": M9, "deagle": DEAGLE, "makarov": MAKAROV,
    "glock17": GLOCK17, "glock18": GLOCK18, "vz61": VZ61, "ray_gun": RAY_GUN,
}

# Special rarity overrides
WEAPON_RARITY: dict[str, str] = {
    "ray_gun": "epic",
}

# Reusable magazines: (weapon, capacity). A full and an "_empty" variant is made for each.
MAGAZINES: list[tuple[str, int]] = [
    ("ak47", 30), ("aug", 30), ("deagle", 7), ("famas", 25), ("fnfal", 20),
    ("g3a3", 20), ("glock17", 17), ("glock18", 19), ("m16a4", 30), ("m1911", 7),
    ("m249", 150), ("m4a1", 30), ("m82", 10), ("m9", 15), ("mac10", 30),
    ("makarov", 8), ("mp5", 30), ("mp7", 40), ("ppsh41", 71), ("rpk", 75),
    ("scar17", 20), ("sten", 32), ("svd", 10), ("vz61", 20),
]

# Individual rounds that stack; reloading consumes items from the stack, not the whole stack.
CONSUMABLE_MAGAZINES: list[tuple[str, str, int]] = [
    ("rpg7", "rpg7_rocket", 1),
    ("mosin", "mosin_bullet", 1),
    ("m24", "m24_bullet", 1),
    ("spas12", "spas12_shell", 1),
    ("m500", "m500_shell", 1),
    ("m590", "m590_shell", 1),
    ("ray_gun", "element_115", 1),
]

CASINGS: tuple[str, ...] = (
    CASING_9X18MM, CASING_9X19MM, CASING_12GA3IN, CASING_12GA275IN, CASING_32ACP,
    CASING_45ACP, CASING_46X30MM, CASING_50AE, CASING_50BMG, CASING_338LAPUA,
    CASING_556X45MM, CASING_762X25MM, CASING_762X39MM, CASING_762X51MM,
    CASING_762X54MM,
)

# Perk machines in registration order: a dye name recolors both accent slots, a pair sets them explicitly.
PERK_MACHINES: dict[str, str | tuple[str, str]] = {
    "juggernog": "red",
    "speed_cola": "lime",
    "double_tap": "yellow",
    "quick_revive": "light_blue",
    "mule_kick": "green",
    "stamin_up": "orange",
    "phd_flopper": "purple",
    "deadshot": ("minecraft:block/green_terracotta", "minecraft:block/dark_prismarine"),
    "timeslip": "magenta",
    "electric_cherry": "blue",
    "widows_wine": ("minecraft:block/black_concrete", "minecraft:block/red_terracotta"),
    "dying_wish": ("minecraft:block/blue_concrete", "minecraft:block/white_terracotta"),
    "tombstone": "brown",
    "whos_who": "cyan",
}


def perk_machine_model(accent: str | tuple[str, str]) -> JsonDict:
    """ Perk-machine child model overriding the two accent texture slots. """
    first, second = accent if isinstance(accent, tuple) else (f"minecraft:block/{accent}_concrete", f"minecraft:block/{accent}_terracotta")
    return {
        "parent": "mgs:item/perk_machine",
        "textures": {"accent": first, "accent2": second, "particle": second},
    }


def recolored_model(model_name: str, gray_map: JsonDict, default: str | None = None) -> JsonDict:
    """ Load a model and remap its textures through `gray_map`; `default` replaces unmapped ones (None keeps them). """
    model: JsonDict = load_model(get_model_path(model_name))
    for key, tex in model["textures"].items():
        model["textures"][key] = gray_map.get(tex, default if default is not None else tex)
    return model


def power_switch_on_model() -> JsonDict:
    """ "On" breaker: lever flipped down, handle/light lit green. Mirrored about pivot y=7 and tilted
    forward-down rather than rotated 180°, because Minecraft caps element rotations at ±45°. """
    model: JsonDict = load_model(get_model_path("power_switch"))
    model["textures"]["handle"] = "minecraft:block/lime_terracotta"
    model["textures"]["light"] = "minecraft:block/sea_lantern"
    pivot_y = 7
    for el in model["elements"]:
        if el["name"] in ("lever handle", "lever knob"):
            y_from, y_to = el["from"][1], el["to"][1]
            el["from"][1] = 2 * pivot_y - y_to
            el["to"][1] = 2 * pivot_y - y_from
            el["rotation"]["angle"] = 45  # tilt forward-down (off is -45, forward-up)
    return model


def add_casings() -> None:
    """ Ejected bullet casings, named after their cartridge. """
    for casing in CASINGS:
        add_item(casing, model_path="auto").components["item_name"] = {"text": casing, "color": "white"}


def add_magazines() -> None:
    """ Reusable magazines (full + empty) and the stacking single-round items. """
    ns: str = Mem.ctx.project_id
    for weapon, capacity in MAGAZINES:
        for is_empty in (False, True):
            item: str = f"{weapon}_mag{'_empty' if is_empty else ''}"
            Item(
                id=item,
                override_model=load_model(get_model_path(item)),
                components={
                    "max_stack_size": 1,
                    "custom_data": {ns: {"magazine": True, "weapon": weapon, "stats": {REMAINING_BULLETS: 0 if is_empty else capacity, CAPACITY: capacity}}},
                    "rarity": "common",
                }
            )

    for weapon, item_name, capacity in CONSUMABLE_MAGAZINES:
        Item(
            id=item_name,
            override_model=load_model(get_model_path(item_name)),
            components={
                "max_stack_size": 64,
                "custom_data": {ns: {"magazine": True, "consumable": True, "weapon": weapon, "stats": {REMAINING_BULLETS: capacity, CAPACITY: capacity}}},
                "rarity": "common",
            }
        )


def add_machines_and_props() -> None:
    """ Zombies map props: knife, Pack-a-Punch, Mystery Box, perk machines, breaker, turret. """
    ns: str = Mem.ctx.project_id

    # BO->MC 2/15 damage conversion like the zombie HP curve: BO 1150 -> MC 153, one-hit until ~round 11.
    Item(
        id="bowie_knife",
        base_item="minecraft:iron_sword",
        components={
            "max_stack_size": 1,
            "rarity": "rare",
            "unbreakable": {},
            "custom_data": {ns: {"knife": True, "bowie_knife": True}},
            "item_name": [{"text": "Bowie Knife", "color": "gold", "italic": False}],
            "lore": [[{"text": "One-hit kills until ~round 11", "color": "gray", "italic": False}]],
            "attribute_modifiers": [
                {"type": "attack_damage", "amount": 153, "operation": "add_value", "slot": "mainhand", "id": "minecraft:base_attack_damage"},
                {"type": "attack_speed", "amount": -2.5, "operation": "add_value", "slot": "mainhand", "id": "minecraft:base_attack_speed"},
            ],
        },
        override_model=load_model(get_model_path("bowie_knife")),
    )

    Item(id="pack_a_punch", override_model=load_model(get_model_path("pack_a_punch")))

    # Split into base + lid so the lid can animate open.
    Item(id="mystery_box_base", override_model=load_model(get_model_path("mystery_box_base")))
    Item(id="mystery_box_lid", override_model=load_model(get_model_path("mystery_box_lid")))
    # Grayed-out crate (base only, every texture muted) shown at inactive roam spots.
    Item(id="mystery_box_disabled", override_model=recolored_model("mystery_box_base", {
        "minecraft:block/oak_planks": "minecraft:block/gray_concrete",
        "minecraft:block/stripped_dark_oak_log": "minecraft:block/deepslate",
        "minecraft:block/gold_block": "minecraft:block/iron_block",
        "minecraft:block/sea_lantern": "minecraft:block/light_gray_concrete",
        "minecraft:block/hay_block_top": "minecraft:block/light_gray_concrete",
    }, default="minecraft:block/gray_concrete"))

    # A new perk only needs an entry in PERK_MACHINES and a default line in perks.py setup_iter.
    Item(id="perk_machine", override_model=load_model(get_model_path("perk_machine")))
    for perk_id, accent in PERK_MACHINES.items():
        Item(id=f"perk_machine_{perk_id}", override_model=perk_machine_model(accent))

    # Dedicated model (not a recolor): the middle alcove is open so the perk bottle can float in it.
    Item(id="der_wunderfizz", override_model=load_model(get_model_path("der_wunderfizz")))
    Item(id="der_wunderfizz_disabled", override_model=recolored_model("der_wunderfizz", {
        "minecraft:block/gold_block": "minecraft:block/iron_block",
        "minecraft:block/purple_concrete": "minecraft:block/gray_concrete",
        "minecraft:block/sea_lantern": "minecraft:block/light_gray_concrete",
    }))

    Item(id="power_switch", override_model=load_model(get_model_path("power_switch")))
    Item(id="power_switch_on", override_model=power_switch_on_model())

    # Stationary base + rotating head (centred on [8,8,8], barrels along +Z for a facing-entity display).
    Item(id="turret_base", override_model=load_model(get_model_path("turret_base")))
    Item(id="turret_head", override_model=load_model(get_model_path("turret_head")))


def add_weapons() -> None:
    """ The RPG-7, then every gun with its scope variants; each gets a `_zoom` twin. """
    for name in ("rpg7", "rpg7_zoom", "rpg7_empty", "rpg7_empty_zoom"):
        add_item(name, stats=RPG7, model_path="auto")

    for weapon_id, stats in WEAPON_STATS.items():
        rarity: str | None = WEAPON_RARITY.get(weapon_id)
        for suffix in SCOPE_VARIANTS.get(weapon_id, ("",)):
            for name in (f"{weapon_id}{suffix}", f"{weapon_id}{suffix}_zoom"):
                item: Item = add_item(name, stats=stats, model_path="auto")
                if rarity:
                    item.components["rarity"] = rarity


def add_grenades() -> None:
    """ Throwables, including the two that are never in a multiplayer loadout. """
    ns: str = Mem.ctx.project_id
    for grenade_id, stats in (
        ("frag_grenade", FRAG_GRENADE), ("semtex", SEMTEX),
        ("smoke_grenade", SMOKE_GRENADE), ("flash_grenade", FLASH_GRENADE),
    ):
        add_item(grenade_id, stats=stats, model_path="auto", max_stack_size=4)

    # Widow's Wine web grenade (perk-exclusive): frag geometry, cobweb texture.
    web = add_item("web_grenade", stats=WEB_GRENADE, model_path=get_model_path("frag_grenade"), max_stack_size=4)
    if web.override_model:
        for k in web.override_model["textures"].keys():
            web.override_model["textures"][k] = f"{ns}:item/cobweb"

    # Zombies-exclusive tactical (mystery box / wallbuys only), capped at 3 by the give/refill functions.
    add_item("monkey_bomb", stats=MONKEY_BOMB, model_path="auto", max_stack_size=3)


def main() -> None:
    """ Register every item, in the order that defines Mem.definitions ordering. """
    add_casings()
    add_magazines()
    add_machines_and_props()
    add_weapons()
    add_grenades()
