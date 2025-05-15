
# Imports
import stouputils as stp
from python_datapack.utils.database_helper import write_advancement, write_versioned_function

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

    # Handle pending clicks
    write_versioned_function(config, "player/tick",
f"""
# If pending clicks, run function
execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1
execute if score @s {ns}.pending_clicks matches 1.. run function {ns}:v{version}/player/right_click
""")

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Decrease pending clicks by 1 and stop if cooldown
scoreboard players remove @s {ns}.pending_clicks 1
execute if score @s {ns}.cooldown matches 1.. run return fail

# Copy gun data, stop if SelectedItem is not a gun
data remove storage {ns}:gun stats
data modify storage {ns}:gun stats set from entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats
execute unless data storage {ns}:gun stats run return fail

# Set cooldown
execute store result score @s {ns}.cooldown run data get storage {ns}:gun stats.{COOLDOWN}
""")

