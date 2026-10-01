""" Door system.

Physical block barricades that players purchase to open.

Doors with the same link_id open together.
A door's link_id is also its front-room spawn group, and back_group_id is its back-room spawn group; opening a door unlocks both groups' zombie spawns.
"""

# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ...core.feedback import ZombiesFeedback
from ...helpers import MGS_TAG
from ...helpers.text import Text
from ...progression import Xp
from ..common import ZombiesCommon


# Functions
def generate_doors() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#door_price")
	interaction_offset: float = 0.75  # Distance in front of door block to place interaction entities
	front_door_tags: str = f'["{ns}.door","{ns}.door_front","{ns}.gm_entity","bs.entity.interaction","{ns}.door_new"]'
	back_door_tags: str = f'["{ns}.door","{ns}.door_back","{ns}.gm_entity","bs.entity.interaction","{ns}.door_new"]'
	door_hover_message: str = (
		f'[{{"text":"🛠 "}},'
		f'{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}}]'
	)
	# Chip-in doors show the next chunk plus the group's progress instead of the full price
	door_hover_partial_message: str = (
		f'[{{"text":"🛠 "}},'
		f'{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Chip in: ","color":"gray"}},'
		f'{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points (","color":"gray"}},'
		f'{{"score":{{"name":"#door_paid","objective":"{ns}.data"}},"color":"green"}},'
		f'{{"text":"/","color":"gray"}},'
		f'{{"score":{{"name":"#door_total","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":")","color":"gray"}}]'
	)

	write_load_file(f"""
scoreboard objectives add {ns}.zb.door.link dummy
scoreboard objectives add {ns}.zb.door.price dummy
scoreboard objectives add {ns}.zb.door.bgid dummy
scoreboard objectives add {ns}.zb.door.anim dummy
scoreboard objectives add {ns}.zb.door.rot dummy
# Chip-in: chunk size (0 = off) and what the group paid; progress is global, so `paid` is mirrored on the whole link group.
scoreboard objectives add {ns}.zb.door.partial dummy
scoreboard objectives add {ns}.zb.door.paid dummy
""")

	write_versioned_function("zombies/doors/setup", f"""
data modify storage {ns}:temp _door_iter set from storage {ns}:zombies game.map.doors
execute if data storage {ns}:temp _door_iter[0] run function {ns}:v{version}/zombies/doors/setup_iter
""")

	write_versioned_function("zombies/doors/setup_iter", f"""
execute store result score #dx {ns}.data run data get storage {ns}:temp _door_iter[0].pos[0]
execute store result score #dy {ns}.data run data get storage {ns}:temp _door_iter[0].pos[1]
execute store result score #dz {ns}.data run data get storage {ns}:temp _door_iter[0].pos[2]
scoreboard players operation #dx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #dy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #dz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _door.x int 1 run scoreboard players get #dx {ns}.data
execute store result storage {ns}:temp _door.y int 1 run scoreboard players get #dy {ns}.data
execute store result storage {ns}:temp _door.z int 1 run scoreboard players get #dz {ns}.data
data modify storage {ns}:temp _door.block set from storage {ns}:temp _door_iter[0].block
data modify storage {ns}:temp _door.facing set value 0
execute store result storage {ns}:temp _door.facing int 1 run data get storage {ns}:temp _door_iter[0].rotation[0]

# Name defaults to "Door".
data modify storage {ns}:temp _door_name.name set value "Door"
execute if data storage {ns}:temp _door_iter[0].name run data modify storage {ns}:temp _door_name.name set from storage {ns}:temp _door_iter[0].name
# back_name defaults to the name.
data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_name.name
execute if data storage {ns}:temp _door_iter[0].back_name run data modify storage {ns}:temp _door_name.back_name set from storage {ns}:temp _door_iter[0].back_name

function {ns}:v{version}/zombies/doors/place_at with storage {ns}:temp _door

execute store result score @e[tag={ns}.door_new] {ns}.zb.door.link run data get storage {ns}:temp _door_iter[0].link_id
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.price run data get storage {ns}:temp _door_iter[0].price
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.bgid run data get storage {ns}:temp _door_iter[0].back_group_id
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.anim run data get storage {ns}:temp _door_iter[0].animation
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.rot run data get storage {ns}:temp _door_iter[0].rotation[0]

# Maps saved before chip-in existed have no field: the failed read stores 0 (off).
scoreboard players set @e[tag={ns}.door_new] {ns}.zb.door.paid 0
execute store result score @e[tag={ns}.door_new] {ns}.zb.door.partial run data get storage {ns}:temp _door_iter[0].partial_price

execute store result storage {ns}:temp _door_name.id int 1 run data get storage {ns}:temp _door_iter[0].link_id
function {ns}:v{version}/zombies/doors/store_name with storage {ns}:temp _door_name

execute as @e[tag={ns}.door_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/doors/on_right_click",executor:"source"}}
execute as @e[tag={ns}.door_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/doors/on_hover",executor:"source"}}
tag @e[tag={ns}.door_new] remove {ns}.door_new

data remove storage {ns}:temp _door_iter[0]
execute if data storage {ns}:temp _door_iter[0] run function {ns}:v{version}/zombies/doors/setup_iter
""")

	write_versioned_function("zombies/doors/place_at", f"""
$setblock $(x) $(y) $(z) $(block)

$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^{interaction_offset} {{width:1.5f,height:1.1f,response:true,Tags:{front_door_tags}}}

$execute positioned $(x) $(y) $(z) rotated $(facing) 0 run summon minecraft:interaction ^ ^ ^-{interaction_offset} {{width:1.5f,height:1.1f,response:true,Tags:{back_door_tags}}}
""")

	## Read the interacted door's pricing: #door_total is the full price, #door_price what this click costs
	## (a chunk when chip-in is on, the rest for the last one), #door_paid the group's progress.
	write_versioned_function("zombies/doors/read_price", f"""
execute store result score #door_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.price
execute store result score #door_partial {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.partial
execute store result score #door_paid {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.paid
scoreboard players operation #door_total {ns}.data = #door_price {ns}.data

# Clamped at 0, so a price lowered below the progress cannot hand out points.
scoreboard players operation #door_left {ns}.data = #door_total {ns}.data
scoreboard players operation #door_left {ns}.data -= #door_paid {ns}.data
execute if score #door_left {ns}.data matches ..0 run scoreboard players set #door_left {ns}.data 0

execute if score #door_partial {ns}.data matches 1.. run scoreboard players operation #door_price {ns}.data = #door_partial {ns}.data
execute if score #door_partial {ns}.data matches 1.. run scoreboard players operation #door_price {ns}.data < #door_left {ns}.data
""")

	## Run as the player.
	write_versioned_function("zombies/doors/on_right_click", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}

function {ns}:v{version}/zombies/doors/read_price

execute unless score @s {ns}.zb.points >= #door_price {ns}.data run return run {deny_not_enough_points}

scoreboard players operation @s {ns}.zb.points -= #door_price {ns}.data

execute store result score #door_link {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link

# Front or back name, for the announce.
execute store result storage {ns}:temp _door_hover.id int 1 run scoreboard players get #door_link {ns}.data
execute if entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name_back with storage {ns}:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name with storage {ns}:temp _door_hover

# Chip-in progress is global: mirror it on every entity of the link group (both sides of every linked door).
scoreboard players operation #door_paid {ns}.data += #door_price {ns}.data
execute if score #door_partial {ns}.data matches 1.. as @e[tag={ns}.door] if score @s {ns}.zb.door.link = #door_link {ns}.data run scoreboard players operation @s {ns}.zb.door.paid = #door_paid {ns}.data
execute if score #door_partial {ns}.data matches 1.. if score #door_paid {ns}.data < #door_total {ns}.data run return run function {ns}:v{version}/zombies/doors/announce_progress

execute as @e[tag={ns}.door] if score @s {ns}.zb.door.link = #door_link {ns}.data at @s run function {ns}:v{version}/zombies/doors/open_one

# Announces the total, not the last chunk.
{Xp.announce("zb", "door", f'{MGS_TAG},{Text.player(ns, "@s", side="zb", color="yellow")},{{"text":" opened ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"gold","interpret":true}},{{"text":" for ","color":"green"}},{{"score":{{"name":"#door_total","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"green"}}')}
{ZombiesFeedback.zb_sound('announce')}
""")

	## Run as the paying player, when the chunk did not finish the door.
	write_versioned_function("zombies/doors/announce_progress", f"""
tellraw @a [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="yellow")},{{"text":" chipped in ","color":"green"}},{{"score":{{"name":"#door_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points for ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_door_hover_name","color":"gold","interpret":true}},{{"text":"  (","color":"gray"}},{{"score":{{"name":"#door_paid","objective":"{ns}.data"}},"color":"green"}},{{"text":"/","color":"gray"}},{{"score":{{"name":"#door_total","objective":"{ns}.data"}},"color":"yellow"}},{{"text":")","color":"gray"}}]
{ZombiesFeedback.zb_sound('announce')}
""")

	## Run as the door entity, at it.
	write_versioned_function("zombies/doors/open_one", f"""
# Stored rotation and side-aware offset, so both interactions target the same door block.
execute store result storage {ns}:temp _door_open.rot int 1 run scoreboard players get @s {ns}.zb.door.rot
data modify storage {ns}:temp _door_open.offset set value -{interaction_offset}
execute if entity @s[tag={ns}.door_back] run data modify storage {ns}:temp _door_open.offset set value {interaction_offset}

# anim 0 breaks the block with particles, 1+ sets air silently.
execute if score @s {ns}.zb.door.anim matches 0 run function {ns}:v{version}/zombies/doors/remove_block_destroy with storage {ns}:temp _door_open
execute unless score @s {ns}.zb.door.anim matches 0 run function {ns}:v{version}/zombies/doors/remove_block_silent with storage {ns}:temp _door_open

# link_id is the front room's group_id.
execute store result storage {ns}:temp _door_unlock.gid int 1 run scoreboard players get @s {ns}.zb.door.link
function {ns}:v{version}/zombies/doors/unlock_group with storage {ns}:temp _door_unlock

# back_group_id -1 means no back room.
execute unless score @s {ns}.zb.door.bgid matches -1 run function {ns}:v{version}/zombies/doors/unlock_back_group

kill @s
""")

	write_versioned_function("zombies/doors/remove_block_destroy", """
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air destroy
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run kill @e[type=item,distance=..1.5]
""")

	write_versioned_function("zombies/doors/remove_block_silent", """
$execute positioned ~ ~ ~ rotated $(rot) 0 positioned ^ ^ ^$(offset) run setblock ~ ~ ~ air
""")

	## Run as the door entity.
	write_versioned_function("zombies/doors/unlock_back_group", f"""
execute store result storage {ns}:temp _door_unlock.gid int 1 run scoreboard players get @s {ns}.zb.door.bgid
function {ns}:v{version}/zombies/doors/unlock_group with storage {ns}:temp _door_unlock
""")

	write_versioned_function("zombies/doors/unlock_group", f"""
$data modify storage {ns}:zombies game.unlocked_groups."$(gid)" set value 1b

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

	## Run as the player.
	write_versioned_function("zombies/doors/on_hover", f"""
function {ns}:v{version}/zombies/doors/read_price
execute store result score #door_link {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.door.link
execute store result storage {ns}:temp _door_hover.id int 1 run scoreboard players get #door_link {ns}.data
execute if entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name_back with storage {ns}:temp _door_hover
execute unless entity @e[tag=bs.interaction.target,tag={ns}.door_back] run function {ns}:v{version}/zombies/doors/get_hover_name with storage {ns}:temp _door_hover
execute unless score #door_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{door_hover_message},priority:"conditional",freeze:5}}
execute if score #door_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{door_hover_partial_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/start", f"""
# Group 0 is the starting area; compound keys for quick lookup.
data modify storage {ns}:zombies game.unlocked_groups set value {{"0": 1b}}
""")

	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.doors[0] run function {ns}:v{version}/zombies/doors/setup
""")

