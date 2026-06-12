
# Imports
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

# Main function should return a database
def main() -> None:

    # Add Pack-a-Punch
    Item(id="pack_a_punch", override_model=load_model(get_model_path("pack_a_punch")))

    # Generic perk machine (vanilla textures) + per-perk recolors.
    # New perks only need a small child model overriding the "accent"/"accent2" textures
    # (see perk_machine_juggernog.json) and a default line in zombies/perks.py setup_iter.
    Item(id="perk_machine", override_model=load_model(get_model_path("perk_machine")))
    Item(id="perk_machine_juggernog", override_model=override_model("red"))
    Item(id="perk_machine_speed_cola", override_model=override_model("lime"))
    Item(id="perk_machine_double_tap", override_model=override_model("yellow"))
    Item(id="perk_machine_quick_revive", override_model=override_model("light_blue"))
    Item(id="perk_machine_mule_kick", override_model=override_model("green"))


