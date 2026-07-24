
# Power Switch System
# A one-time activatable wall switch (custom breaker-box model) that enables power for the map.
# Elements with power:true (perk machines, traps) require power to be active.
# The switch is rendered as an item_display using the {ns}:power_switch model (see
# database/models/power_switch.json + database/others.py); on activation it swaps to
# {ns}:power_switch_on (handle + indicator light recolored green/lit).
from stewbeet import Mem, write_versioned_function

from ..core.feedback import zb_sound
from ..helpers import MGS_TAG
from .common import deny_cmd, game_active_guard_cmd


def generate_power_switch() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	deny_already_on: str = deny_cmd(ns, version, '{"text":"Power is already on.","color":"yellow"}')

	## Setup: iterate power switch compounds, summon interaction entities + custom-model displays
	write_versioned_function("zombies/power/setup", f"""
# Iterate power switch compounds from map data
data modify storage {ns}:temp _pw_iter set from storage {ns}:zombies game.map.power_switch
execute if data storage {ns}:temp _pw_iter[0] run function {ns}:v{version}/zombies/power/setup_iter
""")

	write_versioned_function("zombies/power/setup_iter", f"""
# Read relative position and convert to absolute
execute store result score #pwx {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[0]
execute store result score #pwy {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[1]
execute store result score #pwz {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[2]
scoreboard players operation #pwx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #pwy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #pwz {ns}.data += #gm_base_z {ns}.data

# Store absolute position for macro
execute store result storage {ns}:temp _pw.x int 1 run scoreboard players get #pwx {ns}.data
execute store result storage {ns}:temp _pw.y int 1 run scoreboard players get #pwy {ns}.data
execute store result storage {ns}:temp _pw.z int 1 run scoreboard players get #pwz {ns}.data

# Store yaw for the display (stored = player_yaw + 180 so the switch faces the placer, just like
# the perk/PAP machine displays; this model is built front-facing the opposite way, so its fixed
# display rotation is 0 instead of -180 — see database/models/power_switch.json)
data modify storage {ns}:temp _pw.yaw set value 0.0f
execute if data storage {ns}:temp _pw_iter[0].rotation[0] run data modify storage {ns}:temp _pw.yaw set from storage {ns}:temp _pw_iter[0].rotation[0]

# Summon interaction entity + custom-model display
function {ns}:v{version}/zombies/power/place_at with storage {ns}:temp _pw

# Continue iteration
data remove storage {ns}:temp _pw_iter[0]
execute if data storage {ns}:temp _pw_iter[0] run function {ns}:v{version}/zombies/power/setup_iter
""")

	write_versioned_function("zombies/power/place_at", f"""
# Summon interaction entity (clickable hitbox) with Bookshelf tag
$summon minecraft:interaction $(x) $(y) $(z) {{width:0.9f,height:0.9f,response:true,Tags:["{ns}.power_switch","{ns}.gm_entity","bs.entity.interaction","_pw_new"]}}

# Summon the custom-model display, centered in the switch block, facing the placer (yaw)
$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.power_switch_disp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:lever",count:1,components:{{"minecraft:item_model":"{ns}:power_switch"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}

# Register Bookshelf events on newly spawned interaction entity
execute as @e[tag=_pw_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/power/on_activate",executor:"source"}}
execute as @e[tag=_pw_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/power/on_hover",executor:"source"}}
tag @e[tag=_pw_new] remove _pw_new
""")  # noqa: E501

	## On right-click: activate power (runs as the clicking player)
	write_versioned_function("zombies/power/on_activate", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Guard: power must not already be on
execute if score #zb_power {ns}.data matches 1 run return run {deny_already_on}

# Enable power
scoreboard players set #zb_power {ns}.data 1

# Effects at each power switch position
execute as @e[tag={ns}.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag={ns}.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Switch every display model to its powered ('on') variant (handle + light go green/lit)
execute as @e[tag={ns}.power_switch_disp] run data modify entity @s item.components."minecraft:item_model" set value "{ns}:power_switch_on"

# Kill power switch interaction entities (one-time use); displays stay to show the "on" state
kill @e[tag={ns}.power_switch]

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Power is ON!","color":"green","bold":true}}]
{zb_sound('power_on')}

# Signal map-specific power-on hooks
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"power"}}
""")

	## Hover events (run as the player looking at the power switch)
	write_versioned_function("zombies/power/on_hover", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ Power Switch","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	## Hook into game start: reset power scoreboard
	write_versioned_function("zombies/start", f"""
# Initialize power state
scoreboard players set #zb_power {ns}.data 0
""")

	## Hook into preload_complete: setup power switches
	write_versioned_function("zombies/preload_complete", f"""
# Setup power switches
execute if data storage {ns}:zombies game.map.power_switch[0] run function {ns}:v{version}/zombies/power/setup
""")
