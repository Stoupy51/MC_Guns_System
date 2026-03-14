
# Power Switch System
# A one-time activatable wall lever that enables power for the map.
# Elements with power:true (perk machines, traps) require power to be active.
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


def generate_power_switch() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Setup: iterate power switch compounds, place levers, summon interaction entities
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

# Determine lever facing from stored yaw (stored = player_yaw + 180)
execute store result score #pw_yaw {ns}.data run data get storage {ns}:temp _pw_iter[0].rotation[0]
data modify storage {ns}:temp _pw.facing set value "north"
execute if score #pw_yaw {ns}.data matches 0..44 run data modify storage {ns}:temp _pw.facing set value "south"
execute if score #pw_yaw {ns}.data matches 315..360 run data modify storage {ns}:temp _pw.facing set value "south"
execute if score #pw_yaw {ns}.data matches 45..134 run data modify storage {ns}:temp _pw.facing set value "west"
execute if score #pw_yaw {ns}.data matches 225..314 run data modify storage {ns}:temp _pw.facing set value "east"

# Place lever and summon interaction entity
function {ns}:v{version}/zombies/power/place_at with storage {ns}:temp _pw

# Continue iteration
data remove storage {ns}:temp _pw_iter[0]
execute if data storage {ns}:temp _pw_iter[0] run function {ns}:v{version}/zombies/power/setup_iter
""")

	write_versioned_function("zombies/power/place_at", f"""
# Place lever block
$setblock $(x) $(y) $(z) minecraft:lever[face=wall,facing=$(facing),powered=false]

# Summon interaction entity with Bookshelf tag and facing tag
$summon minecraft:interaction $(x) $(y) $(z) {{width:0.9f,height:0.9f,response:true,Tags:["{ns}.power_switch","{ns}.gm_entity","bs.entity.interaction","{ns}.pw_face_$(facing)","_pw_new"]}}

# Register Bookshelf events on newly spawned entity
execute as @e[tag=_pw_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/power/on_activate",executor:"source"}}
execute as @e[tag=_pw_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/power/on_hover",executor:"source"}}
tag @e[tag=_pw_new] remove _pw_new
""")

	## On right-click: activate power (runs as the clicking player)
	write_versioned_function("zombies/power/on_activate", f"""
# Guard: game must be active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Guard: power must not already be on
execute if score #zb_power {ns}.data matches 1 run return run function {ns}:v{version}/zombies/power/deny_already_on

# Enable power
scoreboard players set #zb_power {ns}.data 1

# Effects at each power switch position
execute as @e[tag={ns}.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag={ns}.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Toggle lever blocks to powered state
execute as @e[tag={ns}.power_switch] at @s if entity @s[tag={ns}.pw_face_north] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=north,powered=true]
execute as @e[tag={ns}.power_switch] at @s if entity @s[tag={ns}.pw_face_south] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=south,powered=true]
execute as @e[tag={ns}.power_switch] at @s if entity @s[tag={ns}.pw_face_east] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=east,powered=true]
execute as @e[tag={ns}.power_switch] at @s if entity @s[tag={ns}.pw_face_west] run setblock ~ ~ ~ minecraft:lever[face=wall,facing=west,powered=true]

# Kill power switch interaction entities (one-time use)
kill @e[tag={ns}.power_switch]

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Power is ON!","color":"green","bold":true}}]
function {ns}:v{version}/zombies/feedback/sound_power_on
""")

	write_versioned_function("zombies/power/deny_already_on", f"""
tellraw @s [{MGS_TAG},{{"text":"Power is already on.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	## Hover events (run as the player looking at the power switch)
	write_versioned_function("zombies/power/on_hover", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ Power Switch","color":"yellow"}],priority:'notification',freeze:5}
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

