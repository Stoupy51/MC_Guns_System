""" Tombstone: the marker left behind on a bleed-out and recovering perks and weapons from it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from .definitions import PERK_DEFINITIONS, TOMBSTONE_PERKS


# Functions
def write_tombstone() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Tombstone (disabled solo): going down spawns a marker with the owner's perks, dropped on revive; a bleed-out leaves 60 s after the round respawn to recover perks and weapons.
	# Only an active Quick Revive is snapshotted: score 1 can also mean "solo uses exhausted".
	ts_snapshot: str = "\n".join(
		f"execute store success score @s {ns}.zb.tsp.{pid} if entity @s[tag={ns}.perk.quick_revive]"
		if pid == "quick_revive"
		else f"scoreboard players operation @s {ns}.zb.tsp.{pid} = @s {ns}.zb.perk.{pid}"
		for pid in TOMBSTONE_PERKS
	)
	ts_clear: str = "\n".join(f"scoreboard players set @s {ns}.zb.tsp.{pid} 0" for pid in TOMBSTONE_PERKS)

	# Silent re-apply for recovery: apply/<pid> would stack up to five purchase jingles and XP payouts in one tick.
	for pid, pdata in PERK_DEFINITIONS.items():
		cmds: str = "\n".join(c.replace("{ns}", ns).replace("{version}", version) for c in pdata.commands)
		if cmds:
			write_versioned_function(f"zombies/perks/reapply/{pid}", cmds)

	ts_restore_perks_lines: list[str] = []
	for pid in TOMBSTONE_PERKS:
		pdata = PERK_DEFINITIONS[pid]
		ts_restore_perks_lines.append(f"execute if score @s {ns}.zb.tsp.{pid} matches 1 run scoreboard players set @s {ns}.zb.perk.{pid} 1")
		if pdata.commands:
			ts_restore_perks_lines.append(f"execute if score @s {ns}.zb.tsp.{pid} matches 1 run function {ns}:v{version}/zombies/perks/reapply/{pid}")
	ts_restore_perks: str = "\n".join(ts_restore_perks_lines)

	# A skeleton skull laid flat, raised and enlarged so it reads from across the map.
	ts_tags: str = f'Tags:["{ns}.tombstone","{ns}.tombstone_new","{ns}.gm_entity"]'
	ts_item: str = 'item:{id:"minecraft:skeleton_skull",count:1},item_display:"ground"'
	ts_transform: str = (
		"transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],"
		"translation:[0f,0.3f,0f],scale:[1.2f,1.2f,1.2f]}"
	)
	ts_marker: str = f'{{{ts_tags},Glowing:true,billboard:"vertical",teleport_duration:1,{ts_item},{ts_transform}}}'

	# Run from revive/on_down before lose_all, as the player; the death position is in temp rv_x, rv_y, rv_z.
	write_versioned_function("zombies/perks/tombstone_on_down", f"""
# A solo bleed-out is game over, so there is nothing to recover to.
execute store result score #ts_ingame {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if score #ts_ingame {ns}.data matches ..1 run return 0

{ts_snapshot}

# Tagged with the owner's downed_id, then moved to the death spot.
summon minecraft:item_display ~ ~ ~ {ts_marker}
scoreboard players operation @n[tag={ns}.tombstone_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id
scoreboard players set @n[tag={ns}.tombstone_new] {ns}.zb.ts.state 0
scoreboard players set @n[tag={ns}.tombstone_new] {ns}.zb.ts.timer 0
function {ns}:v{version}/zombies/perks/tombstone_tp with storage {ns}:temp
tag @e[tag={ns}.tombstone_new] remove {ns}.tombstone_new
""")

	write_versioned_function("zombies/perks/tombstone_tp", f"""
$tp @n[tag={ns}.tombstone_new] $(rv_x) $(rv_y) $(rv_z)
""")

	# Run from revive_complete: the owner was revived, so the marker and snapshot go.
	write_versioned_function("zombies/perks/tombstone_on_revived", f"""
kill @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match]
{ts_clear}
""")

	# Run from bleed_out: snapshot the inventory while it is intact.
	write_versioned_function("zombies/perks/tombstone_on_bleed_out", f"""
execute unless entity @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] run return 0
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_snapshot_inv with storage {ns}:temp _ts_id
""")

	write_versioned_function("zombies/perks/tombstone_snapshot_inv", f"""
$data modify storage {ns}:zombies tombstone_inv."$(id)" set from entity @s Inventory
""")

	# Run from do_round_respawn: a pending marker starts its 60 s recovery timer.
	write_versioned_function("zombies/perks/tombstone_on_respawn", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute unless entity @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] run return 0
scoreboard players set @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] {ns}.zb.ts.state 1
scoreboard players set @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match] {ns}.zb.ts.timer 1200
{TitleTimes.EVENT.cmd()}
title @s title ["🪦"]
title @s subtitle [{{"text":"Return to your ","color":"gold"}},{{"text":"🪦","color":"white"}},{{"text":" within 60s to recover your gear!","color":"gold"}}]
""")

	# Run as an active marker, at it.
	ts_nearby_alive: str = f"@a[distance=..2,gamemode=!spectator,scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}}]"
	write_versioned_function("zombies/perks/tombstone_marker_tick", f"""
particle minecraft:soul ~ ~0.5 ~ 0.25 0.4 0.25 0.01 3 force @a[distance=..48]
particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.15 0.2 0.15 0.005 1 force @a[distance=..48]

scoreboard players operation @s {ns}.zb.ts.timer -= #tick_delta {ns}.data
execute if score @s {ns}.zb.ts.timer matches ..0 run return run function {ns}:v{version}/zombies/perks/tombstone_expire

# The owner within 2 blocks, alive and in game.
scoreboard players operation #ts_mid {ns}.data = @s {ns}.zb.downed_id
execute as {ts_nearby_alive} if score @s {ns}.zb.downed_id = #ts_mid {ns}.data run function {ns}:v{version}/zombies/perks/tombstone_collect
""")

	## Run as an expired marker.
	write_versioned_function("zombies/perks/tombstone_expire", f"""
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_clear_inv with storage {ns}:temp _ts_id
kill @s
""")

	write_versioned_function("zombies/perks/tombstone_clear_inv", f"""
$data remove storage {ns}:zombies tombstone_inv."$(id)"
""")

	## Run as the owner standing on their tombstone.
	write_versioned_function("zombies/perks/tombstone_collect", f"""
{ts_restore_perks}

# Juggernog's max health.
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Players cannot be data-modified, so the inventory goes back slot by slot through the shared restore system.
execute store result storage {ns}:temp _ts_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/perks/tombstone_load_snapshot with storage {ns}:temp _ts_id
function {ns}:v{version}/zombies/inventory/restore_inventory

function {ns}:v{version}/zombies/inventory/refresh_perk_items

{ts_clear}
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
kill @e[tag={ns}.tombstone,predicate={ns}:v{version}/zombies/revive/downed_id_match]

{TitleTimes.EVENT.cmd()}
title @s title ["🪦"]
title @s subtitle [{{"text":"Gear recovered!","color":"green"}}]
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.2
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":" recovered their gear from a tombstone!","color":"gray"}}]
""")

	write_versioned_function("zombies/perks/tombstone_load_snapshot", f"""
$data modify storage {ns}:temp _restore.items set from storage {ns}:zombies tombstone_inv."$(id)"
$data remove storage {ns}:zombies tombstone_inv."$(id)"
""")

	write_versioned_function("zombies/game_tick", f"""
execute as @e[type=minecraft:item_display,tag={ns}.tombstone,scores={{{ns}.zb.ts.state=1}}] at @s run function {ns}:v{version}/zombies/perks/tombstone_marker_tick
""")

