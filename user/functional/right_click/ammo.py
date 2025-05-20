
# Imports
from typing import Any

from python_datapack.utils.database_helper import write_item_modifier, write_versioned_function

from user.config.stats import CAPACITY, RELOAD_END, RELOAD_TIME, REMAINING_BULLETS, json_dump


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Decrease bullet count
function {ns}:v{version}/ammo/decrease
""")

    # Main function
    write_versioned_function(config, "ammo/decrease",
f"""
# Decrease ammo count
scoreboard players remove @s {ns}.{REMAINING_BULLETS} 1
""")

    # On weapon switch function
    write_versioned_function(config, "switch/on_weapon_switch",
f"""
# 1. When unequipping a weapon (`if score @s {ns}.last_selected matches 1..` means player was holding a weapon)
#   - Find the weapon with CURRENT_AMMO set to -1 (meaning not updated)
#   - Set the score @s {ns}.{REMAINING_BULLETS} into this weapon's stats.{REMAINING_BULLETS}
execute if score @s {ns}.last_selected matches 1.. run function {ns}:v{version}/ammo/update_old_weapon

# 2. When equipping a weapon (current weapon id):
#   - Copy stats.{REMAINING_BULLETS} into @s {ns}.{REMAINING_BULLETS}
#   - Set stats.{REMAINING_BULLETS} to -1 (indicating it needs to be updated)
execute if score #current_id {ns}.data matches 1.. run function {ns}:v{version}/ammo/copy_data
""")

    # Find old weapon and set the remaining bullets
    custom_data = f"{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}"
    content: str = f"""
# Store the current bullet count from the player's scoreboard into the weapon's stats
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

# For each slot, if remaining bullets is -1, update it
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

    # Update weapon stats item modifier
    modifier: dict[str, Any] = {
        "function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:temp"},
        "ops":[{"source":REMAINING_BULLETS,"target":f"{ns}.stats.{REMAINING_BULLETS}","op":"replace"}]
    }
    write_item_modifier(config, f"{ns}:v{version}/update_ammo", json_dump(modifier))

    # Set remaining bullets function
    write_versioned_function(config, "ammo/set_count",
f"""
# Item modifier to apply the new remaining bullets count
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Modify gun lore
$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

    # Copy gun data
    write_versioned_function(config, "ammo/copy_data",
f"""
# Copy the number of remaining bullets
execute store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{REMAINING_BULLETS}

# Set remaining bullets to -1 to mark this weapon as needing an update
data modify storage {ns}:gun all.stats.{REMAINING_BULLETS} set value -1
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

    # Lore function
    write_versioned_function(config, "ammo/modify_lore",
f"""
## In this context, @s has the right amount of bullets in {ns}.{REMAINING_BULLETS}
# Temporary tag
tag @s add {ns}.modify_lore

# Copy item lore
$execute summon item_display run function {ns}:v{version}/ammo/get_current_lore {{"slot":"$(slot)"}}

# Find the ammo line and modify it
scoreboard players set #index {ns}.data 0
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_lore_loop {{"slot":"$(slot)"}}

# Remove temporary tag
tag @s remove {ns}.modify_lore
""")

    # Get lore function
    write_versioned_function(config, "ammo/get_current_lore",
f"""
# Copy item lore
$item replace entity @s contents from entity @p[tag={ns}.modify_lore] $(slot)
data modify storage {ns}:temp components set from entity @s item.components
data modify storage {ns}:temp lore set from storage {ns}:temp components."minecraft:lore"
data modify storage {ns}:temp copy set from storage {ns}:temp lore

# Kill item display
kill @s
""")

    # Search the damn line
    write_versioned_function(config, "ammo/search_lore_loop",
f"""
# Check if lore finishes by format `number/number`, ex: "30", {{"text":"/"}}, "30"
scoreboard players set #success {ns}.data 0
data modify storage {ns}:temp lore_extra set from storage {ns}:temp copy[0].extra
data modify storage {ns}:temp lore_slash set from storage {ns}:temp lore_extra[-2]
execute if data storage {ns}:temp lore_slash{{"text":"/"}} unless data storage {ns}:temp lore_extra[-3].text unless data storage {ns}:temp lore_extra[-1].text run scoreboard players set #success {ns}.data 1

# If it is, prepare arguments and modify the line
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with set value {{}}
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.index int 1 run scoreboard players get #index {ns}.data
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.{REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.{CAPACITY} set from storage {ns}:temp components."minecraft:custom_data".{ns}.stats.{CAPACITY}
$execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.slot set value "$(slot)"
execute if score #success {ns}.data matches 1 summon item_display run return run function {ns}:v{version}/ammo/found_line with storage {ns}:input with

# Continue loop if not
data remove storage {ns}:temp copy[0]
scoreboard players add #index {ns}.data 1
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_lore_loop {{"slot":"$(slot)"}}
""")

    # Get lore function
    write_versioned_function(config, "ammo/found_line",
f"""
# Copy item to the item display
$item replace entity @s contents from entity @p[tag={ns}.modify_lore] $(slot)

# Modify lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$({CAPACITY})"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$({REMAINING_BULLETS})"

# Copy back the item to the player
$item replace entity @p[tag={ns}.modify_lore] $(slot) from entity @s contents

# Kill item display
kill @s
""")

    # Reload function
    write_versioned_function(config, "ammo/reload",
f"""
# TODO {CAPACITY} {RELOAD_TIME} {RELOAD_END}
# scoreboard players set ak47_mag S 30           # TODO: Not Implemented
# scoreboard players set ak47_reload S 70        # TODO: Not Implemented
# scoreboard players set ak47_reload_end S 10    # TODO: Not Implemented
""")

