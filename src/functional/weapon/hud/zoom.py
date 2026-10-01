""" Aim-down-sights state, and the edges that drive the scope and crosshair post effects. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import IS_ZOOM, MODELS


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zoom/main", f"""
# No gun.
execute unless data storage {ns}:gun all.gun run return run function {ns}:v{version}/zoom/check_slowness

# Grenades cannot aim, but still get the movement crosshair.
execute if data storage {ns}:gun all.stats.grenade_type run return run function {ns}:v{version}/zoom/crosshair_spread

# No zoom while reloading.
scoreboard players set #is_sneaking {ns}.data 0
execute if predicate {ns}:v{version}/is_sneaking unless entity @s[tag={ns}.reloading] run scoreboard players set #is_sneaking {ns}.data 1

execute if data storage {ns}:gun all.stats.{IS_ZOOM} if score #is_sneaking {ns}.data matches 0 run return run function {ns}:v{version}/zoom/remove

# Keyed on the score, not the item: a gun switched away from mid-aim keeps its zoom stat.
execute if score #is_sneaking {ns}.data matches 1 unless score @s {ns}.zoom matches 1 run return run function {ns}:v{version}/zoom/set

## The scope overlay while aiming, the spread crosshair otherwise; the crosshair is hidden behind the scope.
execute if score @s {ns}.zoom matches 1 run return run function {ns}:v{version}/zoom/crosshair_clear
function {ns}:v{version}/zoom/crosshair_spread
""")

	write_versioned_function("zoom/remove", f"""
data remove storage {ns}:gun all.stats.{IS_ZOOM}

data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun all.stats.{MODELS}.normal

function {ns}:v{version}/utils/update_model with storage {ns}:input with
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

playsound {ns}:common/lean_out player
scoreboard players reset @s {ns}.zoom
effect clear @s slowness

# The scope overlay switches to its fade-out id.
function {ns}:v{version}/zoom/fx_leave

# Run as the player; weapon data in mgs:signals.
data modify storage {ns}:signals on_unzoom set value {{}}
data modify storage {ns}:signals on_unzoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_unzoom
""")

	write_versioned_function("zoom/set", f"""
data modify storage {ns}:gun all.stats.{IS_ZOOM} set value true

data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun all.stats.{MODELS}.zoom

function {ns}:v{version}/utils/update_model with storage {ns}:input with
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

playsound {ns}:common/lean_in player @s
effect give @s slowness infinite 2 true
scoreboard players set @s {ns}.zoom 1

# Overlay level from the weapon's scope_level.
function {ns}:v{version}/zoom/fx_enter

# Run as the player; weapon data in mgs:signals.
data modify storage {ns}:signals on_zoom set value {{}}
data modify storage {ns}:signals on_zoom.weapon set from storage {ns}:gun all
function #{ns}:signals/on_zoom
""")

	# Clears the player-side zoom on weapon switch without touching the held item: mgs:gun already holds the new weapon, so zoom/remove would corrupt it.
	# The old item keeps its zoomed stats until zoom/main sees it held again.
	write_versioned_function("zoom/clear_state", f"""
playsound {ns}:common/lean_out player @s
scoreboard players reset @s {ns}.zoom
effect clear @s slowness
function {ns}:v{version}/zoom/fx_leave
""")

	write_versioned_function("zoom/check_slowness", f"""
# No gun: the vanilla crosshair sprite is blank, so the static base one shows.
function {ns}:v{version}/zoom/crosshair_base

# Switched away from a gun while zoomed: remove the slowness.
execute unless score @s {ns}.zoom matches 1 run return fail
playsound {ns}:common/lean_out player @s
scoreboard players reset @s {ns}.zoom
effect clear @s slowness
function {ns}:v{version}/zoom/fx_leave
""")

