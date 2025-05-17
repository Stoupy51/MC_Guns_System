
# Imports
from typing import Any

import stouputils as stp
from python_datapack.utils.database_helper import write_advancement, write_item_modifier, write_predicate, write_versioned_function

from user.config.stats import COOLDOWN


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

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
            "function": f"{ns}:v{version}/player/set_pending_clicks"
        }
    }
    write_advancement(config, f"{ns}:v{version}/right_click", stp.super_json_dump(adv, max_level=-1))

    # Function to set pending clicks
    write_versioned_function(config, "player/set_pending_clicks",
f"""

# Revoke advancement and reset right click
advancement revoke @s only {ns}:v{version}/right_click
scoreboard players reset @s {ns}.right_click

# Set pending clicks
scoreboard players set @s {ns}.pending_clicks 4
""")

    # Player tick function
    write_versioned_function(config, "player/tick",
f"""
# Add temporary tag
tag @s add {ns}.ticking

# Copy gun data
data remove storage {ns}:gun stats
data modify storage {ns}:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats

# Check if we need to zoom weapon or stop
execute if data storage {ns}:gun stats run function {ns}:v{version}/zoom/main

# If pending clicks, run function
execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1
execute if score @s {ns}.pending_clicks matches 1.. run function {ns}:v{version}/player/right_click

# Remove temporary tag
tag @s remove {ns}.ticking
""")

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Decrease pending clicks by 1 and stop if cooldown
scoreboard players remove @s {ns}.pending_clicks 1
execute if score @s {ns}.cooldown matches 1.. run return fail

# Stop if SelectedItem is not a gun
execute unless data storage {ns}:gun stats run return fail

# Set cooldown
execute store result score @s {ns}.cooldown run data get storage {ns}:gun stats.{COOLDOWN}
""")

    # Prepare predicates for movement checks
    # (Can't use flag 'is_on_ground' because /tp @s ~ ~ ~ makes it false for two ticks)
    write_predicate(config, f"{ns}:v{version}/is_on_ground", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"vertical_speed":{"max":0.1}}}}))
    write_predicate(config, f"{ns}:v{version}/is_sprinting", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sprinting":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_sneaking", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sneaking":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_moving", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"horizontal_speed":{"min":0.1}}}}))

    # Handle zoom
    write_versioned_function(config, "zoom/main",
f"""
# If already zoom and not sneaking, unzoom
execute if data storage {ns}:gun stats.is_zoom unless predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage {ns}:gun stats.is_zoom if predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/set
""")
    write_versioned_function(config, "zoom/remove",
f"""
data remove storage {ns}:gun stats.is_zoom
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun stats.models.normal
function {ns}:v{version}/zoom/update_model with storage {ns}:input with
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")
    write_versioned_function(config, "zoom/set",
f"""
data modify storage {ns}:gun stats.is_zoom set value 1b
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun stats.models.zoom
function {ns}:v{version}/zoom/update_model with storage {ns}:input with
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

    # Update weapon stats item modifier
    modifier: dict[str, Any] = {"function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:gun"},"ops":[{"source":"stats","target":f"{ns}.stats","op":"replace"}]}
    write_item_modifier(config, f"{ns}:v{version}/update_stats", stp.super_json_dump(modifier))

    # Update weapon model item modifier
    write_versioned_function(config, "zoom/update_model", """
$item modify entity @s weapon.mainhand {"function": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}
""")

