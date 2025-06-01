
# Imports
from typing import Any

import orjson
from python_datapack.utils.database_helper import write_tick_file, write_versioned_function

from user.database.flash import flash_models


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
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
    summon_commands: list[str] = []
    for i, model in enumerate(flash_models):
        summon_commands.append(f"execute if score #random {ns}.data matches {i+1} if predicate {ns}:v{version}/is_sneaking anchored eyes run summon item_display ^ ^-0.1 ^0.5 {get_item(model)}")
        summon_commands.append(f"execute if score #random {ns}.data matches {i+1} unless predicate {ns}:v{version}/is_sneaking anchored eyes run summon item_display ^-0.1 ^-0.1 ^0.5 {get_item(model)}")
    write_versioned_function(config, "flash/summon",
f"""
# Take a random number between 1 and len(flash_models)
execute store result score #random {ns}.data run random value 1..{len(flash_models)}

# Summon a random flash texture
{'\n'.join(summon_commands)}

# Increment flash entity counter
scoreboard players add #flash_count {ns}.data 1
""")

    # Tick function
    write_versioned_function(config, "flash/tick",
f"""
# Decrement life time
scoreboard players remove @s {ns}.data 1

# Kill flash after 1 tick (50 ms)
execute if score @s {ns}.data matches -2 run function {ns}:v{version}/flash/delete
""")

    # Kill function
    write_versioned_function(config, "flash/delete",
f"""
# Decrease flash entity counter and kill entity
scoreboard players remove #flash_count {ns}.data 1
kill @s
""")

    # Run function every tick
    write_tick_file(config,
f"""
# Tick function for flashes
execute if score #flash_count {ns}.data matches 1.. as @e[tag={ns}.flash] run function {ns}:v{version}/flash/tick
""")

