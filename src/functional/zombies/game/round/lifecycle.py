""" The rise animation, the death intercept and the spawn batch tick. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_lifecycle() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run from game_tick for every rising zombie.
	write_versioned_function("zombies/zombie_rise_tick", f"""
tp @s ~ ~0.1 ~

# Block particles from the surface, about 2 blocks above the spawn.
execute positioned ~ ~ ~ run function #bs.block:get_type
data modify storage {ns}:temp _rise_particle.block set from storage bs:out block.type
function {ns}:v{version}/zombies/zombie_rise_particles with storage {ns}:temp _rise_particle

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/zombie_finish_rise
""")

	write_versioned_function("zombies/zombie_rise_particles", r"""
$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~1 ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]
""")

	write_versioned_function("zombies/zombie_finish_rise", f"""
data modify entity @s NoAI set value 0b
tag @s remove {ns}.zb_rising

# summon_zombie_at already joins the horde; a zombie that missed it would make escort traders flee it.
team join {ns}.horde @s

# Walk-to spawn: only once the rise is over, since the escort freezes the zombie.
execute if data entity @s data.walk_to run function {ns}:v{version}/zombies/escort/start_to_target
""")

	## Intercept zombie death before vanilla event 60 (poof particles).
	write_versioned_function("zombies/death_watch_tick", f"""
# From the marker passenger to its vehicle, once DeathTime starts.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if data entity @s {{DeathTime:1s}} run function {ns}:v{version}/zombies/on_zombie_dying

# Death groan keyed on Health, which is 0 the instant it dies: DeathTime is preset to -16, so the intercept above
# lands 17 ticks late. zb_dying fires it once; dogs are skipped, they die with their own wolf vocals.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if entity @s[tag={ns}.zombie_round,tag=!{ns}.zb_dog,tag=!{ns}.zb_dying] if data entity @s {{Health:0.0f}} run function {ns}:v{version}/zombies/vocals/death
""")

	## Intercept a dying zombie before DeathTime reaches 20.
	write_versioned_function("zombies/on_zombie_dying", f"""
execute unless entity @s[tag={ns}.zombie_round] run return 0

# Kill the death-watch marker while still mounted, so none are orphaned.
kill @n[type=minecraft:marker,tag={ns}.death_watch,distance=..1]

# Dogs never roll the drop table: a dog round only drops the Max Ammo of its last hound.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/powerups/check_drop

# Dogs: "was this the last one" needs an exact count.
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/dog_death

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

	## Spawns up to #zb_spawn_batch zombies, one per recursive call.
	write_versioned_function("zombies/spawn_batch_tick", f"""
execute if score #zb_to_spawn {ns}.data matches ..0 run return 0

# Dog rounds release one hound per timer tick, capped by how many are out.
execute if score #zb_dog_round {ns}.data matches 1 run return run function {ns}:v{version}/zombies/spawn_dog_capped

function {ns}:v{version}/zombies/spawn_zombie
scoreboard players remove #zb_to_spawn {ns}.data 1
scoreboard players remove #zb_spawn_batch_remaining {ns}.data 1

execute if score #zb_spawn_batch_remaining {ns}.data matches 1.. if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_batch_tick
""")

