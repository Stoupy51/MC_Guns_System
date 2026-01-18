
# Imports
import json

import stouputils as stp
from stewbeet import Item, Mem

from ..config.stats import get_model_path


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
            Item(
                id=item,
                override_model=json.loads(stp.read_file(get_model_path(item)).replace("mgs:item", f"{Mem.ctx.project_id}:item")),
                components={"max_stack_size": 1, "custom_data": {ns: {"magazine": True, "weapon": weapon, "bullets": capacity}}}
            )

