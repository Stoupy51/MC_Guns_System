""" Intact and destroyed barricade ticks, plus restoring zombie speed after a freeze. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....progression import Xp

# Constants
SOUND_BANG: str = "zombies/barricade/bang"
""" 5 variants, 20-34 ticks: a zombie pounding the boards while it tears them off. """
SOUND_SNAP: str = "zombies/barricade/snap"
""" 6 variants, 8-26 ticks: a board coming loose. Punctuates the teardown. """
SOUND_SLAM: str = "zombies/barricade/slam"
""" 6 variants, 36-54 ticks: a board driven back into place. Punctuates the repair. """
SOUND_REPAIR: str = "zombies/barricade/repair_no_cash"
""" 67 ticks of sustained hammering, covering a whole rebuild. The `repair` variant next to it is the
same take with Treyarch's points ka-ching left in; we award points ourselves, so use the clean one. """

BANG_INTERVAL: int = 35
""" Ticks between pounding sounds for one player. Longer than the longest bang (34) so they never
overlap, and short enough that the 40-tick teardown gets one or two of them. """
REPAIR_INTERVAL: int = 80
""" Ticks before a player can hear the repair hammering again. Longer than the clip (67) so tapping
sneak to restart the repair cannot stack copies of it. """


# Functions
def write_barricade_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/barricades/intact_tick", f"""
# Upper barricades of a column share the floor-level detection.
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function {ns}:v{version}/zombies/barricades/intact_tick

# Run as the intact barricade display, at it.
execute store result score #barricade_id {ns}.data run scoreboard players get @s {ns}.zb.barricade.id
execute store result storage {ns}:temp _btick.radius int 1 run scoreboard players get @s {ns}.zb.barricade.radius

function {ns}:v{version}/zombies/barricades/freeze_zombies with storage {ns}:temp _btick

execute if score @s {ns}.zb.barricade.r_timer matches 1.. run function {ns}:v{version}/zombies/barricades/handle_removing with storage {ns}:temp _btick
execute if score @s {ns}.zb.barricade.r_timer matches 0 if score @s {ns}.zb.barricade.state matches 0 run function {ns}:v{version}/zombies/barricades/find_remover with storage {ns}:temp _btick
""")

	write_versioned_function("zombies/barricades/freeze_zombies", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add {ns}:freeze -1024 add_multiplied_total
$tag @e[tag={ns}.zombie_round,distance=..$(radius)] add {ns}.barricade_frozen

# Escort taxis are not zombie_round, so the freeze misses them and the glued zombie would walk through.
# Ending the escort hands the zombie back to normal AI, and the freeze catches it next tick.
$execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..$(radius)] at @s run function {ns}:v{version}/zombies/escort/end_at_trader
""")

	write_versioned_function("zombies/barricades/find_remover", f"""
# Run as the barricade display; $(radius) is the sphere radius. Picks the nearest eligible zombie.
scoreboard players set #barricade_found_remover {ns}.data 0
$execute as @e[tag={ns}.zombie_round,tag=!{ns}.barricade_removing,distance=..$(radius),limit=1,sort=nearest] run function {ns}:v{version}/zombies/barricades/start_removing_zombie
execute if score #barricade_found_remover {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barricade.r_timer 40
""")

	write_versioned_function("zombies/barricades/start_removing_zombie", f"""
# Run as the zombie assigned as remover.
tag @s add {ns}.barricade_removing
scoreboard players operation @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data
scoreboard players set #barricade_found_remover {ns}.data 1
""")

	write_versioned_function("zombies/barricades/handle_removing", f"""
# Run as the barricade display; $(radius) is the sphere radius.
scoreboard players set #barricade_remover_valid {ns}.data 0
$execute as @e[tag={ns}.barricade_removing,distance=..$(radius)] at @s if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run function {ns}:v{version}/zombies/barricades/on_remover_valid

execute if score #barricade_remover_valid {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.barricade.r_timer -= #tick_delta {ns}.data
execute if score #barricade_remover_valid {ns}.data matches 1 unless score @s {ns}.zb.barricade.r_timer matches 0.. run scoreboard players set @s {ns}.zb.barricade.r_timer 0
execute if score #barricade_remover_valid {ns}.data matches 1 if score @s {ns}.zb.barricade.r_timer matches 0 run function {ns}:v{version}/zombies/barricades/destroy

# Out of range (dead or pushed away): cancel so the zombie is freed.
execute if score #barricade_remover_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barricades/cancel_remove
""")

	write_versioned_function("zombies/barricades/on_remover_valid", f"""
# Run as the removing zombie, at it.
scoreboard players set #barricade_remover_valid {ns}.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1

# This runs every tick of the 40-tick teardown, so the bang is rate-limited per listening player.
# `as` keeps the position, so ~ ~ ~ is still the zombie.
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..32] unless score @s {ns}.zb.barricade.bang_at > #total_tick {ns}.data run function {ns}:v{version}/zombies/barricades/bang_for
""")

	## Run as a listening player, at the zombie tearing the boards off.
	write_versioned_function("zombies/barricades/bang_for", f"""
scoreboard players operation @s {ns}.zb.barricade.bang_at = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.barricade.bang_at {BANG_INTERVAL}
playsound {ns}:{SOUND_BANG} block @s ~ ~ ~ 1.0 1.0
""")

	write_versioned_function("zombies/barricades/cancel_remove", f"""
# Run as the barricade display: the remover left range or died.
scoreboard players set @s {ns}.zb.barricade.r_timer 0
execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing
""")

	write_versioned_function("zombies/barricades/destroy", f"""
# Run as the barricade display: intact to destroyed.
scoreboard players set @s {ns}.zb.barricade.state 1
scoreboard players set @s {ns}.zb.barricade.r_timer 0

execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing

data modify entity @s block_state set from entity @s data.block_disabled

particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound {ns}:{SOUND_SNAP} block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

	write_versioned_function("zombies/barricades/destroyed_tick", f"""
# Upper barricades of a column share the floor-level detection, so a player on the ground can repair them.
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function {ns}:v{version}/zombies/barricades/destroyed_tick

# Run as the destroyed barricade display, at it.
execute store result score #barricade_id {ns}.data run scoreboard players get @s {ns}.zb.barricade.id
execute store result storage {ns}:temp _brptick.radius int 1 run scoreboard players get @s {ns}.zb.barricade.radius

execute if score @s {ns}.zb.barricade.rp_timer matches 1.. run function {ns}:v{version}/zombies/barricades/handle_repair with storage {ns}:temp _brptick
execute if score @s {ns}.zb.barricade.rp_timer matches 0 if score @s {ns}.zb.barricade.state matches 1 run function {ns}:v{version}/zombies/barricades/find_repairer with storage {ns}:temp _brptick
""")

	write_versioned_function("zombies/barricades/find_repairer", f"""
# Run as the barricade display; $(radius) is the sphere radius. Picks the nearest sneaking in-game player.
scoreboard players set #barricade_found_repairer {ns}.data 0
$execute as @a[scores={{{ns}.zb.in_game=1}},predicate={ns}:v{version}/is_sneaking,distance=..$(radius),tag=!{ns}.barricade_repairing,limit=1,sort=nearest] run function {ns}:v{version}/zombies/barricades/start_repairing_player
execute if score #barricade_found_repairer {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barricade.rp_timer 30
""")

	write_versioned_function("zombies/barricades/start_repairing_player", f"""
# Run as the player assigned as repairer, at the barricade.
tag @s add {ns}.barricade_repairing
scoreboard players operation @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data
scoreboard players set #barricade_found_repairer {ns}.data 1

# Played once: the clip lasts longer than the 30-tick repair.
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..32] unless score @s {ns}.zb.barricade.rep_at > #total_tick {ns}.data run function {ns}:v{version}/zombies/barricades/repair_sound_for
""")

	## Run as a listening player, at the barricade being repaired.
	write_versioned_function("zombies/barricades/repair_sound_for", f"""
scoreboard players operation @s {ns}.zb.barricade.rep_at = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.barricade.rep_at {REPAIR_INTERVAL}
playsound {ns}:{SOUND_REPAIR} block @s ~ ~ ~ 1.0 1.0
""")

	write_versioned_function("zombies/barricades/handle_repair", f"""
# Run as the barricade display; $(radius) is the sphere radius.
execute store result score #barricade_rp_cur {ns}.data run scoreboard players get @s {ns}.zb.barricade.rp_timer
scoreboard players set #barricade_repair_valid {ns}.data 0
$execute as @a[tag={ns}.barricade_repairing,distance=..$(radius)] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data if predicate {ns}:v{version}/is_sneaking run function {ns}:v{version}/zombies/barricades/on_repairer_valid

execute if score #barricade_repair_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barricades/cancel_repair
execute if score #barricade_repair_valid {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.barricade.rp_timer -= #tick_delta {ns}.data
execute if score #barricade_repair_valid {ns}.data matches 1 unless score @s {ns}.zb.barricade.rp_timer matches 0.. run scoreboard players set @s {ns}.zb.barricade.rp_timer 0
execute if score #barricade_repair_valid {ns}.data matches 1 if score @s {ns}.zb.barricade.rp_timer matches 0 run function {ns}:v{version}/zombies/barricades/repair
""")

	write_versioned_function("zombies/barricades/on_repairer_valid", f"""
# Run as the repairing player.
scoreboard players set #barricade_repair_valid {ns}.data 1
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🔧 ","color":"white"}},{{"text":"Repairing barricade... ","color":"aqua"}},{{"score":{{"name":"#barricade_rp_cur","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/30","color":"gray"}}],priority:"conditional",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/barricades/cancel_repair", f"""
# Run as the barricade display: the repairer stopped sneaking or left range.
scoreboard players set @s {ns}.zb.barricade.rp_timer 0
execute as @a[tag={ns}.barricade_repairing] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_repairing
""")

	write_versioned_function("zombies/barricades/repair", f"""
# Run as the barricade display: destroyed to intact.
scoreboard players set @s {ns}.zb.barricade.state 0
scoreboard players set @s {ns}.zb.barricade.rp_timer 0

execute as @a[tag={ns}.barricade_repairing] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data run function {ns}:v{version}/zombies/barricades/on_repair_complete_player

data modify entity @s block_state set from entity @s data.block_enabled

execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing

particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 10
playsound {ns}:{SOUND_SLAM} block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

	write_versioned_function("zombies/barricades/on_repair_complete_player", f"""
# Run as the repairing player.
tag @s remove {ns}.barricade_repairing

# +10 points, for at most 25 repairs per round.
execute unless score @s {ns}.zb.barricade_repairs matches 25.. run scoreboard players add @s {ns}.zb.points 10
execute unless score @s {ns}.zb.barricade_repairs matches 25.. run scoreboard players add @s {ns}.zb.barricade_repairs 1

data modify storage smithed.actionbar:input message set value {{json:[{{"text":"✔ Barricade repaired! ","color":"green"}},{{"text":"+10","color":"gold"}},{{"text":" points","color":"yellow"}},{Xp.suffix("zb", "barricade")}],priority:"notification",freeze:20}}
{Xp.give("zb", "barricade")}
function #smithed.actionbar:message
""")

	## Runs before the freeze each tick.
	write_versioned_function("zombies/barricades/restore_zombie_speed", f"""
attribute @s minecraft:movement_speed modifier remove {ns}:freeze
tag @s remove {ns}.barricade_frozen
""")

