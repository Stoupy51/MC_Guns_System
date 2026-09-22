""" Aim-down-sights state, and the edges that drive the scope and crosshair post effects. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import IS_ZOOM, MODELS


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Handle zoom functionality
	write_versioned_function("zoom/main", f"""
# If no gun data, stop here
execute unless data storage {ns}:gun all.gun run return run function {ns}:v{version}/zoom/check_slowness

# Grenades cannot zoom/aim, but still get the movement crosshair
execute if data storage {ns}:gun all.stats.grenade_type run return run function {ns}:v{version}/zoom/crosshair_spread

# Get is sneaking state (don't apply zoom if reloading)
scoreboard players set #is_sneaking {ns}.data 0
execute if predicate {ns}:v{version}/is_sneaking unless entity @s[tag={ns}.reloading] run scoreboard players set #is_sneaking {ns}.data 1

# If already zoom and not sneaking, unzoom
execute if data storage {ns}:gun all.stats.{IS_ZOOM} if score #is_sneaking {ns}.data matches 0 run return run function {ns}:v{version}/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage {ns}:gun all.stats.{IS_ZOOM} if score #is_sneaking {ns}.data matches 1 run return run function {ns}:v{version}/zoom/set

## Shader ids: the scope overlay while aiming, the spread crosshair while not
# Reset zoom timer when not zooming
execute unless score @s {ns}.zoom matches 1 run scoreboard players set @s {ns}.zoom_timer 0

# Increment zoom timer while zooming
execute if score @s {ns}.zoom matches 1 run scoreboard players add @s {ns}.zoom_timer 1

# The crosshair is hidden behind the scope, so the two are mutually exclusive
execute if score @s {ns}.zoom matches 1 run return run function {ns}:v{version}/zoom/crosshair_clear
function {ns}:v{version}/zoom/crosshair_spread
""")

	# Function to remove zoom state
	write_versioned_function("zoom/remove", f"""
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

# Shader: hand the scope overlay to its fade-out id
function {ns}:v{version}/zoom/fx_leave

# Signal: on_unzoom (@s = unzooming player, weapon data in mgs:signals)
data modify storage {ns}:signals on_unzoom set value {{}}
data modify storage {ns}:signals on_unzoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_unzoom
""")

	# Function to set zoom state
	write_versioned_function("zoom/set", f"""
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

# Shader: ramp the scope overlay in, level picked from the weapon's scope_level stat
function {ns}:v{version}/zoom/fx_enter

# Signal: on_zoom (@s = zooming player, weapon data in mgs:signals)
data modify storage {ns}:signals on_zoom set value {{}}
data modify storage {ns}:signals on_zoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_zoom
""")

	# Clear the player-side zoom state without touching the held item.
	# Called on weapon switch: zoom/main only unzooms when the HELD gun has the zoom stat, so switching from a zoomed gun to another gun would otherwise leave the player stuck with zoom=1 and infinite slowness.
	# The old item's zoomed model/stats self-heal via zoom/remove the next time it is held while not sneaking.
	# (mgs:gun storage already holds the NEW weapon here, so zoom/remove itself must not be used — it would corrupt the new weapon.)
	write_versioned_function("zoom/clear_state", f"""
playsound {ns}:common/lean_out player @s
scoreboard players reset @s {ns}.zoom
scoreboard players set @s {ns}.zoom_timer 0
effect clear @s slowness
function {ns}:v{version}/zoom/fx_leave
""")

	# Function to check and handle slowness effect
	write_versioned_function("zoom/check_slowness", f"""
# Not holding a gun: the vanilla crosshair sprite is blanked, so show the static base one
function {ns}:v{version}/zoom/crosshair_base

# If player was zooming and switched slot so no longer holding a gun, remove slowness effect
execute unless score @s {ns}.zoom matches 1 run return fail
playsound {ns}:common/lean_out player @s
scoreboard players reset @s {ns}.zoom
effect clear @s slowness
function {ns}:v{version}/zoom/fx_leave
""")

