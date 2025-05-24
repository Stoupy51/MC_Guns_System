
# Imports
from typing import Any

from python_datapack.utils.database_helper import write_item_modifier, write_versioned_function

from user.config.stats import CAPACITY, RELOAD_END, RELOAD_TIME, REMAINING_BULLETS, json_dump


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle right click event by decreasing ammo count
    write_versioned_function(config, "player/right_click",
f"""
# Decrease bullet count
function {ns}:v{version}/ammo/decrease
""")

    # Decrease ammo count function
    write_versioned_function(config, "ammo/decrease",
f"""
# Remove 1 bullet from player's ammo count
scoreboard players remove @s {ns}.{REMAINING_BULLETS} 1
""")

    # Handle weapon switching logic
    write_versioned_function(config, "switch/on_weapon_switch",
f"""
# When unequipping a weapon (player was holding a weapon):
#   - Find weapon with CURRENT_AMMO = -1 (needs update)
#   - Store current ammo count in weapon's stats
execute if score @s {ns}.last_selected matches 1.. run function {ns}:v{version}/ammo/update_old_weapon

# When equipping a new weapon:
#   - Load ammo count from weapon's stats into player scoreboard
#   - Mark weapon as needing update by setting ammo to -1
execute if score #current_id {ns}.data matches 1.. run function {ns}:v{version}/ammo/copy_data
""")

    # Update ammo count for previously equipped weapon
    custom_data = f"{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}"
    content: str = f"""
# Store player's current ammo count in temporary storage
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

# Check all inventory slots for weapon needing ammo update (remaining bullets = -1)
"""
    for slot in (
        *[f"hotbar.{i}" for i in range(9)],
        "weapon.offhand",
        *[f"container.{i}" for i in range(4*9)],
        "player.cursor",
        *[f"player.crafting.{i}" for i in range(4)],
    ):
        content += f"""execute if items entity @s {slot} *[custom_data~{custom_data}] run return run function {ns}:v{version}/ammo/set_count {{slot:"{slot}"}}\n"""
    write_versioned_function(config, "ammo/update_old_weapon", content)

    # Create item modifier to update weapon's ammo count
    modifier: dict[str, Any] = {
        "function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:temp"},
        "ops":[{"source":REMAINING_BULLETS,"target":f"{ns}.stats.{REMAINING_BULLETS}","op":"replace"}]
    }
    write_item_modifier(config, f"{ns}:v{version}/update_ammo", json_dump(modifier))

    # Update weapon's ammo count and lore
    write_versioned_function(config, "ammo/set_count",
f"""
# Apply new ammo count to weapon
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update weapon's lore to show new ammo count
$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

    # Load ammo data from newly equipped weapon
    write_versioned_function(config, "ammo/copy_data",
f"""
# Load ammo count from weapon into player's scoreboard (if different from -1)
execute store result score #count {ns}.data run data get storage {ns}:gun all.stats.{REMAINING_BULLETS}
execute unless score #count {ns}.data matches -1 run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #count {ns}.data

# Mark weapon as needing update
data modify storage {ns}:gun all.stats.{REMAINING_BULLETS} set value -1
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

    # Update weapon's lore to show current ammo count
    write_versioned_function(config, "ammo/modify_lore",
f"""
## In this context, @s has the right amount of bullets in {ns}.{REMAINING_BULLETS}
# Add temporary tag for item display targeting
tag @s add {ns}.modify_lore

# Get current weapon lore
$execute summon item_display run function {ns}:v{version}/ammo/get_current_lore {{"slot":"$(slot)"}}

# Find and update ammo count in lore
scoreboard players set #index {ns}.data 0
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_lore_loop {{"slot":"$(slot)"}}

# Clean up temporary tag
tag @s remove {ns}.modify_lore
""")

    # Get current weapon lore for modification
    write_versioned_function(config, "ammo/get_current_lore",
f"""
# Copy weapon to item display entity
$item replace entity @s contents from entity @p[tag={ns}.modify_lore] $(slot)

# Extract lore data
data modify storage {ns}:temp components set from entity @s item.components
data modify storage {ns}:temp lore set from storage {ns}:temp components."minecraft:lore"
data modify storage {ns}:temp copy set from storage {ns}:temp lore

# Clean up item display
kill @s
""")

    # Search for ammo count line in lore
    write_versioned_function(config, "ammo/search_lore_loop",
f"""
# Check if current lore line matches ammo format (number/number)
scoreboard players set #success {ns}.data 0
data modify storage {ns}:temp lore_extra set from storage {ns}:temp copy[0].extra
data modify storage {ns}:temp lore_slash set from storage {ns}:temp lore_extra[-2]
execute if data storage {ns}:temp lore_slash{{"text":"/"}} unless data storage {ns}:temp lore_extra[-3].text unless data storage {ns}:temp lore_extra[-1].text run scoreboard players set #success {ns}.data 1

# If ammo line found, prepare data for modification
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with set value {{}}
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.index int 1 run scoreboard players get #index {ns}.data
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.{REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.{CAPACITY} set from storage {ns}:temp components."minecraft:custom_data".{ns}.stats.{CAPACITY}
$execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.slot set value "$(slot)"
execute if score #success {ns}.data matches 1 summon item_display run return run function {ns}:v{version}/ammo/found_line with storage {ns}:input with

# Continue searching if not found
data remove storage {ns}:temp copy[0]
scoreboard players add #index {ns}.data 1
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_lore_loop {{"slot":"$(slot)"}}
""")  # noqa: E501

    # Update ammo count in weapon lore
    write_versioned_function(config, "ammo/found_line",
f"""
# Copy weapon to item display for modification
$item replace entity @s contents from entity @p[tag={ns}.modify_lore] $(slot)

# Update ammo count in lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$({CAPACITY})"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$({REMAINING_BULLETS})"

# Copy modified weapon back to player
$item replace entity @p[tag={ns}.modify_lore] $(slot) from entity @s contents

# Clean up item display
kill @s
""")

    # Reload weapon function (not implemented)
    write_versioned_function(config, "ammo/reload",
f"""
# Set cooldown to reload duration
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{RELOAD_TIME}

# Get the new ammo count
# TODO: Find ammo in inventory and don't take it out for your ass
execute store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}

# Play reload sound (and send stats for macro)
function {ns}:v{version}/sound/reload_start with storage {ns}:gun all.stats

# Add reloading tag
tag @s add {ns}.reloading
""")

