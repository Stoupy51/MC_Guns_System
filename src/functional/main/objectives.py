""" Scoreboard objectives, the global tick loop and the custom health-regeneration system. """
# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_versioned_function

from ...config.stats.keys import REMAINING_BULLETS
from ..helpers.scores import SpecialScores


# Functions
def write_objectives() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Write to load file
	write_load_file(f"""
## Define objectives
# Used to tag players that should be selected by Multiplayer/Mission/Zombies functions (@a)
# We use a scoreboard instead of tag so we can reset offline players
scoreboard objectives add {ns}.player dummy

# Tracks the currently selected weapon ID for each player
scoreboard objectives add {ns}.previous_selected dummy

# Tracks right clicks to enable continuous right-click detection
scoreboard objectives add {ns}.pending_clicks dummy

# Tracks if the player is holding right-click (vs single tap)
scoreboard objectives add {ns}.held_click dummy

# Tracks current burst fire count (resets after BURST shots)
scoreboard objectives add {ns}.burst_count dummy

# Tracks weapon drops to enable fire mode switching
scoreboard objectives add {ns}.dropped minecraft.custom:minecraft.drop

# Cooldown in ticks before being able to shot
scoreboard objectives add {ns}.cooldown dummy

# Tracks weapon-switch-only cooldown (not set when shooting) for zoom shader guard
scoreboard objectives add {ns}.switch_cooldown dummy

# Indicates if the player was zooming (used to remove slowness)
scoreboard objectives add {ns}.zoom dummy

# Tracks continuous zoom duration for delayed scope effect (10-tick delay)
scoreboard objectives add {ns}.zoom_timer dummy

# Tracks the most recently selected weapon ID for weapon switching mechanics
scoreboard objectives add {ns}.last_selected dummy

# Tracks the current amount of bullets in the selected weapon
scoreboard objectives add {ns}.{REMAINING_BULLETS} dummy

# Tracks the total reserve ammo (sum of all magazine bullets in inventory)
# Updated on reload and when player is idle (not shooting for ~60 ticks)
scoreboard objectives add {ns}.reserve_ammo dummy

# Tracks the room acoustics level for crack sound effects
scoreboard objectives add {ns}.acoustics_level dummy

# Tracks how much time has passed since the player last saw a muzzle flash
scoreboard objectives add {ns}.last_muzzle_flash dummy

## Global configuration scoreboards (admin/server-level)
# RPG explosion power (0 = no block destruction, higher = more destruction)
scoreboard objectives add {ns}.config dummy

## Per-player special scoreboards (for zombies bonuses, testing, etc.)
## Generated from SpecialScores.ALL, which is also what game starts wipe to get a clean slate.
{SpecialScores.special_objectives_lines(ns)}
# DPS tracking: accumulates damage dealt per second, snapshot stored for actionbar
scoreboard objectives add {ns}.dps dummy
scoreboard objectives add {ns}.previous_dps dummy
scoreboard objectives add {ns}.dps_timer dummy

# Forces an immediate actionbar refresh (set by events its idle gate can't detect, e.g. fire-mode toggle)
scoreboard objectives add {ns}.ab_force dummy

# Initialize slow bullet (projectile) counter
scoreboard players add #slow_bullet_count {ns}.data 0

# Semtex entity pairing: unique ID objective + global counter
scoreboard objectives add {ns}.grenade_launch dummy
scoreboard objectives add {ns}.stuck_id dummy

# Per-grenade accumulated tumble angle (1e-4 rad units)
scoreboard objectives add {ns}.grenade_spin dummy
scoreboard players set #semtex_id {ns}.data 0

# Initialize global config defaults (only if not already set)
execute unless score #projectile_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #projectile_explosion_power {ns}.config 0
execute unless score #grenade_explosion_power {ns}.config matches -2147483648.. run scoreboard players set #grenade_explosion_power {ns}.config 0
execute unless score #max_ammo_reload_weapons {ns}.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons {ns}.config 0
execute unless score #damage_debug {ns}.config matches -2147483648.. run scoreboard players set #damage_debug {ns}.config 0

# Health regeneration tracking (global, shared across all game modes)
scoreboard objectives add {ns}.last_hit dummy
scoreboard objectives add {ns}.hp_prev dummy

# Read-only criteria objectives, auto-updated by the server every tick a value changes.
# Reading these replaces per-tick `data get entity @s Health/foodLevel` (full player-NBT
# serialization) with a plain score read. NOTE: {ns}.health = ceil(health + absorption);
# this pack has no absorption sources, so it tracks health exactly.
scoreboard objectives add {ns}.health health
scoreboard objectives add {ns}.food food

# Real-time clock: global stopwatch queried every tick (lag-immune wall-clock time).
# Recreated on every load — only per-tick deltas are consumed, so the reset is harmless.
stopwatch remove {ns}:clock
stopwatch create {ns}:clock
scoreboard players set #real_prev {ns}.data 0
""", prepend=True)

	# Write to tick file
	write_tick_file(f"""
# Infinitely incrementing tick counter for general timing purposes
scoreboard players add #total_tick {ns}.data 1

# Real-time tick equivalents from the {ns}:clock stopwatch (scale 20 = seconds x20).
# #tick_delta = real ticks elapsed since the previous game tick: ~1 at 20 TPS, 2+ under lag.
# Mode timers subtract #tick_delta instead of 1 so durations stay wall-clock accurate.
# No lower clamp to 1: ms rounding jitters deltas between 0/1/2 but their SUM stays exact.
# Upper clamp 40 (2s) bounds the jump after a singleplayer pause or a world freeze.
execute store result score #real_tick {ns}.data run stopwatch query {ns}:clock 20
scoreboard players operation #tick_delta {ns}.data = #real_tick {ns}.data
scoreboard players operation #tick_delta {ns}.data -= #real_prev {ns}.data
scoreboard players operation #real_prev {ns}.data = #real_tick {ns}.data
execute unless score #tick_delta {ns}.data matches 0.. run scoreboard players set #tick_delta {ns}.data 0
execute if score #tick_delta {ns}.data matches 41.. run scoreboard players set #tick_delta {ns}.data 40

# Player loop
execute as @e[type=player,sort=random] at @s run function {ns}:v{version}/player/tick
""")

	# Health regeneration tick hook (global — only runs during an active game)
	write_versioned_function("player/tick", f"""
# Health regeneration: Black Ops style — only active during a game
execute if score #any_game_active {ns}.data matches 1 run function {ns}:v{version}/player/regen_tick
""")

	write_versioned_function("player/regen_tick", f"""
# @s = any player during an active game
# Damage detection via the auto-updated 'health' criterion (no player-NBT read)
execute if score @s {ns}.health < @s {ns}.hp_prev run scoreboard players set @s {ns}.last_hit 0
execute unless score @s {ns}.health < @s {ns}.hp_prev run scoreboard players add @s {ns}.last_hit 1
scoreboard players operation @s {ns}.hp_prev = @s {ns}.health
execute unless score @s {ns}.last_hit matches 100.. run return 0

# At full health there is nothing to refresh; a still-running 3s pulse finishes any half-heart
# (regeneration can't overheal, so letting it expire replaces the old per-tick `effect clear`)
execute store result score #hp_max {ns}.data run attribute @s minecraft:max_health get 1
execute if score @s {ns}.health >= #hp_max {ns}.data run return 0
effect give @s minecraft:regeneration 3 2 true
""")

