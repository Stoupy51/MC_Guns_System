
# Imports
from stewbeet import Item, JsonDict, Mem

from ..config.stats import get_model_path, load_model


def override_model(color: str) -> JsonDict:
    return {
        "parent": "mgs:item/perk_machine",
        "textures": {
            "accent": f"minecraft:block/{color}_concrete",
            "accent2": f"minecraft:block/{color}_terracotta",
            "particle": f"minecraft:block/{color}_terracotta",
        }
    }


def override_model_2tone(accent: str, accent2: str) -> JsonDict:
    """ Perk-machine recolor when no single dye reads right (README task 5 taste calls). Pass the
    full block texture paths for the two accent slots directly. """
    return {
        "parent": "mgs:item/perk_machine",
        "textures": {
            "accent": accent,
            "accent2": accent2,
            "particle": accent2,
        }
    }


def mystery_box_disabled_model() -> JsonDict:
    """ Grayed-out Mystery Box crate (the base without the lid) shown at inactive roam spots so
    players can see where the box might travel to. Same geometry as mystery_box_base, every vanilla
    texture remapped to a muted grayscale block (no gold, no lit lantern). """
    model: JsonDict = load_model(get_model_path("mystery_box_base"))
    gray_map: JsonDict = {
        "minecraft:block/oak_planks": "minecraft:block/gray_concrete",
        "minecraft:block/stripped_dark_oak_log": "minecraft:block/deepslate",
        "minecraft:block/gold_block": "minecraft:block/iron_block",
        "minecraft:block/sea_lantern": "minecraft:block/light_gray_concrete",
        "minecraft:block/hay_block_top": "minecraft:block/light_gray_concrete",
    }
    for key, tex in model["textures"].items():
        model["textures"][key] = gray_map.get(tex, "minecraft:block/gray_concrete")
    return model


def der_wunderfizz_disabled_model() -> JsonDict:
    """ Grayed-out Der Wunderfizz cabinet shown at inactive roam spots (see mystery_box_disabled_model).
    Gold/purple accents remapped to iron/gray; the lit lantern goes dark; the already-gray/black
    structural textures are kept. """
    model: JsonDict = load_model(get_model_path("der_wunderfizz"))
    gray_map: JsonDict = {
        "minecraft:block/gold_block": "minecraft:block/iron_block",
        "minecraft:block/purple_concrete": "minecraft:block/gray_concrete",
        "minecraft:block/sea_lantern": "minecraft:block/light_gray_concrete",
    }
    for key, tex in model["textures"].items():
        model["textures"][key] = gray_map.get(tex, tex)
    return model


def power_switch_on_model() -> JsonDict:
    """ "On" breaker model: same box as the base, but the lever is flipped to the DOWN position
    and the handle + indicator light recolored green/lit. The lever bar is physically mirrored
    about the housing pivot (y=7) and tilted forward-down, because Minecraft caps element
    rotations at ±45° and so the bar can't simply be rotated 180° from the up (off) position. """
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

# Main function should return a database
def main() -> None:
    ns: str = Mem.ctx.project_id

    # Bowie Knife: zombies wall-buy knife upgrade for hotbar.0 (see zombies/wallbuys.py buy_knife).
    # Damage follows the same BO->MC 2/15 conversion as the zombie HP curve: BO Bowie 1150 -> MC 153,
    # one-hit kills until ~round 11 like the original (plain knife is BO 150 -> MC 20, helpers.py).
    # Netherite sword texture as placeholder until real knife art exists (see zombies README task 1).
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

    # Add Pack-a-Punch
    Item(id="pack_a_punch", override_model=load_model(get_model_path("pack_a_punch")))

    # Mystery Box crate (vanilla textures), split into base + lid so the lid can animate open.
    Item(id="mystery_box_base", override_model=load_model(get_model_path("mystery_box_base")))
    Item(id="mystery_box_lid", override_model=load_model(get_model_path("mystery_box_lid")))
    # Grayed-out crate (base only) shown at inactive roam spots (see zombies/roaming.py).
    Item(id="mystery_box_disabled", override_model=mystery_box_disabled_model())

    # Generic perk machine (vanilla textures) + per-perk recolors.
    # New perks only need a small child model overriding the "accent"/"accent2" textures
    # (see perk_machine_juggernog.json) and a default line in zombies/perks.py setup_iter.
    Item(id="perk_machine", override_model=load_model(get_model_path("perk_machine")))
    Item(id="perk_machine_juggernog", override_model=override_model("red"))
    Item(id="perk_machine_speed_cola", override_model=override_model("lime"))
    Item(id="perk_machine_double_tap", override_model=override_model("yellow"))
    Item(id="perk_machine_quick_revive", override_model=override_model("light_blue"))
    Item(id="perk_machine_mule_kick", override_model=override_model("green"))
    Item(id="perk_machine_stamin_up", override_model=override_model("orange"))
    Item(id="perk_machine_phd_flopper", override_model=override_model("purple"))
    Item(id="perk_machine_deadshot", override_model=override_model_2tone(
        "minecraft:block/green_terracotta", "minecraft:block/dark_prismarine"))
    Item(id="perk_machine_timeslip", override_model=override_model("magenta"))
    Item(id="perk_machine_electric_cherry", override_model=override_model("blue"))
    Item(id="perk_machine_widows_wine", override_model=override_model_2tone(
        "minecraft:block/black_concrete", "minecraft:block/red_terracotta"))
    Item(id="perk_machine_dying_wish", override_model=override_model_2tone(
        "minecraft:block/blue_concrete", "minecraft:block/white_terracotta"))
    Item(id="perk_machine_tombstone", override_model=override_model("brown"))
    Item(id="perk_machine_whos_who", override_model=override_model("cyan"))
    # Dedicated model (not a perk-machine recolor): gold/purple cabinet with an OPEN middle alcove
    # where the spinning perk bottle floats (see zombies/wunderfizz.py spawn_orb).
    Item(id="der_wunderfizz", override_model=load_model(get_model_path("der_wunderfizz")))
    # Grayed-out cabinet shown at inactive roam spots (see zombies/roaming.py).
    Item(id="der_wunderfizz_disabled", override_model=der_wunderfizz_disabled_model())

    # Power switch / breaker box (vanilla textures). "_on" shares the box geometry but flips the
    # lever to the down position and recolors the handle + indicator light to green/lit.
    Item(id="power_switch", override_model=load_model(get_model_path("power_switch")))
    Item(id="power_switch_on", override_model=power_switch_on_model())

    # Turret trap (vanilla textures), split into a stationary base + a rotating head so the head
    # can be aimed at the zombie it is shooting (see zombies/traps.py turret_fire). The head model
    # is built centred on [8,8,8] with barrels along +Z so a fixed item_display facing-entity
    # rotation points the barrels at the target.
    Item(id="turret_base", override_model=load_model(get_model_path("turret_base")))
    Item(id="turret_head", override_model=load_model(get_model_path("turret_head")))

