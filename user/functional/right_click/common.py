
# Imports
from typing import Any

from python_datapack.utils.database_helper import write_advancement, write_item_modifier, write_predicate, write_versioned_function

from user.config.stats import COOLDOWN, REMAINING_BULLETS, json_dump


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
    write_advancement(config, f"{ns}:v{version}/right_click", json_dump(adv))

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
data remove storage {ns}:gun all
data modify storage {ns}:gun all set from entity @s SelectedItem.components."minecraft:custom_data".{ns}

# Check if we need to zoom weapon or stop
function {ns}:v{version}/zoom/main

# Check if switching weapon
function {ns}:v{version}/switch/main

# If pending clicks, run function
execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1
execute if score @s {ns}.pending_clicks matches -100.. run function {ns}:v{version}/player/right_click

# TODO: Title action bar that shows bullet icons (grayed = no bullet) instead of count/max_count

# Remove temporary tag
tag @s remove {ns}.ticking
""")

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Decrease pending clicks by 1
scoreboard players remove @s {ns}.pending_clicks 1

# If player stopped right clicking for 1 second, we update the item lore
execute if score @s {ns}.pending_clicks matches -20 run function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}

# Stop here is weapon cooldown OR pending clicks if negative
execute if score @s {ns}.cooldown matches 1.. run return fail
execute if score @s {ns}.pending_clicks matches ..-1 run return fail

# Stop if SelectedItem is not a gun or if not enough ammo
execute unless data storage {ns}:gun all.stats run return fail
execute if score @s {ns}.{REMAINING_BULLETS} matches ..0 run return run function {ns}:v{version}/ammo/reload

# Set cooldown
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{COOLDOWN}
""")

    # Prepare predicates for movement checks
    # (Can't use flag 'is_on_ground' because /tp @s ~ ~ ~ makes it false for two ticks)
    write_predicate(config, f"{ns}:v{version}/is_on_ground", json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"vertical_speed":{"max":0.1}}}}))
    write_predicate(config, f"{ns}:v{version}/is_sprinting", json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sprinting":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_sneaking", json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sneaking":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_moving", json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"horizontal_speed":{"min":0.1}}}}))

    # Update weapon stats item modifier
    modifier: dict[str, Any] = {"function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:gun"},"ops":[{"source":"all.stats","target":f"{ns}.stats","op":"replace"}]}
    write_item_modifier(config, f"{ns}:v{version}/update_stats", json_dump(modifier))

    # Update weapon model item modifier
    write_versioned_function(config, "utils/update_model", """
$item modify entity @s weapon.mainhand {"function": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}
""")

