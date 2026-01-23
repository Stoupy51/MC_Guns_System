
# Imports
from typing import Any

import orjson
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...database.flash import flash_models


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle pending clicks
    # TODO: fix flash bug where they don't appear sometimes (probably because the server kills them too fast before the client can render them)
    write_versioned_function("player/right_click",
f"""
# Summon flash
function {ns}:v{version}/flash/summon
""")

    # Function to get summon NBT
    def get_item(model: str):
        nbt: dict[str, Any] = {}
        nbt["item"] = {"id":"minecraft:white_stained_glass_pane", "count":1, "components":{"minecraft:item_model":f"{ns}:{model}"}}
        nbt["Tags"] = [f"{ns}.flash"]
        nbt["billboard"] = "center"
        nbt["transformation"] = {
            "left_rotation": [0.0, 0.0, 0.0, 1.0],
            "right_rotation": [0.0, 0.0, 0.0, 1.0],
            "translation": [0.0, 0.0, 0.0],
            "scale": [0.5, 0.5, 0.000001]  # Flat item
        }
        nbt["brightness"] = {"block": 15, "sky": 15}
        return orjson.dumps(nbt).decode("utf-8")

    # Summon function
    summons: list[str] = []
    for i, model in enumerate(flash_models):
        summons.append(f"execute if score #random {ns}.data matches {i+1} if predicate {ns}:v{version}/is_sneaking anchored eyes run summon item_display ^ ^-0.1 ^0.5 {get_item(model)}")
        summons.append(f"execute if score #random {ns}.data matches {i+1} unless predicate {ns}:v{version}/is_sneaking anchored eyes run summon item_display ^-0.1 ^-0.1 ^0.5 {get_item(model)}")
    write_versioned_function("flash/summon",
f"""
# Take a random number between 1 and len(flash_models)
execute store result score #random {ns}.data run random value 1..{len(flash_models)}

# Summon a random flash texture
{'\n'.join(summons)}

# Increment flash entity counter
scoreboard players add #flash_count {ns}.data 1
""")

    # Tick function
    write_versioned_function("flash/tick",
f"""
# Decrement life time
scoreboard players remove @s {ns}.data 1

# Kill flash after 1 tick (50 ms)
execute if score @s {ns}.data matches -2 run function {ns}:v{version}/flash/delete
""")

    # Kill function
    write_versioned_function("flash/delete",
f"""
# Decrease flash entity counter and kill entity
scoreboard players remove #flash_count {ns}.data 1
kill @s
""")

    # Run function every tick
    write_tick_file(
f"""
# Tick function for flashes
execute if score #flash_count {ns}.data matches 1.. as @e[tag={ns}.flash] run function {ns}:v{version}/flash/tick
""")

