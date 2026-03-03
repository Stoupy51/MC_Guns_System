
# Imports
import json

import stouputils as stp
from stewbeet import Item, Mem

from ..config.stats import CAPACITY, REMAINING_BULLETS, get_model_path


# Main function should return a database
def main() -> None:
    ns = Mem.ctx.project_id

    # Magazine definitions: (weapon, capacity)
    magazines = [
        ("ak47", 30),
        ("aug", 30),
        ("deagle", 7),
        ("famas", 25),
        ("fnfal", 20),
        ("g3a3", 20),
        ("glock17", 17),
        ("glock18", 19),
        ("m16a4", 30),
        ("m1911", 7),
        ("m249", 150),
        ("m4a1", 30),
        ("m82", 10),
        ("m9", 15),
        ("mac10", 30),
        ("makarov", 8),
        ("mp5", 30),
        ("mp7", 40),
        ("ppsh41", 71),
        ("rpk", 75),
        ("scar17", 20),
        ("sten", 32),
        ("svd", 10),
        ("vz61", 20),
    ]

    # Add magazine items
    for weapon, capacity in magazines:
        for is_empty in (False, True):
            suffix = "_empty" if is_empty else ""
            item: str = f"{weapon}_mag{suffix}"
            bullets = 0 if is_empty else capacity
            Item(
                id=item,
                override_model=json.loads(stp.read_file(get_model_path(item)).replace("mgs:item", f"{Mem.ctx.project_id}:item")),
                components={
                    "max_stack_size": 1,
                    "custom_data": {ns: {"magazine": True, "weapon": weapon, "stats": {REMAINING_BULLETS: bullets, CAPACITY: capacity}}}
                }
            )

    # Add consumable magazine items (cleared from inventory when depleted)
    # These are individual bullets/shells that stack, each representing 1 round.
    # When reloading, the system consumes items from the stack (not the whole stack).
    consumable_magazines: list[tuple[str, str, int]] = [
        ("rpg7", "rpg7_rocket", 1),
        ("mosin", "mosin_bullet", 1),
        ("m24", "m24_bullet", 1),
        ("spas12", "spas12_shell", 1),
        ("m500", "m500_shell", 1),
        ("m590", "m590_shell", 1),
    ]
    for weapon, item_name, capacity in consumable_magazines:
        Item(
            id=item_name,
            override_model=json.loads(stp.read_file(get_model_path(item_name)).replace("mgs:item", f"{Mem.ctx.project_id}:item")),
            components={
                "max_stack_size": 64,
                "custom_data": {ns: {"magazine": True, "consumable": True, "weapon": weapon, "stats": {REMAINING_BULLETS: capacity, CAPACITY: capacity}}}
            }
        )

