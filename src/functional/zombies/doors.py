
# Door System
# Physical block barriers that players purchase to open.
# Doors with the same link_id open together. Opening doors unlocks new map areas via the group system.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_doors() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Door entity scoreboards
	write_load_file(f"""
# Door entity scoreboards
scoreboard objectives add {ns}.zb.door.link dummy
scoreboard objectives add {ns}.zb.door.price dummy
scoreboard objectives add {ns}.zb.door.gid dummy
scoreboard objectives add {ns}.zb.door.bgid dummy
scoreboard objectives add {ns}.zb.door.anim dummy
""")

	## Setup: iterate door compounds, place blocks, summon interaction entities
	write_versioned_function("zombies/doors/setup", f"""
data modify storage {ns}:temp _door_iter set from storage {ns}:zombies game.map.doors
execute if data storage {ns}:temp _door_iter[0] run function {ns}:v{version}/zombies/doors/setup_iter
""")

	write_versioned_function("zombies/doors/setup_iter", f"""
# Read relative position and convert to absolute
execute store result score #dx {ns}.data run data get storage {ns}:temp _door_iter[0].pos[0]
execute store result score #dy {ns}.data run data get storage {ns}:temp _door_iter[0].pos[1]
execute store result score #dz {ns}.data run data get storage {ns}:temp _door_iter[0].pos[2]
scoreboard players operation #dx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #dy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #dz {ns}.data += #gm_base_z {ns}.data

# Store absolute position and block for macro
execute store result storage {ns}:temp _door.x int 1 run scoreboard players get #dx {ns}.data
execute store result storage {ns}:temp _door.y int 1 run scoreboard players get #dy {ns}.data
execute store result storage {ns}:temp _door.z int 1 run scoreboard players get #dz {ns}.data
data modify storage {ns}:temp _door.block set from storage {ns}:temp _door_iter[0].block

# Read door name (default "Door", override with "name" field)
data modify storage {ns}:temp _door_name.name set value "Door"
execute if data storage {ns}:temp _door_iter[0].name run data modify storage {ns}:temp _door_name.name set from storage {ns}:temp _door_iter[0].name
# Read optional back_name (default to name)
data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_name.name
execute if data storage {ns}:temp _door_iter[0].back_name run data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_iter[0].back_name

# Place block and summon interaction entity
function {ns}:v{version}/zombies/doors/place_at with storage {ns}:temp _door

# Set scoreboards on newly spawned door entity
execute store result score @n[tag={ns}.door_new] {ns}.zb.door.link run data get storage {ns}:temp _door_iter[0].link_id
execute store result score @n[tag={ns}.door_new] {ns}.zb.door.price run data get storage {ns}:temp _door_iter[0].price
execute store result score @n[tag={ns}.door_new] {ns}.zb.door.gid run data get storage {ns}:temp _door_iter[0].group_id
execute store result score @n[tag={ns}.door_new] {ns}.zb.door.bgid run data get storage {ns}:temp _door_iter[0].back_group_id
execute store result score @n[tag={ns}.door_new] {ns}.zb.door.anim run data get storage {ns}:temp _door_iter[0].animation

# Store name indexed by link_id
execute store result storage {ns}:temp _door_name.id int 1 run data get storage {ns}:temp _door_iter[0].link_id
function {ns}:v{version}/zombies/doors/store_name with storage {ns}:temp _door_name

# Register Bookshelf events
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/doors/on_right_click",executor:"source"}}
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_hover_enter {{run:"function {ns}:v{version}/zombies/doors/on_hover_enter",executor:"source"}}
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_hover_leave {{run:"function {ns}:v{version}/zombies/doors/on_hover_leave",executor:"source"}}
tag @e[tag={ns}.door_new] remove {ns}.door_new

# Continue iteration
data remove storage {ns}:temp _door_iter[0]
execute if data storage {ns}:temp _door_iter[0] run function {ns}:v{version}/zombies/doors/setup_iter
""")

	write_versioned_function("zombies/doors/place_at", f"""
# Place door block at position
$setblock $(x) $(y) $(z) $(block)

# Summon interaction entity
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.1f,height:1.1f,response:true,Tags:["{ns}.door","{ns}.gm_entity","bs.entity.interaction","{ns}.door_new"]}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/doors/on_right_click", f"""
# Guard: game must be active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Get door price from interacted entity
execute store result score #door_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.price

# Check player has enough points
execute unless score @s {ns}.zb.points >= #door_price {ns}.data run return run tellraw @s [{MGS_TAG},{{"text":" Not enough points!","color":"red"}}]

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #door_price {ns}.data

# Get link_id from interacted door
execute store result score #door_link {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link

# Open all doors with matching link_id
execute as @e[tag={ns}.door] if score @s {ns}.zb.door.link = #door_link {ns}.data at @s run function {ns}:v{version}/zombies/doors/open_one

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":" 🚪 Door opened!","color":"green"}}]
""")

	## Open a single door entity (@s = door entity, at @s position)
	write_versioned_function("zombies/doors/open_one", f"""
# Remove block based on animation type (0 = destroy with particles, 1+ = silent air)
execute if score @s {ns}.zb.door.anim matches 0 run setblock ~ ~ ~ air destroy
execute if score @s {ns}.zb.door.anim matches 0 run kill @e[type=item,distance=..1.5]
execute unless score @s {ns}.zb.door.anim matches 0 run setblock ~ ~ ~ air

# Unlock primary group
execute store result storage {ns}:temp _door_unlock.gid int 1 run scoreboard players get @s {ns}.zb.door.gid
function {ns}:v{version}/zombies/doors/unlock_group with storage {ns}:temp _door_unlock

# Unlock back group if applicable (back_group_id != -1)
execute unless score @s {ns}.zb.door.bgid matches -1 run function {ns}:v{version}/zombies/doors/unlock_back_group

# Kill door interaction entity
kill @s
""")

	## Unlock back group helper (@s = door entity)
	write_versioned_function("zombies/doors/unlock_back_group", f"""
execute store result storage {ns}:temp _door_unlock.gid int 1 run scoreboard players get @s {ns}.zb.door.bgid
function {ns}:v{version}/zombies/doors/unlock_group with storage {ns}:temp _door_unlock
""")

	## Unlock group (macro): add group to unlocked set and tag spawn markers
	write_versioned_function("zombies/doors/unlock_group", f"""
$data modify storage {ns}:zombies game.unlocked_groups."$(gid)" set value 1b

# Tag spawn markers with matching group_id as unlocked
$scoreboard players set #unlock_gid {ns}.data $(gid)
execute as @e[tag={ns}.spawn_point] if score @s {ns}.zb.spawn.gid = #unlock_gid {ns}.data run tag @s add {ns}.spawn_unlocked
""")

	write_versioned_function("zombies/doors/store_name", f"""
$data modify storage {ns}:zombies door_names."$(id)" set value {{name:"$(name)",back_name:"$(back_name)"}}
""")

	write_versioned_function("zombies/doors/get_hover_name", f"""
$data modify storage {ns}:temp _door_hover_name set from storage {ns}:zombies door_names."$(id)".name
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/doors/on_hover_enter", f"""
execute store result score #door_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.price
execute store result storage {ns}:temp _door_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link
function {ns}:v{version}/zombies/doors/get_hover_name with storage {ns}:temp _door_hover
title @s times 0 40 10
title @s title [{{"text":"🚪 ","color":"gold"}},{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"gold"}}]
title @s subtitle [{{"text":"Cost: ","color":"gray"}},{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]
""")

	write_versioned_function("zombies/doors/on_hover_leave", """
title @s clear
""")

	## Hook into game start: initialize unlocked groups
	write_versioned_function("zombies/start", f"""
# Initialize unlocked groups (group 0 = starting area, compound keys for quick lookup)
data modify storage {ns}:zombies game.unlocked_groups set value {{"0": 1b}}
""")

	## Hook into preload_complete: setup doors
	write_versioned_function("zombies/preload_complete", f"""
# Setup doors
execute if data storage {ns}:zombies game.map.doors[0] run function {ns}:v{version}/zombies/doors/setup
""")

