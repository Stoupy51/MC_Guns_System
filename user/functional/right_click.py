
# Imports
import stouputils as stp
from python_datapack.utils.database_helper import *

from user.config.stats import *


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]
    pass

    # Right click = 4

    # Advancement detecting right click
    adv: dict = {
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {"condition": "minecraft:entity_scores","entity": "this","scores": {f"{ns}.right_click": {"min": 1}}}
                    ]
                }
            }
        },
        "rewards": {
            "function": f"{ns}:v{version}/right_click/set_pending_clicks"
        }
    }
    write_advancement(config, f"{ns}:v{version}/right_click", stp.super_json_dump(adv, max_level=-1))

    # Function to set pending clicks
    write_versioned_function(config, "right_click/set_pending_clicks",
f"""
# Revoke advancement
advancement revoke @s only {ns}:v{version}/right_click

# Set pending clicks and reset right click
scoreboard players set @s {ns}.pending_clicks 1
scoreboard players reset @s {ns}.right_click
""")

    # Handle pending clicks
    write_versioned_function(config, "player/tick",
f"""
# If pending clicks, run function
execute if score @s {ns}.pending_clicks matches 1.. run function {ns}:v{version}/right_click/handle
""")

    # Handle pending clicks
    write_versioned_function(config, "right_click/handle",
f"""
# Decrease pending clicks by 1
scoreboard players remove @s {ns}.pending_clicks 1

# If SelectedItem is not a gun, stop
data modify storage {ns}:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats
execute unless data storage {ns}:gun stats run return fail

## Raycast (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html)
# Prepare arguments
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value true
data modify storage {ns}:input with.entities set value true
data modify storage {ns}:input with.piercing set value 10
data modify storage {ns}:input with.max_distance set value 128
data modify storage {ns}:input with.hitbox_shape set value "interaction"
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/air"
data modify storage {ns}:input with.on_hit_point set value "function {ns}:v{version}/raycast/on_hit_point"
data modify storage {ns}:input with.on_targeted_block set value "function {ns}:v{version}/raycast/on_targeted_block"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/raycast/on_targeted_entity"

# Run raycast with callbacks
execute anchored eyes positioned ^ ^ ^ run function #bs.raycast:run with storage {ns}:input

# TODO: Advanced Playsound
playsound stoupgun:ak47/fire player @s ~ ~1000000 ~ 400000
playsound stoupgun:ak47/fire player @a[distance=0.01..48] ~ ~ ~ 3

# Remove storage
data remove storage {ns}:gun stats
""")

    # On hit point
    write_versioned_function(config, "raycast/on_hit_point",
"""
particle happy_villager ~ ~ ~ 0 0 0 0 10
""")

    # On targeted block
    write_versioned_function(config, "raycast/on_targeted_block",
f"""
particle angry_villager ~ ~ ~ 0 0 0 0 10

# Allow bullets to pierce 2 blocks at most
execute if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 4
execute if score $raycast.piercing bs.lambda matches 1..4 run scoreboard players remove $raycast.piercing bs.lambda 1

execute if block ~ ~ ~ #{ns}:v{version}/sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute if block ~ ~ ~ #{ns}:v{version}/sounds/cloth run playsound {ns}:common.cloth_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/dirt run playsound {ns}:common.dirt_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/mud run playsound {ns}:common.mud_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/wood run playsound {ns}:common.wood_bullet_impact block @a ~ ~ ~ 1
""")

    # On targeted entity
    write_versioned_function(config, "raycast/on_targeted_entity",
"""
particle heart ~ ~ ~ 0 0 0 0 10
say entity hit
""")

