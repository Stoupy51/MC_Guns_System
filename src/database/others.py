
# Imports
import copy

from stewbeet import Item, JsonDict

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


def power_switch_on_model() -> JsonDict:
    """ "On" breaker model: same box as the base, but the lever is flipped to the DOWN position
    and the handle + indicator light recolored green/lit. The lever bar is physically mirrored
    about the housing pivot (y=7) and tilted forward-down, because Minecraft caps element
    rotations at ±45° and so the bar can't simply be rotated 180° from the up (off) position. """
    model: JsonDict = copy.deepcopy(load_model(get_model_path("power_switch")))
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

    # Add Pack-a-Punch
    Item(id="pack_a_punch", override_model=load_model(get_model_path("pack_a_punch")))

    # Mystery Box crate (vanilla textures), split into base + lid so the lid can animate open.
    Item(id="mystery_box_base", override_model=load_model(get_model_path("mystery_box_base")))
    Item(id="mystery_box_lid", override_model=load_model(get_model_path("mystery_box_lid")))

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


