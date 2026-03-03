
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

# Grenades cannot zoom/aim
execute if data storage {ns}:gun all.stats.grenade_type run return 0

# If already zoom and not sneaking, unzoom
execute if data storage {ns}:gun all.stats.{IS_ZOOM} unless predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage {ns}:gun all.stats.{IS_ZOOM} if predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/set

## Shader: zoom marker with delay, scope check, and cooldown guard
# Reset zoom timer when not zooming
execute unless score @s {ns}.zoom matches 1 run scoreboard players set @s {ns}.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s {ns}.zoom matches 1 run scoreboard players add @s {ns}.zoom_timer 1

# FOV marker: spawn IMMEDIATELY on zoom (no delay) for smooth FOV reduction
# Uses color with B=0.15 (non-zero B + non-zero G) to distinguish from zoom/flash/spread markers
# B=0.15 → B'∈[18-38] after randomization, safely above dim grayscale particles
scoreboard players set #scope_level {ns}.data 0
execute store result score #scope_level {ns}.data run data get storage {ns}:gun all.scope_level
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score #scope_level {ns}.data matches 3 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.02,0.15],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score #scope_level {ns}.data matches 4 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.08,0.15],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 unless score #scope_level {ns}.data matches 3 unless score #scope_level {ns}.data matches 4 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.25,0.15],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Scope zoom marker: spawn AFTER delay for barrel distortion effect
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. if score #scope_level {ns}.data matches 3 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.02,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. if score #scope_level {ns}.data matches 4 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.08,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
execute if score @s {ns}.zoom matches 1 if score @s {ns}.switch_cooldown matches 0 if score @s {ns}.zoom_timer matches 5.. unless score #scope_level {ns}.data matches 3 unless score #scope_level {ns}.data matches 4 at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.25,0.0],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Crosshair spread marker: spawn when NOT zooming to indicate accuracy via crosshair gap
execute unless score @s {ns}.zoom matches 1 run function {ns}:v{version}/zoom/crosshair_spread
""")

    # Crosshair spread: spawn a marker particle encoding the player's movement state
    # Uses B channel > 0 (with G=0) to distinguish from flash/zoom markers
    # Priority: jump > sprint > walk > sneak > base (matching accuracy system)
    write_versioned_function("zoom/crosshair_spread",
f"""
# If sneaking in the air, treat as walking (not jump spread)
execute unless predicate {ns}:v{version}/is_on_ground if predicate {ns}:v{version}/is_sneaking at @s anchored eyes run return run particle minecraft:dust{{color:[0.02,0.0,0.12],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Jump (in air, not sneaking): widest spread
execute unless predicate {ns}:v{version}/is_on_ground at @s anchored eyes run return run particle minecraft:dust{{color:[0.02,0.0,0.60],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Sprint: very wide spread
execute if predicate {ns}:v{version}/is_sprinting at @s anchored eyes run return run particle minecraft:dust{{color:[0.02,0.0,0.28],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Walk: wider spread
execute unless predicate {ns}:v{version}/is_sprinting if predicate {ns}:v{version}/is_moving at @s anchored eyes run return run particle minecraft:dust{{color:[0.02,0.0,0.12],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Sneak: tightest spread (rarely visible since sneak = zoom for guns)
execute if predicate {ns}:v{version}/is_sneaking at @s anchored eyes run return run particle minecraft:dust{{color:[0.02,0.0,0.02],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s

# Base: standing still, default spread
execute at @s anchored eyes run particle minecraft:dust{{color:[0.02,0.0,0.05],scale:0.01}} ^ ^ ^1 0 0 0 0 1 force @s
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

# Signal: on_unzoom (@s = unzooming player, weapon data in mgs:signals)
data modify storage {ns}:signals on_unzoom set value {{}}
data modify storage {ns}:signals on_unzoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_unzoom
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

# Signal: on_zoom (@s = zooming player, weapon data in mgs:signals)
data modify storage {ns}:signals on_zoom set value {{}}
data modify storage {ns}:signals on_zoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_zoom
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

