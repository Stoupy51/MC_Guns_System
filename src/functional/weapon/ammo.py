
# Imports
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from ...config.stats import ALL_SLOTS, BASE_WEAPON, CAPACITY, RELOAD_TIME, REMAINING_BULLETS


def create_lore_functions(type_name: str, tag: str, remaining_source: str, capacity_source: str) -> None:
    """ Create lore modification functions for weapons or magazines.

    Args:
        type_name        (str): Type name for the lore functions (e.g., "lore" or "mag_lore").
        tag              (str): Temporary tag to identify the item being modified.
        remaining_source (str): Source to get the remaining bullets value.
        capacity_source  (str): Source to get the capacity value.
    """
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Modify lore function
    write_versioned_function(f"ammo/modify_{type_name}",
f"""
# Add temporary tag for item display targeting
tag @s add {tag}

# Get current item lore
$execute summon item_display run function {ns}:v{version}/ammo/get_current_{type_name} {{"slot":"$(slot)"}}

# Find and update ammo count in lore
scoreboard players set #index {ns}.data 0
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}

# Clean up temporary tag
tag @s remove {tag}
""")

    # Get current item lore
    write_versioned_function(f"ammo/get_current_{type_name}",
f"""
# Copy item to item display entity
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

# Extract lore data
data modify storage {ns}:temp components set from entity @s item.components
data modify storage {ns}:temp lore set from storage {ns}:temp components."minecraft:lore"
data modify storage {ns}:temp copy set from storage {ns}:temp lore

# Clean up item display
kill @s
""")

    # Search for ammo line in lore
    write_versioned_function(f"ammo/search_{type_name}_loop",
f"""
# Check if current lore line matches ammo format (number/number)
scoreboard players set #success {ns}.data 0
data modify storage {ns}:temp lore_extra set from storage {ns}:temp copy[0].extra
data modify storage {ns}:temp lore_slash set from storage {ns}:temp lore_extra[-2]
execute if data storage {ns}:temp lore_slash{{"text":"/"}} unless data storage {ns}:temp lore_extra[-3].text unless data storage {ns}:temp lore_extra[-1].text run scoreboard players set #success {ns}.data 1

# If ammo line found, prepare data for modification
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with set value {{}}
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.index int 1 run scoreboard players get #index {ns}.data
execute if score #success {ns}.data matches 1 store result storage {ns}:input with.{REMAINING_BULLETS} int 1 run scoreboard players get {remaining_source}
execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.{CAPACITY} set from {capacity_source}
$execute if score #success {ns}.data matches 1 run data modify storage {ns}:input with.slot set value "$(slot)"
execute if score #success {ns}.data matches 1 summon item_display run return run function {ns}:v{version}/ammo/found_{type_name}_line with storage {ns}:input with

# Continue searching if not found
data remove storage {ns}:temp copy[0]
scoreboard players add #index {ns}.data 1
$execute if data storage {ns}:temp copy[0] run function {ns}:v{version}/ammo/search_{type_name}_loop {{"slot":"$(slot)"}}
""")  # noqa: E501

    # Update ammo count in item lore
    write_versioned_function(f"ammo/found_{type_name}_line",
f"""
# Copy item to item display for modification
$item replace entity @s contents from entity @p[tag={tag}] $(slot)

# Update ammo count in lore
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-1] set value "$({CAPACITY})"
$data modify entity @s item.components."minecraft:lore"[$(index)].extra[-3] set value "$({REMAINING_BULLETS})"

# Copy modified item back to player
$item replace entity @p[tag={tag}] $(slot) from entity @s contents

# Clean up item display
kill @s
""")


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Create lore functions for weapons
    create_lore_functions(
        type_name="lore",
        tag=f"{ns}.modify_lore",
        remaining_source=f"@s {ns}.{REMAINING_BULLETS}",
        capacity_source=f"storage {ns}:temp components.\"minecraft:custom_data\".{ns}.stats.{CAPACITY}"
    )

    # Create lore functions for magazines
    create_lore_functions(
        type_name="mag_lore",
        tag=f"{ns}.modify_mag_lore",
        remaining_source=f"#bullets {ns}.data",
        capacity_source=f"storage {ns}:temp {CAPACITY}"
    )

    # Handle right click event by decreasing ammo count
    write_versioned_function("player/right_click",
f"""
# Decrease bullet count
function {ns}:v{version}/ammo/decrease
""")

    # Decrease ammo count function
    write_versioned_function("ammo/decrease",
f"""
# Remove 1 bullet from player's ammo count
scoreboard players remove @s {ns}.{REMAINING_BULLETS} 1
""")

    # Handle weapon switching logic
    write_versioned_function("switch/on_weapon_switch",
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
    for slot in ALL_SLOTS:
        content += f"""execute if items entity @s {slot} *[custom_data~{custom_data}] run return run function {ns}:v{version}/ammo/set_count {{slot:"{slot}"}}\n"""
    write_versioned_function("ammo/update_old_weapon", content)

    # Create item modifier to update weapon's ammo count
    modifier: JsonDict = {
        "function":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:temp"},
        "ops":[{"source":REMAINING_BULLETS,"target":f"{ns}.stats.{REMAINING_BULLETS}","op":"replace"}]
    }
    Mem.ctx.data[ns].item_modifiers[f"v{version}/update_ammo"] = set_json_encoder(ItemModifier(modifier), max_level=-1)

    # Update weapon's ammo count and lore
    write_versioned_function("ammo/set_count",
f"""
# Apply new ammo count to weapon
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update weapon's lore to show new ammo count
$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

    # Load ammo data from newly equipped weapon
    write_versioned_function("ammo/copy_data",
f"""
# Load ammo count from weapon into player's scoreboard (if different from -1)
execute store result score #count {ns}.data run data get storage {ns}:gun all.stats.{REMAINING_BULLETS}
execute unless score #count {ns}.data matches -1 run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #count {ns}.data

# Mark weapon as needing update
data modify storage {ns}:gun all.stats.{REMAINING_BULLETS} set value -1
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats
""")

    # Update weapon's lore to show current ammo count
    write_versioned_function("ammo/modify_lore",
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
    write_versioned_function("ammo/get_current_lore",
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
    write_versioned_function("ammo/search_lore_loop",
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
    write_versioned_function("ammo/found_line",
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

    # Reload weapon function
    write_versioned_function("ammo/reload",
f"""
# Get the new ammo count
scoreboard players set @s {ns}.cooldown 5
execute if data storage {ns}:config no_magazine store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
execute unless data storage {ns}:config no_magazine run function {ns}:v{version}/ammo/inventory/find with storage {ns}:gun all.stats
execute unless data storage {ns}:config no_magazine unless score #found_ammo {ns}.data matches 1.. run return run playsound mgs:common/empty ambient @s

# Set cooldown to reload duration
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{RELOAD_TIME}

# Force weapon switch animation
function {ns}:v{version}/switch/force_switch_animation

# Update weapon lore
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

# Play reload sound (and send stats for macro)
function {ns}:v{version}/sound/reload_start with storage {ns}:gun all.stats

# Add reloading tag
tag @s add {ns}.reloading
""")

    # Find and consume magazines from inventory
    magazine_custom_data: str = f"""{{{ns}:{{"magazine":true,"weapon":"$({BASE_WEAPON})"}}}}"""
    slot_checks: str = ""
    for slot in ALL_SLOTS:
        slot_checks += (
            f"$execute if score #found_ammo {ns}.data < #capacity {ns}.data if items entity @s {slot} *[custom_data~{magazine_custom_data}] run "
            f"""function {ns}:v{version}/ammo/inventory/process_slot {{slot:"{slot}",{BASE_WEAPON}:"$({BASE_WEAPON})"}}\n"""
        )
    write_versioned_function("ammo/inventory/find",
f"""
# Get capacity and initialize found ammo to current remaining bullets
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute store result score #found_ammo {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}

# Check all slots for magazines
{slot_checks}

# If found ammo, return success, else return fail
execute if score #found_ammo {ns}.data matches 1.. run return 0
return fail
""")

    write_versioned_function("ammo/inventory/process_slot",
f"""
# Get bullets from the magazine
tag @s add {ns}.extracting_bullets
$execute summon item_display run function {ns}:v{version}/ammo/extract_bullets {{slot:"$(slot)"}}
tag @s remove {ns}.extracting_bullets
execute if score #bullets {ns}.data matches 0 run return 0

# Calculate to_take = min(bullets, capacity - found_ammo)
scoreboard players operation #to_take {ns}.data = #capacity {ns}.data
scoreboard players operation #to_take {ns}.data -= #found_ammo {ns}.data
execute if score #bullets {ns}.data < #to_take {ns}.data run scoreboard players operation #to_take {ns}.data = #bullets {ns}.data

# Add to found_ammo
scoreboard players operation #found_ammo {ns}.data += #to_take {ns}.data

# Subtract from bullets
scoreboard players operation #bullets {ns}.data -= #to_take {ns}.data

# Modify the magazine item
$execute if score #bullets {ns}.data matches ..0 run function {ns}:v{version}/ammo/inventory/set_item_model {{slot:"$(slot)",{BASE_WEAPON}:"$({BASE_WEAPON})"}}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run scoreboard players get #bullets {ns}.data
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update magazine lore
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}

# Update player's ammo count
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #found_ammo {ns}.data
""")
    write_versioned_function("ammo/inventory/set_item_model", f"""
$item modify entity @s $(slot) {{function:"minecraft:set_components", components:{{"minecraft:item_model":"{ns}:$({BASE_WEAPON})_mag_empty"}}}}
""")

    write_versioned_function("ammo/extract_bullets",
f"""
# Copy item to entity
$item replace entity @s contents from entity @p[tag={ns}.extracting_bullets] $(slot)

# Get bullets
execute store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

# Get magazine capacity
execute store result storage {ns}:temp {CAPACITY} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

# Kill entity
kill @s
""")

    write_versioned_function("ammo/end_reload",
f"""
# Update weapon lore (if still holding weapon)
execute if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

# Remove reloading tag
tag @s remove {ns}.reloading
""")

