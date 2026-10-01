""" Black Ops style stamina, shared by the three modes.

The hunger bar is the visible meter: 20 full, 6 empty (vanilla already blocks sprinting at foodLevel <= 6, so the bar is also the sprint gate).
A score stays the source of truth for timing, and each tick the bar is nudged toward the mapped target with saturation and hunger pulses.
The draining bar is the only feedback.

The saturation effect restores +1 food but also +2 invisible saturation per tick, which would absorb hunger pulses and freeze the bar.
Refill pulses are therefore only given below target, and leftovers are burned off with hunger pulses at target.

Stamin-Up (zombies perk) adds +STAM_MAX on stam_bonus; its +7% movement speed is an attribute modifier set by the perk.
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

# Constants
STAM_MAX: int = 300
""" Base full stamina; perks add stam_bonus on top. """
STAM_DRAIN: int = 2
""" Per tick while sprinting -> 7.5s, or 15s with Stamin-Up. """
STAM_REGEN: int = 3
""" Per tick while resting -> 5s to refill. Scaled with STAM_MAX so the refill time stays 5s: the pool
grew, the sprint got longer, topping it back up did not get slower. """
SWIM_DRAIN_FACTOR: int = 5
""" Swimming drains this many times slower than sprinting on land, so crossing water is affordable.
The drain applies on one tick in SWIM_DRAIN_FACTOR: STAM_DRAIN is only 2, so dividing it would floor to 0.
"""
REST_DELAY: int = 20
""" Ticks after the last sprint before regen starts. """
RECOVER_AT: int = 120
""" Winded players sprint again at this level (hysteresis). Kept at 40% of STAM_MAX, which at STAM_REGEN
is the same 2s of resting as before the pool was widened. All values are ticks or stamina points, and stamina runs 0..stam_max. """

FOOD_MIN: int = 6
""" Vanilla no-sprint threshold = empty stamina. """
FOOD_MAX: int = 20
FOOD_SPAN: int = FOOD_MAX - FOOD_MIN
""" Hunger-bar mapping: target foodLevel = FOOD_MIN + FOOD_SPAN * stam / stam_max. """

# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# Black Ops style stamina, per player.
scoreboard objectives add {ns}.stam dummy
scoreboard objectives add {ns}.stam_max dummy
scoreboard objectives add {ns}.stam_bonus dummy
scoreboard objectives add {ns}.stam_rest dummy
scoreboard objectives add {ns}.stam_out dummy
scoreboard objectives add {ns}.stam_seen dummy

# Counts swim ticks, so the drain applies once per SWIM_DRAIN_FACTOR ticks (see stamina_swim_drain).
scoreboard objectives add {ns}.stam_swim dummy

# Set while refill pulses may have left invisible saturation; only then does the at-target branch read foodSaturationLevel to burn it off.
scoreboard objectives add {ns}.stam_dirty dummy
""")

	# player/tick runs as each player, at them. One in_game flag at a time, so at most one branch fires; spectators are downed or dead.
	gate: str = f"execute if score #any_game_active {ns}.data matches 1 unless entity @s[gamemode=spectator]"
	write_versioned_function("player/tick", f"""
# Drain while sprinting, block sprinting when winded, regen at rest.
{gate} if score @s {ns}.mp.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
{gate} if score @s {ns}.mi.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
{gate} if score @s {ns}.zb.in_game matches 1 run function {ns}:v{version}/player/stamina_tick
""")

	# Run as an in-game, non-spectating player, at them.
	write_versioned_function("player/stamina_tick", f"""
# Full stamina on the first tick of a game, a late join, a respawn or a revive: stam_seen is reset to 0 on each.
execute if score @s {ns}.stam_seen matches 0 run function {ns}:v{version}/player/stamina_init

# Base + perk bonus (Stamin-Up doubles it); the current value is clamped to it.
scoreboard players set @s {ns}.stam_max {STAM_MAX}
scoreboard players operation @s {ns}.stam_max += @s {ns}.stam_bonus
scoreboard players operation @s {ns}.stam < @s {ns}.stam_max

# The is_sprinting flag, unlike the sprint_one_cm stat (ground only), stays set through a jump, so jump-sprinting drains the same.
scoreboard players set #stam_sprinting {ns}.data 0
execute if predicate {ns}:v{version}/is_sprinting run scoreboard players set #stam_sprinting {ns}.data 1

# Swimming costs 1/{SWIM_DRAIN_FACTOR} of the sprint rate: the swim pose needs sprint held, and a full rate emptied the bar before any water was crossed.
scoreboard players set #stam_swimming {ns}.data 0
execute if predicate {ns}:v{version}/is_swimming run scoreboard players set #stam_swimming {ns}.data 1

# Sprinting drains and re-arms the delay before regen.
execute if score #stam_sprinting {ns}.data matches 1 if score #stam_swimming {ns}.data matches 0 run scoreboard players remove @s {ns}.stam {STAM_DRAIN}
execute if score #stam_sprinting {ns}.data matches 1 if score #stam_swimming {ns}.data matches 1 run function {ns}:v{version}/player/stamina_swim_drain
execute if score #stam_sprinting {ns}.data matches 1 run scoreboard players set @s {ns}.stam_rest {REST_DELAY}

# At rest, the delay counts down, then stamina regenerates.
execute if score #stam_sprinting {ns}.data matches 0 if score @s {ns}.stam_rest matches 1.. run scoreboard players remove @s {ns}.stam_rest 1
execute if score #stam_sprinting {ns}.data matches 0 if score @s {ns}.stam_rest matches 0 run scoreboard players add @s {ns}.stam {STAM_REGEN}

execute if score @s {ns}.stam matches ..-1 run scoreboard players set @s {ns}.stam 0
scoreboard players operation @s {ns}.stam < @s {ns}.stam_max

# Winded at 0, recovered silently past the hysteresis threshold: the empty bar is the only feedback.
execute if score @s {ns}.stam_out matches 0 if score @s {ns}.stam matches 0 run scoreboard players set @s {ns}.stam_out 1
execute if score @s {ns}.stam_out matches 1 if score @s {ns}.stam matches {RECOVER_AT}.. run scoreboard players set @s {ns}.stam_out 0

# Stamina to the hunger bar target ({FOOD_MIN}..{FOOD_MAX}); winded holds it at the no-sprint level.
scoreboard players operation #stam_t {ns}.data = @s {ns}.stam
scoreboard players operation #stam_t {ns}.data *= #{FOOD_SPAN} {ns}.data
scoreboard players operation #stam_t {ns}.data /= @s {ns}.stam_max
scoreboard players add #stam_t {ns}.data {FOOD_MIN}
execute if score @s {ns}.stam_out matches 1 run scoreboard players set #stam_t {ns}.data {FOOD_MIN}

function {ns}:v{version}/player/stamina_bar
""")

	# Pays STAM_DRAIN once the counter wraps (1/SWIM_DRAIN_FACTOR of sprint). The counter is not reset on leaving water,
	# so alternating swim and land strokes cannot dodge the drain.
	write_versioned_function("player/stamina_swim_drain", f"""
scoreboard players add @s {ns}.stam_swim 1
execute if score @s {ns}.stam_swim matches {SWIM_DRAIN_FACTOR}.. run scoreboard players set @s {ns}.stam_swim 0
execute if score @s {ns}.stam_swim matches 0 run scoreboard players remove @s {ns}.stam {STAM_DRAIN}
""")

	write_versioned_function("player/stamina_init", f"""
scoreboard players set @s {ns}.stam_max {STAM_MAX}
scoreboard players operation @s {ns}.stam_max += @s {ns}.stam_bonus
scoreboard players operation @s {ns}.stam = @s {ns}.stam_max
scoreboard players set @s {ns}.stam_out 0
scoreboard players set @s {ns}.stam_rest 0
scoreboard players set @s {ns}.stam_swim 0
scoreboard players set @s {ns}.stam_seen 1

# Assume leftover saturation from before the game (the stop refill), so the first at-target ticks burn it off.
scoreboard players set @s {ns}.stam_dirty 1
""")

	# Drives the bar toward #stam_t with 1-tick pulses; clearing both effects first removes last tick's pulses, so this owns the bar.
	write_versioned_function("player/stamina_bar", f"""
effect clear @s minecraft:saturation
effect clear @s minecraft:hunger

# Read from the auto-updated `food` criterion, no NBT read. Below target: +1 food this tick, never at or above, so the invisible
# saturation (+2 per tick) cannot stack past what is shown; the pulse may leave some, hence the flag.
execute if score @s {ns}.food < #stam_t {ns}.data run scoreboard players set @s {ns}.stam_dirty 1
execute if score @s {ns}.food < #stam_t {ns}.data run return run effect give @s minecraft:saturation 1 0 true

# Above target: a hunger pulse drains the bar slowly.
execute if score @s {ns}.food > #stam_t {ns}.data run return run effect give @s minecraft:hunger 1 255 true

# At target and flagged: read saturation and burn leftovers off with hunger pulses, so the next drain shows at once; once 0 the flag clears and the steady state reads no NBT.
execute unless score @s {ns}.stam_dirty matches 1 run return 0
execute store result score #stam_sat {ns}.data run data get entity @s foodSaturationLevel
execute if score #stam_sat {ns}.data matches 1.. run return run effect give @s minecraft:hunger 1 255 true
scoreboard players set @s {ns}.stam_dirty 0
""")

