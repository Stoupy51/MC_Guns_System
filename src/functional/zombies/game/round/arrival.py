""" How a spawn's enemy comes in: rising through the floor, dropping from the ceiling, struck in by a portal, or at once. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_arrivals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Each runs as the spawn marker, at it, with the enemy's compound in {ns}:temp _mob.

	## 2 blocks up through the floor over the spawn's rise duration, from 1.8 below it.
	write_versioned_function("zombies/arrival/floor", f"""
scoreboard players set #zb_rise_step {ns}.data 2000
scoreboard players operation #zb_rise_step {ns}.data /= @s {ns}.zb.rise_tick
data modify storage {ns}:temp _mob.no_ai set value 1b
execute positioned ~ ~-1.8 ~ run function {ns}:v{version}/zombies/mob/spawn
function {ns}:v{version}/zombies/arrival/rise
function {ns}:v{version}/zombies/summon_rise_dust {{block_y:"-1"}}
""")

	## 2 blocks down from the ceiling, through the block 2 above the spawn.
	write_versioned_function("zombies/arrival/ceiling", f"""
scoreboard players set #zb_rise_step {ns}.data -2000
scoreboard players operation #zb_rise_step {ns}.data /= @s {ns}.zb.rise_tick
data modify storage {ns}:temp _mob.no_ai set value 1b
execute positioned ~ ~2.2 ~ run function {ns}:v{version}/zombies/mob/spawn
function {ns}:v{version}/zombies/arrival/rise
execute positioned ~ ~2 ~ run function {ns}:v{version}/zombies/summon_rise_dust {{block_y:"0"}}
""")

	## The root moves; its riders ride along. zombie_finish_rise wakes it and starts the walk-to escort.
	write_versioned_function("zombies/arrival/rise", f"""
tag @n[tag={ns}.zb_new_root] add {ns}.zb_rising
scoreboard players operation @n[tag={ns}.zb_new_root] {ns}.zb.rise_tick = @s {ns}.zb.rise_tick
scoreboard players operation @n[tag={ns}.zb_new_root] {ns}.zb.rise_step = #zb_rise_step {ns}.data
execute if data entity @s data.walk_to run data modify entity @n[tag={ns}.zb_new_root] data.walk_to set from entity @s data.walk_to
tag @n[tag={ns}.zb_new_root] remove {ns}.zb_new_root
""")

	write_versioned_function("zombies/arrival/instant", f"""
data modify storage {ns}:temp _mob.no_ai set value 0b
function {ns}:v{version}/zombies/mob/spawn
function {ns}:v{version}/zombies/arrival/land
""")

	## Run as the spawn or the portal marker: an enemy that came in awake walks to the spawn's spot right away.
	write_versioned_function("zombies/arrival/land", f"""
execute if data entity @s data.walk_to run data modify entity @n[tag={ns}.zb_new_root] data.walk_to set from entity @s data.walk_to
execute if data entity @s data.walk_to as @n[tag={ns}.zb_new_root] at @s run function {ns}:v{version}/zombies/escort/start_to_target
tag @n[tag={ns}.zb_new_root] remove {ns}.zb_new_root
""")

	## Run as the spawn marker, on the surface the enemy breaks through, which sheds debris for the whole rise.
	write_versioned_function("zombies/summon_rise_dust", f"""
$execute positioned ~ ~$(block_y) ~ run function #bs.block:get_type
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.zb_rise_dust","{ns}.zombies_entity","{ns}.zb_rise_dust_new"],CustomName:"Rise Dust"}}
data modify entity @n[tag={ns}.zb_rise_dust_new] data.block set from storage bs:out block.type
scoreboard players operation @n[tag={ns}.zb_rise_dust_new] {ns}.zb.rise_tick = @s {ns}.zb.rise_tick
tag @n[tag={ns}.zb_rise_dust_new] remove {ns}.zb_rise_dust_new
""")

	## The spot sparks for 1.5 s, then a bolt delivers the enemy (BO2 hellhounds). The portal keeps the compound until then.
	write_versioned_function("zombies/arrival/portal", f"""
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.zb_portal","{ns}.zombies_entity","{ns}.zb_portal_new"],CustomName:"Spawn Portal"}}
data modify entity @n[tag={ns}.zb_portal_new] data.mob set from storage {ns}:temp _mob
execute if data entity @s data.walk_to run data modify entity @n[tag={ns}.zb_portal_new] data.walk_to set from entity @s data.walk_to
scoreboard players set @n[tag={ns}.zb_portal_new] {ns}.zb.rise_tick 30
scoreboard players operation @n[tag={ns}.zb_portal_new] {ns}.zb.spawn.sid = @s {ns}.zb.spawn.sid
tag @n[tag={ns}.zb_portal_new] remove {ns}.zb_portal_new

# An enemy still in its portal is not an entity, so count it or the round ends early (see game_tick).
scoreboard players add #zb_portal_pending {ns}.data 1

# Volume 2.0 reaches the 32-block selector; minVolume lets players further out hear it.
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25
""")

	## Telegraph in 3 escalating phases so the strike point reads from across the map.
	write_versioned_function("zombies/portal_tick", f"""
# Phase 1 (30 ticks): a ring on the floor marks the footprint.
particle minecraft:electric_spark ~ ~0.1 ~ 1.1 0.02 1.1 0.0 5 force @a[distance=..48]

# Phase 2 (last 20): the charge climbs out of the floor.
execute if score @s {ns}.zb.rise_tick matches ..20 run particle minecraft:electric_spark ~ ~0.7 ~ 0.35 0.9 0.35 0.03 8 force @a[distance=..48]

# Phase 3 (last 10): a column forms and the ring tightens.
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:end_rod ~ ~1.2 ~ 0.12 1.3 0.12 0.01 5 force @a[distance=..48]
execute if score @s {ns}.zb.rise_tick matches ..10 run particle minecraft:crit ~ ~0.2 ~ 0.45 0.08 0.45 0.06 8 force @a[distance=..32]

# Crackle every 5 ticks, with the same volume rule as the strike.
scoreboard players operation #zb_portal_mod {ns}.data = @s {ns}.zb.rise_tick
scoreboard players operation #zb_portal_mod {ns}.data %= #5 {ns}.data
execute if score #zb_portal_mod {ns}.data matches 0 run playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..32] ~ ~ ~ 2.0 0.6 0.3

scoreboard players remove @s {ns}.zb.rise_tick 1
execute if score @s {ns}.zb.rise_tick matches ..0 run function {ns}:v{version}/zombies/portal_strike
""")

	## The strike. Not a lightning_bolt entity, which would ignite the map, shock players and carry its thunder dimension-wide.
	write_versioned_function("zombies/portal_strike", f"""
# A wide Y spread with near-zero XZ spread and speed 0 draws a vertical shaft.
particle minecraft:electric_spark ~ ~4 ~ 0.06 4.0 0.06 0.0 160 force @a[distance=..64]
particle minecraft:end_rod ~ ~4 ~ 0.04 4.0 0.04 0.0 40 force @a[distance=..64]

# flash takes a mandatory ARGB color.
particle minecraft:flash{{color:[1.0f,0.82f,0.90f,1.0f]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..64]

particle minecraft:electric_spark ~ ~0.15 ~ 1.6 0.02 1.6 0.5 90 force @a[distance=..48]
particle minecraft:crit ~ ~0.15 ~ 1.2 0.02 1.2 0.3 30 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.impact ambient @a[distance=..48] ~ ~ ~ 3.0 1.2 0.5
playsound minecraft:entity.lightning_bolt.thunder ambient @a[distance=..64] ~ ~ ~ 4.0 1.5 0.4

# Delivered at ground level and awake, so no rise.
data modify storage {ns}:temp _mob set from entity @s data.mob
data modify storage {ns}:temp _mob.no_ai set value 0b
scoreboard players operation #zb_spawn_sid {ns}.data = @s {ns}.zb.spawn.sid
execute store result score #zb_spawn_x {ns}.data run data get entity @s Pos[0]
execute store result score #zb_spawn_z {ns}.data run data get entity @s Pos[2]
execute positioned ~ ~0.2 ~ run function {ns}:v{version}/zombies/mob/spawn
function {ns}:v{version}/zombies/arrival/land

scoreboard players remove #zb_portal_pending {ns}.data 1
kill @s
""")

