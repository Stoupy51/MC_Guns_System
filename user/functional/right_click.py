
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
data remove storage {ns}:gun stats
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
tag @s add {ns}.attacker
execute anchored eyes positioned ^ ^ ^ run function #bs.raycast:run with storage {ns}:input
tag @s remove {ns}.attacker

# TODO: Advanced Playsound
playsound stoupgun:ak47/fire player @s ~ ~1000000 ~ 400000
playsound stoupgun:ak47/fire player @a[distance=0.01..48] ~ ~ ~ 3
""")

    # On hit point
    write_versioned_function(config, "raycast/on_hit_point",
f"""
# Get current block
data modify storage {ns}:temp Pos set from entity @s Pos
data modify entity @s Pos set from storage bs:lambda raycast.targeted_block
execute at @s run function #bs.block:get_block
data modify entity @s Pos set from storage {ns}:temp Pos

# Make block particles
data modify storage {ns}:input with set value {{x:0,y:0,z:0,block:"minecraft:air"}}
data modify storage {ns}:input with.block set from storage bs:out block.type
data modify storage {ns}:input with.x set from storage bs:lambda raycast.hit_point[0]
data modify storage {ns}:input with.y set from storage bs:lambda raycast.hit_point[1]
data modify storage {ns}:input with.z set from storage bs:lambda raycast.hit_point[2]
execute unless data storage {ns}:input with{{block:"minecraft:air"}} run return run function {ns}:v{version}/raycast/block_particles with storage {ns}:input with
""")

    # On targeted block
    write_versioned_function(config, "raycast/on_targeted_block",
f"""
# Allow bullets to pierce 2 blocks at most
execute if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 4
execute if score $raycast.piercing bs.lambda matches 1..4 run scoreboard players remove $raycast.piercing bs.lambda 1

# Divide damage per 2
execute store result storage {ns}:gun stats.damage float 0.5 run data get storage {ns}:gun stats.damage

execute if block ~ ~ ~ #{ns}:v{version}/sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute if block ~ ~ ~ #{ns}:v{version}/sounds/cloth run playsound {ns}:common.cloth_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/dirt run playsound {ns}:common.dirt_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/mud run playsound {ns}:common.mud_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/wood run playsound {ns}:common.wood_bullet_impact block @a ~ ~ ~ 1
""")
    write_versioned_function(config, "raycast/block_particles", """$particle block{block_state:"$(block)"} $(x) $(y) $(z) 0.1 0.1 0.1 1 10 force @a[distance=..128]""")

    # On targeted entity
    write_versioned_function(config, "raycast/on_targeted_entity",
f"""
# Blood particles
particle block{{block_state:"redstone_wire"}} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Is headshot? (#FIXME: hit_point is updated after function call)
scoreboard players set #is_headshot {ns}.data 0
execute store result score #entity_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #hit_y {ns}.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff {ns}.data = #hit_y {ns}.data
scoreboard players operation #y_diff {ns}.data -= #entity_y {ns}.data
execute if score #y_diff {ns}.data matches 1500.. run scoreboard players set #is_headshot {ns}.data 1
#execute if score #is_headshot {ns}.data matches 1 run say Headshot!

# Damage entity
data modify storage {ns}:input with set value {{target:"@s", amount:0.0d, attacker:"@p[tag={ns}.attacker]"}}
execute if score #is_headshot {ns}.data matches 1 store result storage {ns}:input with.amount float 1.0 run data get storage {ns}:gun stats.damage
execute if score #is_headshot {ns}.data matches 0 store result storage {ns}:input with.amount float 0.5 run data get storage {ns}:gun stats.damage
function {ns}:v{version}/utils/damage with storage {ns}:input with
""")

