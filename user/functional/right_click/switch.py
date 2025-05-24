
# Imports
from typing import Any

from python_datapack.utils.database_helper import write_item_modifier, write_versioned_function

from user.config.stats import SWITCH, WEAPON_ID, json_dump


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    ## TODO: idea switch warped_fungus_on_a_stick with carrot_on_a_stick and opposite to reset hand animation
    # Weapon switching main function
    write_versioned_function(config, "switch/main",
f"""
# Set weapon id if not done yet
execute if data storage {ns}:gun all.stats unless data storage {ns}:gun all.stats.{WEAPON_ID} run function {ns}:v{version}/switch/set_weapon_id

# If last_selected is different from this one, set cooldown
scoreboard players set #current_id {ns}.data 0
execute store result score #current_id {ns}.data run data get storage {ns}:gun all.stats.{WEAPON_ID}
execute unless score @s {ns}.last_selected = #current_id {ns}.data run function {ns}:v{version}/switch/on_weapon_switch

# Update last selected
scoreboard players operation @s {ns}.last_selected = #current_id {ns}.data
""")

    # Set weapon id function and item modifier
    write_versioned_function(config, "switch/set_weapon_id",
f"""
execute store result storage {ns}:gun all.stats.{WEAPON_ID} int 1 run scoreboard players add #next_id {ns}.data 1
item modify entity @s weapon.mainhand {ns}:v{version}/set_weapon_id
""")

    # On weapon switch function
    write_versioned_function(config, "switch/on_weapon_switch",
f"""
# Apply weapon switch cooldown only if it exceeds the current cooldown value
execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{SWITCH}
execute if score #cooldown {ns}.data > @s {ns}.cooldown run scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data
""")

    modifier: dict[str, Any] = {
        "function": "minecraft:copy_custom_data",
        "source": {
            "type": "minecraft:storage",
            "source": f"{ns}:gun"
        },
        "ops": [
            {
                "source": f"all.stats.{WEAPON_ID}",
                "target": f"{ns}.stats.{WEAPON_ID}",
                "op": "replace"
            }
        ]
    }
    write_item_modifier(config, f"{ns}:v{version}/set_weapon_id", json_dump(modifier))
