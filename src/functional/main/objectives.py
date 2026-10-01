""" Scoreboard objectives, the global tick loop and the custom health-regeneration system. """
# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_versioned_function

from ...config.stats.keys import REMAINING_BULLETS
from ..helpers.scores import SpecialScores


# Functions
def write_objectives() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
## Length of the selected item id, to detect a change.
scoreboard objectives add {ns}.previous_selected dummy

# Continuous right-click detection.
scoreboard objectives add {ns}.pending_clicks dummy

# Held right click, as opposed to a single tap.
scoreboard objectives add {ns}.held_click dummy

# Shots fired in the current burst.
scoreboard objectives add {ns}.burst_count dummy

# The drop key switches fire mode.
scoreboard objectives add {ns}.dropped minecraft.custom:minecraft.drop

# Expiry tick before the next shot.
scoreboard objectives add {ns}.cooldown dummy

# Was zooming, so the slowness can be removed.
scoreboard objectives add {ns}.zoom dummy

# Last selected weapon id, for switch detection.
scoreboard objectives add {ns}.last_selected dummy

# Bullets in the selected weapon.
scoreboard objectives add {ns}.{REMAINING_BULLETS} dummy

# Sum of the magazine bullets in the inventory, updated on reload and after about 60 idle ticks.
scoreboard objectives add {ns}.reserve_ammo dummy

# Room acoustics, for the crack sounds.
scoreboard objectives add {ns}.acoustics_level dummy

# Ticks since the last muzzle flash this player saw.
scoreboard objectives add {ns}.last_muzzle_flash dummy

## Server config (#projectile_explosion_power, ...): 0 means no block destruction.
scoreboard objectives add {ns}.config dummy

## From SpecialScores.ALL, which game starts also wipe.
{SpecialScores.special_objectives_lines(ns)}
# Damage per second, accumulated then snapshotted for the actionbar.
scoreboard objectives add {ns}.dps dummy
scoreboard objectives add {ns}.previous_dps dummy
scoreboard objectives add {ns}.dps_timer dummy

# Forces an actionbar refresh for changes the idle gate cannot see (fire-mode toggle).
scoreboard objectives add {ns}.ab_force dummy

scoreboard players add #slow_bullet_count {ns}.data 0

# Semtex pairing: a unique id objective and a global counter.
scoreboard objectives add {ns}.grenade_launch dummy
scoreboard objectives add {ns}.stuck_id dummy

# Accumulated tumble angle (1e-4 rad units).
scoreboard objectives add {ns}.grenade_spin dummy
scoreboard players set #semtex_id {ns}.data 0

# Defaults, only when unset.
execute unless score #projectile_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #projectile_explosion_power {ns}.config 0
execute unless score #grenade_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #grenade_explosion_power {ns}.config 0
execute unless score #max_ammo_reload_weapons {ns}.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons {ns}.config 0
execute unless score #damage_debug {ns}.config matches -2147483648.. run scoreboard players set #damage_debug {ns}.config 0

# Health regeneration, shared by every mode.
scoreboard objectives add {ns}.last_hit dummy
scoreboard objectives add {ns}.hp_prev dummy

# Read-only criteria the server keeps current: a score read instead of serializing the player NBT for Health or foodLevel.
# {ns}.health = ceil(health + absorption), and the pack has no absorption source.
scoreboard objectives add {ns}.health health
scoreboard objectives add {ns}.food food

# Global stopwatch, a lag-immune wall clock. Recreated on every load, which is harmless: only per-tick deltas are used.
stopwatch remove {ns}:clock
stopwatch create {ns}:clock
scoreboard players set #real_prev {ns}.data 0
""", prepend=True)

	write_tick_file(f"""
scoreboard players add #total_tick {ns}.data 1

# #tick_delta = real ticks since the previous game tick (about 1 at 20 TPS, 2+ under lag); mode timers subtract it so durations stay wall-clock accurate.
# No lower clamp: ms rounding jitters deltas between 0, 1 and 2 but their sum stays exact. The upper clamp 40 (2 s) bounds the jump after a pause or freeze.
execute store result score #real_tick {ns}.data run stopwatch query {ns}:clock 20
scoreboard players operation #tick_delta {ns}.data = #real_tick {ns}.data
scoreboard players operation #tick_delta {ns}.data -= #real_prev {ns}.data
scoreboard players operation #real_prev {ns}.data = #real_tick {ns}.data
execute unless score #tick_delta {ns}.data matches 0.. run scoreboard players set #tick_delta {ns}.data 0
execute if score #tick_delta {ns}.data matches 41.. run scoreboard players set #tick_delta {ns}.data 40

execute as @e[type=player,sort=random] at @s run function {ns}:v{version}/player/tick
""")

	write_versioned_function("player/tick", f"""
# Black Ops style, only during a game.
execute if score #any_game_active {ns}.data matches 1 run function {ns}:v{version}/player/regen_tick
""")

	write_versioned_function("player/regen_tick", f"""
# Run as a player during a game; damage is read from the `health` criterion, no NBT.
execute if score @s {ns}.health < @s {ns}.hp_prev run scoreboard players set @s {ns}.last_hit 0
execute unless score @s {ns}.health < @s {ns}.hp_prev run scoreboard players add @s {ns}.last_hit 1
scoreboard players operation @s {ns}.hp_prev = @s {ns}.health
execute unless score @s {ns}.last_hit matches 100.. run return 0

# At full health, a running 3 s pulse finishes any half heart (regeneration cannot overheal).
execute store result score #hp_max {ns}.data run attribute @s minecraft:max_health get 1
execute if score @s {ns}.health >= #hp_max {ns}.data run return 0
effect give @s minecraft:regeneration 3 2 true
""")

