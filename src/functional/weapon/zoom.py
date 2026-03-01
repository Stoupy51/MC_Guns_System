
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.stats import IS_ZOOM, MODELS


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle zoom functionality
    write_versioned_function("zoom/main",
f"""
# If no gun data, stop here
execute unless data storage {ns}:gun all.gun run return run function {ns}:v{version}/zoom/check_slowness

# If already zoom and not sneaking, unzoom
execute if data storage {ns}:gun all.stats.{IS_ZOOM} unless predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage {ns}:gun all.stats.{IS_ZOOM} if predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/set

## Shader: zoom marker with delay, scope check, and cooldown guard
# Reset zoom timer when not zooming
execute unless score @s {ns}.zoom matches 1 run scoreboard players set @s {ns}.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s {ns}.zoom matches 1 run scoreboard players add @s {ns}.zoom_timer 1

# Spawn zoom x3 marker for _3 weapons (scope_level:3) — blocked during weapon switch cooldown
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{scope_level:3}}}}] at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.02,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Spawn zoom x4 marker for _4 weapons (scope_level:4) — blocked during weapon switch cooldown
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{scope_level:4}}}}] at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.08,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Spawn zoom center-only marker (mode 2) for weapons WITHOUT scope — centers flash spark w/o barrel distortion
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{scope_level:3}}}}] unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{scope_level:4}}}}] at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.25,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
""")

    # Function to remove zoom state
    write_versioned_function("zoom/remove",
f"""
# Remove zoom state from gun stats
data remove storage {ns}:gun all.stats.{IS_ZOOM}

# Prepare input storage for model update
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun all.stats.{MODELS}.normal

# Update weapon model and stats
function {ns}:v{version}/utils/update_model with storage {ns}:input with
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

# Apply unzoom effects
playsound {ns}:common/lean_out player
scoreboard players reset @s {ns}.zoom
scoreboard players set @s {ns}.zoom_timer 0
effect clear @s slowness
""")

    # Function to set zoom state
    write_versioned_function("zoom/set",
f"""
# Set zoom state in gun stats
data modify storage {ns}:gun all.stats.{IS_ZOOM} set value true

# Prepare input storage for model update
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun all.stats.{MODELS}.zoom

# Update weapon model and stats
function {ns}:v{version}/utils/update_model with storage {ns}:input with
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

# Apply zoom effects
playsound {ns}:common/lean_in player @s
effect give @s slowness infinite 2 true
scoreboard players set @s {ns}.zoom 1
""")

    # Function to check and handle slowness effect
    write_versioned_function("zoom/check_slowness",
f"""
# If player was zooming and switched slot so no longer holding a gun, remove slowness effect
execute unless score @s {ns}.zoom matches 1 run return fail
playsound {ns}:common/lean_out player @s
scoreboard players reset @s {ns}.zoom
effect clear @s slowness

# TODO optionnal: Find the weapon in inventory and turn it back to non-zoom model
""")

