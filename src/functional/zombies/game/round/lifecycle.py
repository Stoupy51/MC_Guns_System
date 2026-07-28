""" The rise animation, the death intercept and the spawn batch tick. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_lifecycle() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Rise Animation.

	## Per-tick rise: called from game_tick for all zb_rising entities
	write_versioned_function("zombies/zombie_rise_tick", f"""
# Rise 0.1 blocks per tick
tp @s ~ ~0.1 ~

# Emit block-breaking particles from the block at the surface (2 blocks above spawn = ~0 now that we're rising)
# Read the block type at +2 above original spawn (approximately ground level)
execute positioned ~ ~ ~ run function #bs.block:get_type
data modify storage {ns}:temp _rise_particle.block set from storage bs:out block.type
function {ns}:v{version}/zombies/zombie_rise_particles with storage {ns}:temp _rise_particle

# Count down rise timer
scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/zombie_finish_rise
""")

	## Macro: emit block-textured particles at current position
	write_versioned_function("zombies/zombie_rise_particles", r"""
$execute align xyz run particle block{block_state:"$(block)"} ~.5 ~1 ~.5 0.3 0.1 0.3 0.5 15 force @a[distance=..64]
""")

	## Finish rise: activate AI and remove rising state
	write_versioned_function("zombies/zombie_finish_rise", f"""
data modify entity @s NoAI set value 0b
tag @s remove {ns}.zb_rising

# Walk-to spawn: hand it to an escort taxi that walks it to the map maker's spot. Only now that the
# rise is over — the escort freezes the zombie, which would strand it mid-animation.
execute if data entity @s data.walk_to run function {ns}:v{version}/zombies/escort/start_to_target
""")

	## Per-tick death watch: intercept zombie death before vanilla event 60 (poof particles)
	write_versioned_function("zombies/death_watch_tick", f"""
# Move execution from marker passenger -> vehicle (zombie), then intercept once DeathTime starts.
execute as @e[type=minecraft:marker,tag={ns}.death_watch] at @s on vehicle if data entity @s {{DeathTime:1s}} run function {ns}:v{version}/zombies/on_zombie_dying
""")

	## Intercept a dying zombie before DeathTime reaches 20
	write_versioned_function("zombies/on_zombie_dying", f"""
# Guard: only process round zombies.
execute unless entity @s[tag={ns}.zombie_round] run return 0

# Kill the attached death-watch marker while still mounted to avoid orphan buildup.
kill @n[type=minecraft:marker,tag={ns}.death_watch,distance=..1]

# Check if a power-up should drop at this zombie's position. Dogs never roll the random table — a
# dog round's only drop is the guaranteed Max Ammo from the last hound.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/powerups/check_drop

# Dogs: handle the death separately, since "was this the last one" needs an exact count.
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/dog_death

# Remove zombie before vanilla death event 60 can fire.
tp @s ~ -10000 ~
""")

	## Spawn tick: spawn zombies on a timer
	write_versioned_function("zombies/spawn_tick", f"""
# Decrease spawn timer
scoreboard players remove #zb_spawn_timer {ns}.data 1
execute if score #zb_spawn_timer {ns}.data matches 1.. run return 0

# Timer fired: recalculate timer and batch size for next cycle
function {ns}:v{version}/zombies/calc_spawn_timer

# Spawn a batch of zombies (batch size depends on round)
scoreboard players operation #zb_spawn_batch_remaining {ns}.data = #zb_spawn_batch {ns}.data
function {ns}:v{version}/zombies/spawn_batch_tick
""")

	## Spawn batch tick: spawn up to #zb_spawn_batch zombies, one per call (recursive)
	write_versioned_function("zombies/spawn_batch_tick", f"""
# Guard: nothing left to spawn
execute if score #zb_to_spawn {ns}.data matches ..0 run return 0

# Dog rounds spawn one hound per timer tick, capped by how many are already out
execute if score #zb_dog_round {ns}.data matches 1 run return run function {ns}:v{version}/zombies/spawn_dog_capped

# Spawn one zombie
function {ns}:v{version}/zombies/spawn_zombie
scoreboard players remove #zb_to_spawn {ns}.data 1
scoreboard players remove #zb_spawn_batch_remaining {ns}.data 1

# Recurse if batch not exhausted and zombies remain
execute if score #zb_spawn_batch_remaining {ns}.data matches 1.. if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_batch_tick
""")

