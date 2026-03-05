
# Imports
from stewbeet import Mem, write_function, write_versioned_function

from ...config.stats import ALL_SLOTS, BASE_WEAPON, CAPACITY, REMAINING_BULLETS


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## ==========================================
    ## Max Ammo: Refill all magazines to capacity
    ## ==========================================

    # Build slot checks for all inventory slots
    magazine_custom_data: str = f"{{{ns}:{{magazine:true}}}}"
    slot_checks: str = ""
    for slot in ALL_SLOTS:
        slot_checks += f'execute if items entity @s {slot} *[custom_data~{magazine_custom_data}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"{slot}"}}\n'

    # Build slot checks for reloading all weapon slots (guns, not magazines)
    gun_custom_data: str = f"{{{ns}:{{gun:true}}}}"
    weapon_slot_checks: str = ""
    for slot in ALL_SLOTS:
        weapon_slot_checks += f'execute if items entity @s {slot} *[custom_data~{gun_custom_data}] run function {ns}:v{version}/zombies/bonus/reload_weapon_slot {{slot:"{slot}"}}\n'

    # Non-versioned entry point: /execute as <player> run function mgs:zombies/bonus/max_ammo
    write_function(f"{ns}:zombies/bonus/max_ammo",
f"""
# Copy gun data for current weapon (needed for ammo scoreboard sync)
function {ns}:v{version}/utils/copy_gun_data

# Refill all magazines in inventory to max capacity
{slot_checks}
# Also reload all weapons in inventory if config allows (1 = recent zombies, 0 = OG magazines only)
execute if score #max_ammo_reload_weapons {ns}.config matches 1.. run function {ns}:v{version}/zombies/bonus/max_ammo_reload_weapons

# Recompute reserve ammo display after refilling all magazines
function {ns}:v{version}/ammo/compute_reserve
""")

    # Reload ALL weapon slots (iterates all inventory)
    write_versioned_function("zombies/bonus/max_ammo_reload_weapons",
f"""
# Reload every gun item in every slot
{weapon_slot_checks}
# Sync current weapon's ammo to player scoreboard (mainhand)
execute if data storage {ns}:gun all.gun store result score @s {ns}.{REMAINING_BULLETS} run data get storage {ns}:gun all.stats.{CAPACITY}
""")

    # Reload a single weapon slot to max capacity
    write_versioned_function("zombies/bonus/reload_weapon_slot",
f"""
# Extract weapon capacity and set remaining_bullets = capacity
tag @s add {ns}.reloading_weapon
$execute summon item_display run function {ns}:v{version}/zombies/bonus/extract_weapon_capacity {{slot:"$(slot)"}}
tag @s remove {ns}.reloading_weapon

# Set player scoreboard to capacity (needed by modify_lore)
scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #bullets {ns}.data

# If this is the active mainhand weapon (remaining_bullets = -1 sentinel), only update lore
# (don't write CAPACITY to item NBT - the player's scoreboard is the source of truth)
$execute if items entity @s $(slot) *[custom_data~{{{ns}:{{stats:{{{REMAINING_BULLETS}:-1}}}}}}] run return run function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}

# For slots with inactive weapons: write CAPACITY to item NBT
$item modify entity @s $(slot) {ns}:v{version}/update_ammo

# Update weapon lore
$function {ns}:v{version}/ammo/modify_lore {{slot:"$(slot)"}}
""")

    # Extract weapon capacity from item_display (@s = item_display)
    write_versioned_function("zombies/bonus/extract_weapon_capacity",
f"""
# Copy weapon from player to item_display
$item replace entity @s contents from entity @p[tag={ns}.reloading_weapon] $(slot)

# Read capacity and store as remaining_bullets (refill = set bullets to capacity)
execute store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

# Also store into temp components for lore update
data modify storage {ns}:temp components set from entity @s item.components

# Clean up item_display
kill @s
""")

    # Refill a single magazine slot
    write_versioned_function("zombies/bonus/refill_magazine",
f"""
# Extract magazine data into storage (sets #bullets = CAPACITY)
tag @s add {ns}.refilling_mag
scoreboard players set #stack_size {ns}.data 1
$execute summon item_display run function {ns}:v{version}/zombies/bonus/extract_mag_data {{slot:"$(slot)"}}
tag @s remove {ns}.refilling_mag

# Consumable magazines use stack count as ammo - just set count to capacity and done
execute if score #stack_size {ns}.data matches 2.. run scoreboard players operation #bullets {ns}.data = #stack_size {ns}.data
$execute if score #stack_size {ns}.data matches 2.. run return run item modify entity @s $(slot) {ns}:v{version}/set_consumable_count
execute if score #stack_size {ns}.data matches 2.. run scoreboard players set #bullets {ns}.data 1

# Regular magazines: update remaining_bullets NBT, restore full model, and refresh lore
$item modify entity @s $(slot) {ns}:v{version}/update_ammo
execute if score #stack_size {ns}.data matches 1 run function {ns}:v{version}/zombies/bonus/set_full_mag_model with storage {ns}:temp refill
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}
""")

    # Extract magazine data from item_display (@s = item_display)
    write_versioned_function("zombies/bonus/extract_mag_data",
f"""
# Copy item from player to item_display
$item replace entity @s contents from entity @p[tag={ns}.refilling_mag] $(slot)

# Special consumable compatibility (get max_stack_size, 64 by default)
execute store success score #is_consumable {ns}.data if data entity @s item.components."minecraft:custom_data".{ns}.consumable
execute if score #is_consumable {ns}.data matches 1 run scoreboard players set #stack_size {ns}.data 64
execute if score #is_consumable {ns}.data matches 1 if data entity @s item.components."minecraft:max_stack_size" store result score #stack_size {ns}.data run data get entity @s item.components."minecraft:max_stack_size"

# Read capacity and store as remaining_bullets (refill = set bullets to capacity)
execute store result score #bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {REMAINING_BULLETS} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
execute store result storage {ns}:temp {CAPACITY} int 1 run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}

# Store weapon name and slot for model update macro
data modify storage {ns}:temp refill set value {{}}
$data modify storage {ns}:temp refill.slot set value "$(slot)"
data modify storage {ns}:temp refill.{BASE_WEAPON} set from entity @s item.components."minecraft:custom_data".{ns}.weapon

# Clean up item_display
kill @s
""")  # noqa: E501

    # Set magazine item model to non-empty (full) version
    write_versioned_function("zombies/bonus/set_full_mag_model", f"""
$item modify entity @s $(slot) {{"function":"minecraft:set_components", "components":{{"minecraft:item_model":"{ns}:$({BASE_WEAPON})_mag"}}}}
""")

    ## ====================================================
    ## Nuke: Tag nukable entities and kill them 1 per tick
    ## ====================================================

    # Non-versioned entry point: /execute as <player> run function mgs:zombies/bonus/nuke
    write_function(f"{ns}:zombies/bonus/nuke",
f"""
# Remove any existing nuke activator (in case of concurrent nukes)
tag @a[tag={ns}.nuke_activator] remove {ns}.nuke_activator

# Tag activating player for damage attribution
tag @s add {ns}.nuke_activator

# Tag all nukable entities as nuked
execute as @e[tag={ns}.nukable] run tag @s add {ns}.nuked

# Zero attack damage on all nuked entities (multiply base by 0)
execute as @e[tag={ns}.nuked] run attribute @s minecraft:attack_damage modifier add {ns}:nuke_zero_damage -1 add_multiplied_base

# Start kill loop (1 entity per tick)
function {ns}:v{version}/zombies/bonus/nuke_loop
""")

    # Nuke kill loop: damage 1 entity per tick
    write_versioned_function("zombies/bonus/nuke_loop",
f"""
# Find one nuked entity and process it
execute as @n[tag={ns}.nuked,sort=random] at @s run function {ns}:v{version}/zombies/bonus/nuke_damage_one

# Continue loop if more nuked entities exist
execute if entity @e[tag={ns}.nuked] run schedule function {ns}:v{version}/zombies/bonus/nuke_loop 1t

# Clean up when all nuked entities are processed
execute unless entity @e[tag={ns}.nuked] run tag @a[tag={ns}.nuke_activator] remove {ns}.nuke_activator
""")

    # Damage one nuked entity (@s = nuked entity, positioned at entity)
    write_versioned_function("zombies/bonus/nuke_damage_one",
f"""
# Remove nuked tag (entity will no longer be selected in loop)
tag @s remove {ns}.nuked

# Remove attack damage modifier (restore normal damage)
attribute @s minecraft:attack_damage modifier remove {ns}:nuke_zero_damage

# Deal lethal damage from the nuke activator player
damage @s 999999 {ns}:bullet by @n[tag={ns}.nuke_activator]
""")

