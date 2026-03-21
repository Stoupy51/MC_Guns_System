
# Door System
# Physical block barriers that players purchase to open.
# Doors with the same link_id open together. Opening doors unlocks new map areas via the group system.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .common import deny_not_enough_points_body, game_active_guard_cmd


def generate_doors() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	interaction_offset: float = 0.75  # Distance in front of door block to place interaction entities
	front_door_tags: str = f'["{ns}.door","{ns}.door_front","{ns}.gm_entity","bs.entity.interaction","{ns}.door_new"]'
	back_door_tags: str = f'["{ns}.door","{ns}.door_back","{ns}.gm_entity","bs.entity.interaction","{ns}.door_new"]'
	door_hover_message: str = (
		f'[{{"text":"🛠 ","color":"gold"}},'
		f'{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}}]'
	)

	## Door entity scoreboards
	write_load_file(f"""
# Door entity scoreboards
scoreboard objectives add {ns}.zb.door.link dummy
scoreboard objectives add {ns}.zb.door.price dummy
scoreboard objectives add {ns}.zb.door.gid dummy
scoreboard objectives add {ns}.zb.door.bgid dummy
scoreboard objectives add {ns}.zb.door.anim dummy
scoreboard objectives add {ns}.zb.door.rot dummy
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
data modify storage {ns}:temp _door.facing set value 0
execute store result storage {ns}:temp _door.facing int 1 run data get storage {ns}:temp _door_iter[0].rotation[0]

# Read door name (default "Door", override with "name" field)
data modify storage {ns}:temp _door_name.name set value "Door"
execute if data storage {ns}:temp _door_iter[0].name run data modify storage {ns}:temp _door_name.name set from storage {ns}:temp _door_iter[0].name
# Read optional back_name (default to name)
data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_name.name
execute if data storage {ns}:temp _door_iter[0].back_name run data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_iter[0].back_name

# Place block and summon interaction entity
function {ns}:v{version}/zombies/doors/place_at with storage {ns}:temp _door

# Set scoreboards on newly spawned door entity
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.link run data get storage {ns}:temp _door_iter[0].link_id
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.price run data get storage {ns}:temp _door_iter[0].price
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.gid run data get storage {ns}:temp _door_iter[0].group_id
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.bgid run data get storage {ns}:temp _door_iter[0].back_group_id
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.anim run data get storage {ns}:temp _door_iter[0].animation
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.rot run data get storage {ns}:temp _door_iter[0].rotation[0]

# Store name indexed by link_id
execute store result storage {ns}:temp _door_name.id int 1 run data get storage {ns}:temp _door_iter[0].link_id
function {ns}:v{version}/zombies/doors/store_name with storage {ns}:temp _door_name

# Register Bookshelf events
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/doors/on_right_click",executor:"source"}}
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/doors/on_hover",executor:"source"}}
tag @e[tag={ns}.door_new] remove {ns}.door_new

# Continue iteration
data remove storage {ns}:temp _door_iter[0]
execute if data storage {ns}:temp _door_iter[0] run function {ns}:v{version}/zombies/doors/setup_iter
""")

	write_versioned_function("zombies/doors/place_at", f"""
# Place door block at position
$setblock $(x) $(y) $(z) $(block)

# Summon front-side interaction entity.
$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^{interaction_offset} {{width:1.5f,height:1.1f,response:true,Tags:{front_door_tags}}}

# Summon back-side interaction entity.
$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^-{interaction_offset} {{width:1.5f,height:1.1f,response:true,Tags:{back_door_tags}}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/doors/on_right_click", f"""
# Guard: game must be active
{game_active_guard_cmd(ns)}

# Get door price from interacted entity
execute store result score #door_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.price

# Check player has enough points
execute unless score @s {ns}.zb.points >= #door_price {ns}.data run return run function {ns}:v{version}/zombies/doors/deny_not_enough_points

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #door_price {ns}.data

# Get link_id from interacted door
execute store result score #door_link {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link

# Open all doors with matching link_id
execute as @e[tag={ns}.door] if score @s {ns}.zb.door.link = #door_link {ns}.data at @s run function {ns}:v{version}/zombies/doors/open_one

# Announce
tellraw @s [{MGS_TAG},{{"text":"Door opened for ","color":"green"}},{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"green"}}]
function {ns}:v{version}/zombies/feedback/sound_announce
""")

	write_versioned_function("zombies/doors/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#door_price")}
""")

	## Open a single door entity (@s = door entity, at @s position)
	write_versioned_function("zombies/doors/open_one", f"""
# Use stored rotation and side-aware local offset so both front/back interactions
# target the same door block position.
execute store result storage {ns}:temp _door_open.rot int 1 run scoreboard players get @s {ns}.zb.door.rot
data modify storage {ns}:temp _door_open.offset set value -{interaction_offset}
execute if entity @s[tag={ns}.door_back] run data modify storage {ns}:temp _door_open.offset set value {interaction_offset}

# Remove block based on animation type (0 = destroy with particles, 1+ = silent air)
execute if score @s {ns}.zb.door.anim matches 0 run function {ns}:v{version}/zombies/doors/remove_block_destroy with storage {ns}:temp _door_open
execute unless score @s {ns}.zb.door.anim matches 0 run function {ns}:v{version}/zombies/doors/remove_block_silent with storage {ns}:temp _door_open

# Unlock primary group
execute store result storage {ns}:temp _door_unlock.gid int 1 run scoreboard players get @s {ns}.zb.door.gid
function {ns}:v{version}/zombies/doors/unlock_group with storage {ns}:temp _door_unlock

# Unlock back group if applicable (back_group_id != -1)
execute unless score @s {ns}.zb.door.bgid matches -1 run function {ns}:v{version}/zombies/doors/unlock_back_group

# Kill door interaction entity
kill @s
""")

	write_versioned_function("zombies/doors/remove_block_destroy", """
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air destroy
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run kill @e[type=item,distance=..1.5]
""")

	write_versioned_function("zombies/doors/remove_block_silent", """
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air
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

	write_versioned_function("zombies/doors/get_hover_name_back", f"""
$data modify storage {ns}:temp _door_hover_name set from storage {ns}:zombies door_names."$(id)".back_name
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/doors/on_hover", f"""
execute store result score #door_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.price
execute store result score #door_link {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link
execute store result storage {ns}:temp _door_hover.id int 1 run scoreboard players get #door_link {ns}.data
execute if entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name_back with storage {ns}:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name with storage {ns}:temp _door_hover
data modify storage smithed.actionbar:input message set value {{json:{door_hover_message},priority:'notification',freeze:5}}
function #smithed.actionbar:message
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

