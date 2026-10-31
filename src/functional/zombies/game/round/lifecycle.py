""" The rise animation, the death intercept and the spawn batch tick. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_lifecycle() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run from game_tick for every rising enemy.
	write_versioned_function("zombies/zombie_rise_tick", f"""
execute store result storage {ns}:temp _rise.dy double 0.001 run scoreboard players get @s {ns}.zb.rise_step
function {ns}:v{version}/zombies/zombie_rise_move with storage {ns}:temp _rise

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/zombie_finish_rise
""")

	write_versioned_function("zombies/zombie_rise_move", "$tp @s ~ ~$(dy) ~")

	## Run as a zb_rise_dust marker, at the surface a zombie is breaking through.
	write_versioned_function("zombies/rise_dust_tick", f"""
function {ns}:v{version}/zombies/rise_dust_particles with entity @s data
scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run kill @s
""")

	write_versioned_function("zombies/rise_dust_particles", r"""
$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~ ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]
""")

	write_versioned_function("zombies/zombie_finish_rise", f"""
data modify entity @s NoAI set value 0b
tag @s remove {ns}.zb_rising

# The stuck timeout counts from here, so a long rise does not eat into it.
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data

# The build already joins the horde; an enemy that missed it would make escort traders flee it.
team join {ns}.horde @s

# Walk-to spawn: only once the rise is over, since the escort freezes the enemy.
execute if data entity @s data.walk_to run function {ns}:v{version}/zombies/escort/start_to_target
""")

	## Intercept enemy death before vanilla event 60 (poof particles).
	write_versioned_function("zombies/death_watch_tick", f"""
# From the marker passenger to its vehicle, once DeathTime starts.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if data entity @s {{DeathTime:1s}} run function {ns}:v{version}/zombies/on_zombie_dying

# Death groan keyed on Health, which is 0 the instant it dies: DeathTime is preset to -16, so the intercept above
# lands 17 ticks late. zb_dying fires it once; other entities than zombies die with their own vocals.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if entity @s[type=minecraft:zombie,tag={ns}.zombie_round,tag=!{ns}.zb_dying] if data entity @s {{Health:0.0f}} run function {ns}:v{version}/zombies/vocals/death
""")

	## Intercept a dying enemy before DeathTime reaches 20.
	write_versioned_function("zombies/on_zombie_dying", f"""
execute unless entity @s[tag={ns}.zombie_round] run return 0

# Kill the death-watch marker while still mounted, so none are orphaned.
kill @n[type=minecraft:marker,tag={ns}.death_watch,distance=..1]

# Riders fight on as enemies of their own; the teleport below would take them along.
execute on passengers run ride @s dismount

# Special rounds never roll the drop table: they only drop the Max Ammo of their last enemy.
execute unless score #zb_special_round {ns}.data matches 1 run function {ns}:v{version}/zombies/powerups/check_drop

# Armed enemies have a 5% chance to drop a Max Ammo, whatever killed them, on top of the usual roll.
execute if entity @s[tag={ns}.armed] if predicate {{type:"minecraft:random_chance",chance:0.05}} run function {ns}:v{version}/zombies/max_ammo_at_self

# "Was this the last one" needs an exact count.
execute if score #zb_special_round {ns}.data matches 1 run function {ns}:v{version}/zombies/special_death

# Removed before vanilla death event 60 fires.
tp @s ~ -10000 ~
""")

	write_versioned_function("zombies/spawn_tick", f"""
scoreboard players remove #zb_spawn_timer {ns}.data 1
execute if score #zb_spawn_timer {ns}.data matches 1.. run return 0

function {ns}:v{version}/zombies/calc_spawn_timer

scoreboard players operation #zb_spawn_batch_remaining {ns}.data = #zb_spawn_batch {ns}.data
function {ns}:v{version}/zombies/spawn_batch_tick
""")

	## Spawns up to #zb_spawn_batch enemies, one per recursive call.
	write_versioned_function("zombies/spawn_batch_tick", f"""
execute if score #zb_to_spawn {ns}.data matches ..0 run return 0

# Special rounds release one enemy per timer tick, capped by how many are out.
execute if score #zb_special_round {ns}.data matches 1 run return run function {ns}:v{version}/zombies/spawn_special_capped

# With no open spawn the enemy stays queued, and the watchdog ends a round that never gets one.
function {ns}:v{version}/zombies/spawn_from/zombies
execute if score #zb_spawned {ns}.data matches 0 run return 0
scoreboard players remove #zb_to_spawn {ns}.data 1
scoreboard players remove #zb_spawn_batch_remaining {ns}.data 1

execute if score #zb_spawn_batch_remaining {ns}.data matches 1.. if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_batch_tick
""")

