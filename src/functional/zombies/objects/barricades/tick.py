""" Intact and destroyed barricade ticks, plus restoring zombie speed after a freeze. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_barricade_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Intact barricade tick
	write_versioned_function("zombies/barricades/intact_tick", f"""
# Delegate detection downward if floating (upper barricades in a column share floor-level detection)
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function {ns}:v{version}/zombies/barricades/intact_tick

# @s = intact barricade display, at @s
execute store result score #barricade_id {ns}.data run scoreboard players get @s {ns}.zb.barricade.id
execute store result storage {ns}:temp _btick.radius int 1 run scoreboard players get @s {ns}.zb.barricade.radius

# Freeze all zombies in radius (macro)
function {ns}:v{version}/zombies/barricades/freeze_zombies with storage {ns}:temp _btick

# Handle remove timer or find a new remover (both macros using radius)
execute if score @s {ns}.zb.barricade.r_timer matches 1.. run function {ns}:v{version}/zombies/barricades/handle_removing with storage {ns}:temp _btick
execute if score @s {ns}.zb.barricade.r_timer matches 0 if score @s {ns}.zb.barricade.state matches 0 run function {ns}:v{version}/zombies/barricades/find_remover with storage {ns}:temp _btick
""")

	write_versioned_function("zombies/barricades/freeze_zombies", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add {ns}:freeze -1024 add_multiplied_total
$tag @e[tag={ns}.zombie_round,distance=..$(radius)] add {ns}.barricade_frozen

# Escort taxis (invisible wandering traders) ignore the freeze — they aren't zombie_round and the
# glued zombie is force-tp'd onto them each tick, so an escorted zombie would walk straight through
# a barricade. End the escort on contact instead: the zombie drops to normal AI and the freeze above
# catches it next tick, so it respects the barricade (and can remove it) like any other zombie.
$execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..$(radius)] at @s run function {ns}:v{version}/zombies/escort/end_at_trader
""")

	write_versioned_function("zombies/barricades/find_remover", f"""
# MACRO: @s = intact barricade marker, $(radius) = sphere radius
# Picks nearest eligible zombie and assigns it as remover
scoreboard players set #barricade_found_remover {ns}.data 0
$execute as @e[tag={ns}.zombie_round,tag=!{ns}.barricade_removing,distance=..$(radius),limit=1,sort=nearest] run function {ns}:v{version}/zombies/barricades/start_removing_zombie
execute if score #barricade_found_remover {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barricade.r_timer 40
""")

	write_versioned_function("zombies/barricades/start_removing_zombie", f"""
# @s = zombie assigned as remover
tag @s add {ns}.barricade_removing
scoreboard players operation @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data
scoreboard players set #barricade_found_remover {ns}.data 1
""")

	write_versioned_function("zombies/barricades/handle_removing", f"""
# MACRO: @s = intact barricade marker, $(radius) = sphere radius
# Verify assigned remover is still in range and matches this barricade
scoreboard players set #barricade_remover_valid {ns}.data 0
$execute as @e[tag={ns}.barricade_removing,distance=..$(radius)] at @s if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run function {ns}:v{version}/zombies/barricades/on_remover_valid

execute if score #barricade_remover_valid {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.barricade.r_timer -= #tick_delta {ns}.data
execute if score #barricade_remover_valid {ns}.data matches 1 unless score @s {ns}.zb.barricade.r_timer matches 0.. run scoreboard players set @s {ns}.zb.barricade.r_timer 0
execute if score #barricade_remover_valid {ns}.data matches 1 if score @s {ns}.zb.barricade.r_timer matches 0 run function {ns}:v{version}/zombies/barricades/destroy

# Not in range (dead or pushed out): always cancel so the zombie is freed
execute if score #barricade_remover_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barricades/cancel_remove
""")

	write_versioned_function("zombies/barricades/on_remover_valid", f"""
# @s = removing zombie, at zombie position (via at @s in handle_removing selector)
scoreboard players set #barricade_remover_valid {ns}.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1
""")

	write_versioned_function("zombies/barricades/cancel_remove", f"""
# @s = barricade display — remover left range or died
scoreboard players set @s {ns}.zb.barricade.r_timer 0
execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing
""")

	write_versioned_function("zombies/barricades/destroy", f"""
# @s = intact barricade display → transitions to destroyed
scoreboard players set @s {ns}.zb.barricade.state 1
scoreboard players set @s {ns}.zb.barricade.r_timer 0

# Clean up removing zombie
execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing

# Switch to disabled block state
data modify entity @s block_state set from entity @s data.block_disabled

# Sound + particles
particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound minecraft:entity.zombie.break_wooden_door block @a[distance=..32] ~ ~ ~ 1.0 1.0
""")

	## Destroyed barricade tick
	write_versioned_function("zombies/barricades/destroyed_tick", f"""
# Delegate detection downward if floating (upper barricades in a column share floor-level repair
# detection) so a player standing on the ground can reach and repair a barricade stacked above them.
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function {ns}:v{version}/zombies/barricades/destroyed_tick

# @s = destroyed barricade display, at @s
execute store result score #barricade_id {ns}.data run scoreboard players get @s {ns}.zb.barricade.id
execute store result storage {ns}:temp _brptick.radius int 1 run scoreboard players get @s {ns}.zb.barricade.radius

# Handle repair timer or find a new repairer (both macros using radius)
execute if score @s {ns}.zb.barricade.rp_timer matches 1.. run function {ns}:v{version}/zombies/barricades/handle_repair with storage {ns}:temp _brptick
execute if score @s {ns}.zb.barricade.rp_timer matches 0 if score @s {ns}.zb.barricade.state matches 1 run function {ns}:v{version}/zombies/barricades/find_repairer with storage {ns}:temp _brptick
""")

	write_versioned_function("zombies/barricades/find_repairer", f"""
# MACRO: @s = destroyed barricade marker, $(radius) = sphere radius
# Picks nearest sneaking in-game player and assigns them as repairer
scoreboard players set #barricade_found_repairer {ns}.data 0
$execute as @a[scores={{{ns}.zb.in_game=1}},predicate={ns}:v{version}/is_sneaking,distance=..$(radius),tag=!{ns}.barricade_repairing,limit=1,sort=nearest] run function {ns}:v{version}/zombies/barricades/start_repairing_player
execute if score #barricade_found_repairer {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barricade.rp_timer 30
""")

	write_versioned_function("zombies/barricades/start_repairing_player", f"""
# @s = player assigned as repairer
tag @s add {ns}.barricade_repairing
scoreboard players operation @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data
scoreboard players set #barricade_found_repairer {ns}.data 1
""")

	write_versioned_function("zombies/barricades/handle_repair", f"""
# MACRO: @s = destroyed barricade marker, $(radius) = sphere radius
# Verify assigned repairer is still valid (sneaking, in range, correct id)
execute store result score #barricade_rp_cur {ns}.data run scoreboard players get @s {ns}.zb.barricade.rp_timer
scoreboard players set #barricade_repair_valid {ns}.data 0
$execute as @a[tag={ns}.barricade_repairing,distance=..$(radius)] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data if predicate {ns}:v{version}/is_sneaking run function {ns}:v{version}/zombies/barricades/on_repairer_valid

execute if score #barricade_repair_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barricades/cancel_repair
execute if score #barricade_repair_valid {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.barricade.rp_timer -= #tick_delta {ns}.data
execute if score #barricade_repair_valid {ns}.data matches 1 unless score @s {ns}.zb.barricade.rp_timer matches 0.. run scoreboard players set @s {ns}.zb.barricade.rp_timer 0
execute if score #barricade_repair_valid {ns}.data matches 1 if score @s {ns}.zb.barricade.rp_timer matches 0 run function {ns}:v{version}/zombies/barricades/repair
""")

	write_versioned_function("zombies/barricades/on_repairer_valid", f"""
# @s = repairing player
scoreboard players set #barricade_repair_valid {ns}.data 1
# Actionbar progress: show remaining ticks out of 30
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🔧 Repairing barricade... ","color":"aqua"}},{{"score":{{"name":"#barricade_rp_cur","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/30","color":"gray"}}],priority:"conditional",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/barricades/cancel_repair", f"""
# @s = barricade display — repairer stopped sneaking or left range
scoreboard players set @s {ns}.zb.barricade.rp_timer 0
execute as @a[tag={ns}.barricade_repairing] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_repairing
""")

	write_versioned_function("zombies/barricades/repair", f"""
# @s = destroyed barricade display → transitions back to intact
scoreboard players set @s {ns}.zb.barricade.state 0
scoreboard players set @s {ns}.zb.barricade.rp_timer 0

# Clean up repairing player tag and show success
execute as @a[tag={ns}.barricade_repairing] if score @s {ns}.zb.barricade.repairing_id = #barricade_id {ns}.data run function {ns}:v{version}/zombies/barricades/on_repair_complete_player

# Switch back to enabled block state
data modify entity @s block_state set from entity @s data.block_enabled

# Clear any leftover barricade_removing tag from zombies associated with this barricade
execute as @e[tag={ns}.barricade_removing] if score @s {ns}.zb.barricade.removing_id = #barricade_id {ns}.data run tag @s remove {ns}.barricade_removing

# Sound + particles
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 10
playsound minecraft:block.anvil.use block @a[distance=..32] ~ ~ ~ 1.0 1.5
""")

	write_versioned_function("zombies/barricades/on_repair_complete_player", f"""
# @s = repairing player
tag @s remove {ns}.barricade_repairing

# Reward +10 points (max 25 barricade repairs rewarded per round)
execute unless score @s {ns}.zb.barricade_repairs matches 25.. run scoreboard players add @s {ns}.zb.points 10
execute unless score @s {ns}.zb.barricade_repairs matches 25.. run scoreboard players add @s {ns}.zb.barricade_repairs 1

data modify storage smithed.actionbar:input message set value {{json:[{{"text":"✔ Barricade repaired! ","color":"green"}},{{"text":"+10","color":"gold"}},{{"text":" points","color":"yellow"}}],priority:"notification",freeze:20}}
function #smithed.actionbar:message
""")

	## Restore zombie movement speed after barricade freeze (called before freeze each tick)
	write_versioned_function("zombies/barricades/restore_zombie_speed", f"""
# @s = frozen zombie — restore level-appropriate speed
attribute @s minecraft:movement_speed modifier remove {ns}:freeze
tag @s remove {ns}.barricade_frozen
""")

