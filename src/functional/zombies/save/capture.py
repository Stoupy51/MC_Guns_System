""" Saving a run into a slot between two rounds, then stopping it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from .schema import FORMAT, MAP_SCORES, PLAYER_SCORES


# Functions
def write_save_capture() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	slot: str = f"storage {ns}:zombies_saves _slot"

	## Run by an operator with {slot:0..4, name:"..."}. #zb_next_round only counts down in the gap after round_complete.
	write_versioned_function("zombies/save/save", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
execute unless score #zb_next_round {ns}.data matches 1.. run return run tellraw @s [{MGS_TAG},{{"text":"A game can only be saved between two rounds.","color":"red"}}]

$data modify {slot} set value {{format:{FORMAT},pack:"{version}",name:"$(name)",players:[],map:{{opened:[]}}}}
data modify {slot}.map_id set from storage {ns}:zombies game.map_id
data modify {slot}.variant set from storage {ns}:zombies game.variant
data modify {slot}.round set from storage {ns}:zombies game.round
execute store result {slot}.saved_at long 1 run time query gametime

execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/save/capture_player
function {ns}:v{version}/zombies/save/capture_map

$data modify storage {ns}:zombies_saves slots[$(slot)] set from {slot}
data remove {slot}

$tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Game saved as ","color":"green"}},{{"text":"$(name)","color":"gold"}},{{"text":".","color":"green"}}]
function {ns}:v{version}/zombies/stop
""")

	player_scores: str = "\n".join(
		f"execute store result {slot}.players[-1].scores.{row.key} int 1 run scoreboard players get @s {ns}.{row.objective}"
		for row in PLAYER_SCORES
	)
	## Run as an online roster player. The held gun keeps its ammo in a score, so it goes back on the item first.
	write_versioned_function("zombies/save/capture_player", f"""
function {ns}:v{version}/ammo/update_old_weapon

data modify {slot}.players append value {{scores:{{}}}}
data modify {slot}.players[-1].uuid set from entity @s UUID
data modify {slot}.players[-1].inventory set from entity @s Inventory
{player_scores}
""")

	map_scores: str = "\n".join(
		f"execute as @e[{row.selector.format(ns=ns)}] run function {ns}:v{version}/zombies/save/capture_{row.element}"
		for row in MAP_SCORES
	)
	write_versioned_function("zombies/save/capture_map", f"""
execute store result {slot}.map.power byte 1 run scoreboard players get #zb_power {ns}.data

# An opened door group has no entity left: a map door whose link id matches none was opened.
data modify storage {ns}:temp _sv_doors set from storage {ns}:zombies game.map.doors
execute if data storage {ns}:temp _sv_doors[0] run function {ns}:v{version}/zombies/save/capture_door_open

execute store result {slot}.map.box_pulls int 1 run scoreboard players get #mb_pulls {ns}.data
execute store result {slot}.map.box_dry_ray_gun int 1 run scoreboard players get #mb_dry_ray_gun {ns}.data
execute as @e[tag={ns}.mystery_box_active,limit=1] store result {slot}.map.box int 1 run scoreboard players get @s {ns}.mb.box
execute store result {slot}.map.wunderfizz_uses int 1 run scoreboard players get #wf_uses {ns}.data
execute as @e[tag={ns}.wf_active,limit=1] store result {slot}.map.wunderfizz int 1 run scoreboard players get @s {ns}.zb.wf.id

{map_scores}
tag @e[tag={ns}.sv_captured] remove {ns}.sv_captured
""")

	## Several map doors share a link id: the group is checked once, then all of its entries leave the list.
	write_versioned_function("zombies/save/capture_door_open", f"""
execute store result score #sv_id {ns}.data run data get storage {ns}:temp _sv_doors[0].link_id
scoreboard players set #sv_found {ns}.data 0
execute as @e[type=minecraft:interaction,tag={ns}.door] if score @s {ns}.zb.door.link = #sv_id {ns}.data run scoreboard players set #sv_found {ns}.data 1
execute if score #sv_found {ns}.data matches 0 run data modify {slot}.map.opened append from storage {ns}:temp _sv_doors[0].link_id

data remove storage {ns}:temp _sv_doors[0]
execute store result storage {ns}:temp _sv_link.id int 1 run scoreboard players get #sv_id {ns}.data
function {ns}:v{version}/zombies/save/forget_door_link with storage {ns}:temp _sv_link
execute if data storage {ns}:temp _sv_doors[0] run function {ns}:v{version}/zombies/save/capture_door_open
""")
	write_versioned_function("zombies/save/forget_door_link", f"$data remove storage {ns}:temp _sv_doors[{{link_id:$(id)}}]")

	# An element made of several entities sharing its id (a door is one interaction per block) is captured once.
	for row in MAP_SCORES:
		write_versioned_function(f"zombies/save/capture_{row.element}", f"""
execute if entity @s[tag={ns}.sv_captured] run return 0
scoreboard players operation #sv_id {ns}.data = @s {ns}.{row.id_objective}
execute as @e[{row.selector.format(ns=ns)}] if score @s {ns}.{row.id_objective} = #sv_id {ns}.data run tag @s add {ns}.sv_captured

data modify {slot}.map.{row.element} append value {{}}
execute store result {slot}.map.{row.element}[-1].id int 1 run scoreboard players get @s {ns}.{row.id_objective}
execute store result {slot}.map.{row.element}[-1].{row.key} int 1 run scoreboard players get @s {ns}.{row.objective}
""")

