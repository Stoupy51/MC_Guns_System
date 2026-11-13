""" Loading a slot: the map starts as usual, then the saved state is replayed on top without any feedback. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import REMAINING_BULLETS
from ...helpers import MGS_TAG
from ..machines.perks.definitions import PERK_DEFINITIONS
from .schema import FORMAT, MAP_SCORES, PLAYER_SCORES


# Functions
def write_save_restore() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	loading: str = f"storage {ns}:zombies_saves loading"

	## Run by an operator with {slot:0..4}. `loading` stays until preload_complete replays it.
	write_versioned_function("zombies/save/load", f"""
execute unless data storage {ns}:zombies game{{state:"lobby"}} run return run tellraw @s [{MGS_TAG},{{"text":"A zombies game is running: stop it before loading a save.","color":"red"}}]
$data modify {loading} set from storage {ns}:zombies_saves slots[$(slot)]
execute unless data {loading}.format run return run function {ns}:v{version}/zombies/save/load_refused {{reason:"This slot is empty."}}
execute unless data {loading}{{format:{FORMAT}}} run return run function {ns}:v{version}/zombies/save/load_refused {{reason:"This save comes from a newer version of the pack."}}

data modify storage {ns}:temp _sv_map.map_id set from {loading}.map_id
function {ns}:v{version}/zombies/load_map_from_storage with storage {ns}:temp _sv_map
data remove storage {ns}:temp map_load
execute unless score #map_load_found {ns}.data matches 1 run return run function {ns}:v{version}/zombies/save/load_refused {{reason:"The map of this save no longer exists."}}

# The saved players online join whoever is already in the game.
execute as @a run function {ns}:v{version}/zombies/save/enlist_player
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run return run function {ns}:v{version}/zombies/save/load_refused {{reason:"No player of this save is online."}}

data modify storage {ns}:zombies game.map_id set from {loading}.map_id
data modify storage {ns}:zombies game.variant set from {loading}.variant
function {ns}:v{version}/zombies/start
execute unless data storage {ns}:zombies game{{state:"preparing"}} run data remove {loading}
""")

	write_versioned_function("zombies/save/load_refused", f"""
data remove {loading}
$tellraw @s [{MGS_TAG},{{"text":"$(reason)","color":"red"}}]
""")

	write_versioned_function("zombies/save/enlist_player", f"""
function {ns}:v{version}/zombies/save/find_player
execute if data storage {ns}:temp _sv_player run scoreboard players set @s {ns}.zb.in_game 1
data remove storage {ns}:temp _sv_player
""")

	## Run as a player: their entry of `loading.players` into temp _sv_player, matched by UUID, or nothing.
	write_versioned_function("zombies/save/find_player", f"""
data remove storage {ns}:temp _sv_player
data modify storage {ns}:temp _sv_find set from {loading}.players
execute if data storage {ns}:temp _sv_find[0] run function {ns}:v{version}/zombies/save/find_player_next
data remove storage {ns}:temp _sv_find
""")

	# A data modify that changes nothing fails, so a failed copy over the player's UUID is a match.
	write_versioned_function("zombies/save/find_player_next", f"""
data modify storage {ns}:temp _sv_uuid set from entity @s UUID
execute store success score #sv_differs {ns}.data run data modify storage {ns}:temp _sv_uuid set from storage {ns}:temp _sv_find[0].uuid
execute if score #sv_differs {ns}.data matches 0 run return run data modify storage {ns}:temp _sv_player set from storage {ns}:temp _sv_find[0]

data remove storage {ns}:temp _sv_find[0]
execute if data storage {ns}:temp _sv_find[0] run function {ns}:v{version}/zombies/save/find_player_next
""")

	## The end of preload_complete, once every element of the map is set up.
	write_versioned_function("zombies/preload_complete", f"""
execute if data {loading} run function {ns}:v{version}/zombies/save/restore
""")

	map_scores: str = "\n".join(
		f"""data modify storage {ns}:temp _sv_iter set from {loading}.map.{row.element}
execute if data storage {ns}:temp _sv_iter[0] run function {ns}:v{version}/zombies/save/restore_{row.element}"""
		for row in MAP_SCORES
	)
	write_versioned_function("zombies/save/restore", f"""
# start_round adds one: the next round is the one after the saved round.
data modify storage {ns}:zombies game.round set from {loading}.round
execute store result score #zb_round {ns}.data run data get {loading}.round
data modify storage {ns}:temp _sv_missing set value []

execute if data {loading}.map{{power:1b}} run function {ns}:v{version}/zombies/power/turn_on

# Opening a door unlocks its spawn groups. anim 1 removes the block without the break effect.
data modify storage {ns}:temp _sv_iter set from {loading}.map.opened
execute if data storage {ns}:temp _sv_iter[0] run function {ns}:v{version}/zombies/save/restore_door_open

{map_scores}
execute as @e[type=minecraft:block_display,tag={ns}.barricade_display,scores={{{ns}.zb.barricade.state=1}}] run function {ns}:v{version}/zombies/barricades/break

execute store result score #mb_pulls {ns}.data run data get {loading}.map.box_pulls
execute store result score #mb_dry_ray_gun {ns}.data run data get {loading}.map.box_dry_ray_gun
execute if data {loading}.map.box run function {ns}:v{version}/zombies/save/restore_box
execute store result score #wf_uses {ns}.data run data get {loading}.map.wunderfizz_uses
execute if data {loading}.map.wunderfizz run function {ns}:v{version}/zombies/save/restore_wunderfizz

execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/save/restore_player

execute if data storage {ns}:temp _sv_missing[0] run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Map elements of the save missing from this map, skipped: ","color":"gold"}},{{"storage":"{ns}:temp","nbt":"_sv_missing[]","color":"yellow"}}]
data remove storage {ns}:temp _sv_missing
data remove storage {ns}:temp _sv_iter
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Save ","color":"green"}},{{"storage":"{ns}:zombies_saves","nbt":"loading.name","color":"gold"}},{{"text":" loaded. Round ","color":"green"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold"}},{{"text":" is over, the next one starts in 10 seconds!","color":"green"}}]
data remove {loading}
""")

	write_versioned_function("zombies/save/restore_door_open", f"""
execute store result score #sv_id {ns}.data run data get storage {ns}:temp _sv_iter[0]
scoreboard players set #sv_found {ns}.data 0
execute as @e[type=minecraft:interaction,tag={ns}.door] if score @s {ns}.zb.door.link = #sv_id {ns}.data run scoreboard players set #sv_found {ns}.data 1
execute if score #sv_found {ns}.data matches 0 run data modify storage {ns}:temp _sv_missing append value {{element:"doors",id:0}}
execute if score #sv_found {ns}.data matches 0 store result storage {ns}:temp _sv_missing[-1].id int 1 run scoreboard players get #sv_id {ns}.data
execute as @e[type=minecraft:interaction,tag={ns}.door] if score @s {ns}.zb.door.link = #sv_id {ns}.data run scoreboard players set @s {ns}.zb.door.anim 1
execute as @e[type=minecraft:interaction,tag={ns}.door] if score @s {ns}.zb.door.link = #sv_id {ns}.data at @s run function {ns}:v{version}/zombies/doors/open_one

data remove storage {ns}:temp _sv_iter[0]
execute if data storage {ns}:temp _sv_iter[0] run function {ns}:v{version}/zombies/save/restore_door_open
""")

	for row in MAP_SCORES:
		selector: str = row.selector.format(ns=ns)
		write_versioned_function(f"zombies/save/restore_{row.element}", f"""
execute store result score #sv_id {ns}.data run data get storage {ns}:temp _sv_iter[0].id
execute store result score #sv_value {ns}.data run data get storage {ns}:temp _sv_iter[0].{row.key}
scoreboard players set #sv_found {ns}.data 0
execute as @e[{selector}] if score @s {ns}.{row.id_objective} = #sv_id {ns}.data store success score #sv_found {ns}.data run scoreboard players operation @s {ns}.{row.objective} = #sv_value {ns}.data
execute if score #sv_found {ns}.data matches 0 run data modify storage {ns}:temp _sv_missing append value {{element:"{row.element}",id:0}}
execute if score #sv_found {ns}.data matches 0 store result storage {ns}:temp _sv_missing[-1].id int 1 run scoreboard players get #sv_id {ns}.data

data remove storage {ns}:temp _sv_iter[0]
execute if data storage {ns}:temp _sv_iter[0] run function {ns}:v{version}/zombies/save/restore_{row.element}
""")

	write_versioned_function("zombies/save/restore_box", f"""
execute store result score #sv_id {ns}.data run data get {loading}.map.box
scoreboard players set #sv_found {ns}.data 0
execute as @e[tag={ns}.mystery_box_pos] if score @s {ns}.mb.box = #sv_id {ns}.data run scoreboard players set #sv_found {ns}.data 1
execute if score #sv_found {ns}.data matches 0 run return run data modify storage {ns}:temp _sv_missing append value {{element:"box"}}

tag @e[tag={ns}.mystery_box_active] remove {ns}.mystery_box_active
execute as @e[tag={ns}.mystery_box_pos] if score @s {ns}.mb.box = #sv_id {ns}.data run tag @s add {ns}.mystery_box_active
function {ns}:v{version}/zombies/mystery_box/sync_presence_display
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	write_versioned_function("zombies/save/restore_wunderfizz", f"""
execute store result score #sv_id {ns}.data run data get {loading}.map.wunderfizz
scoreboard players set #sv_found {ns}.data 0
execute as @e[tag={ns}.wunderfizz_machine] if score @s {ns}.zb.wf.id = #sv_id {ns}.data run scoreboard players set #sv_found {ns}.data 1
execute if score #sv_found {ns}.data matches 0 run return run data modify storage {ns}:temp _sv_missing append value {{element:"wunderfizz"}}

tag @e[tag={ns}.wf_active] remove {ns}.wf_active
execute as @e[tag={ns}.wunderfizz_machine] if score @s {ns}.zb.wf.id = #sv_id {ns}.data run tag @s add {ns}.wf_active
function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility
""")

	player_scores: str = "\n".join(
		f"execute store result score @s {ns}.{row.objective} run data get storage {ns}:temp _sv_player.scores.{row.key}"
		for row in PLAYER_SCORES
	)
	perk_effects: str = "\n".join(
		f"execute if score @s {ns}.zb.perk.{perk_id} matches 1 run {command.replace('{ns}', ns).replace('{version}', version)}"
		for perk_id, perk in PERK_DEFINITIONS.items()
		for command in perk.commands
	)
	## Run as a roster player, at them. One who is not in the save keeps the fresh start they got.
	write_versioned_function("zombies/save/restore_player", f"""
function {ns}:v{version}/zombies/save/find_player
execute unless data storage {ns}:temp _sv_player run return 0

# Their passive is restored, so the Zonweeb pick is not asked again.
dialog clear @s
{player_scores}
# Or the XP tracker reads the restored points as earned.
scoreboard players operation @s {ns}.zb.xp_pts_prev = @s {ns}.zb.points

# Before the inventory, which already holds what some perks give.
{perk_effects}

function {ns}:v{version}/zombies/save/rebuild_weapons
data modify storage {ns}:temp _restore.items set from storage {ns}:temp _sv_items
data remove storage {ns}:temp _sv_items
function {ns}:v{version}/zombies/inventory/restore_inventory
# The held gun's ammo moves to the score on the next weapon switch check.
scoreboard players set @s {ns}.last_selected 0
function {ns}:v{version}/zombies/inventory/refresh_perk_items
data remove storage {ns}:temp _sv_player
""")

	# Item stats are frozen in custom_data, so a gun saved on an older version is rebuilt from today's loot table
	# with its Pack-a-Punch level reapplied; the rest of its state and its look carry over.
	gun: str = f'storage {ns}:temp _sv_item.components."minecraft:custom_data".{ns}'
	fresh: str = f'storage {ns}:temp _sv_fresh.components."minecraft:custom_data".{ns}'
	carried_stats: str = "\n".join(
		f"execute if data {gun}.stats.{field} run data modify {fresh}.stats.{field} set from {gun}.stats.{field}"
		for field in (REMAINING_BULLETS, "fire_mode", "models", "scope_level")
	)
	pap_look: str = "\n".join(
		f'data modify storage {ns}:temp _sv_fresh.components."minecraft:{component}" set from storage {ns}:temp _sv_item.components."minecraft:{component}"'
		for component in ("item_name", "lore", "item_model")
	)

	## Run as a player, at them: _sv_player.inventory into _sv_items, guns rebuilt.
	write_versioned_function("zombies/save/rebuild_weapons", f"""
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.sv_rebuild","{ns}.zombies_entity"]}}
data modify storage {ns}:temp _sv_items set value []
data modify storage {ns}:temp _sv_source set from storage {ns}:temp _sv_player.inventory
execute if data storage {ns}:temp _sv_source[0] run function {ns}:v{version}/zombies/save/rebuild_next
kill @e[type=minecraft:item_display,tag={ns}.sv_rebuild]
data remove storage {ns}:temp _sv_source
""")

	write_versioned_function("zombies/save/rebuild_next", f"""
data modify storage {ns}:temp _sv_item set from storage {ns}:temp _sv_source[0]
execute if data {gun}.gun run function {ns}:v{version}/zombies/save/rebuild_gun with {gun}.stats
data modify storage {ns}:temp _sv_items append from storage {ns}:temp _sv_item

data remove storage {ns}:temp _sv_source[0]
execute if data storage {ns}:temp _sv_source[0] run function {ns}:v{version}/zombies/save/rebuild_next
""")

	## A gun whose weapon no longer exists stays as it was saved.
	write_versioned_function("zombies/save/rebuild_gun", f"""
item replace entity @n[type=minecraft:item_display,tag={ns}.sv_rebuild] contents with minecraft:air
$loot replace entity @n[type=minecraft:item_display,tag={ns}.sv_rebuild] contents loot {ns}:i/$(base_weapon)
execute unless data entity @n[type=minecraft:item_display,tag={ns}.sv_rebuild] item run return 0
data modify storage {ns}:temp _sv_fresh set from entity @n[type=minecraft:item_display,tag={ns}.sv_rebuild] item
data modify storage {ns}:temp _sv_fresh.Slot set from storage {ns}:temp _sv_item.Slot

execute if data {gun}.stats.pap_level run function {ns}:v{version}/zombies/save/rebuild_pap
{carried_stats}
data modify storage {ns}:temp _sv_item set from storage {ns}:temp _sv_fresh
""")

	## The overrides of zombies/pap/purchase for the saved level, on the fresh stats. The look is the saved one: name, lore and camo model.
	write_versioned_function("zombies/save/rebuild_pap", f"""
data modify storage {ns}:temp _pap_extract set value {{}}
data modify storage {ns}:temp _pap_extract.stats set from {fresh}.stats
execute store result score #pap_next_idx {ns}.data run data get {gun}.stats.pap_level
scoreboard players remove #pap_next_idx {ns}.data 1
function {ns}:v{version}/zombies/pap/apply_runtime_overrides
data modify {fresh}.stats set from storage {ns}:temp _pap_extract.stats
data modify {fresh}.stats.pap_level set from {gun}.stats.pap_level
execute if data {gun}.weapon run data modify {fresh}.weapon set from {gun}.weapon
{pap_look}
""")

