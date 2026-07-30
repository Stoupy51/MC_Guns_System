""" The per-tick escort: dragging the zombie behind its trader and the stuck watchdog. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import (
	ESCORT_TTL,
	LURE_RELEASE,
	MONKEY_RELEASE,
	RELEASE_RADIUS,
	RELEASE_RADIUS_CLOSE,
	WALK_ARRIVAL,
	WATCHDOG_GIVE_UP,
)


# Functions
def write_escort_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Escorted zombies are glued to their trader every tick, so "mine" is always the nearest one
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	my_trader_monkey: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_monkey,distance=..8]"
	my_trader_walk: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_walk,distance=..8]"

	# Per-tick escort logic (@s = escorted zombie, at @s = the trader's last-tick position)
	write_versioned_function("zombies/escort/zombie_tick", f"""
# Trader gone (killed externally)? Unfreeze; normal stuck detection takes over again
execute unless entity {my_trader} run return run function {ns}:v{version}/zombies/escort/detach

# Glue the zombie exactly onto the trader (same position AND rotation): always a path-valid
# spot, and the horde's pushOtherTeams collision rule keeps the overlap from pushing the trader
execute at {my_trader} run tp @s ~ ~ ~ ~ ~

# Monkey-bomb lure (monkey_bomb.py): while the trader is flagged, this escort pulls the zombie to
# a thrown monkey. Drop the flag once every monkey is gone (revert to a normal player escort);
# otherwise ride toward the monkey and release on arrival, ignoring the player releases below.
execute if entity {my_trader_monkey} unless entity @e[tag={ns}.monkey_bomb] run tag {my_trader} remove {ns}.zb_escort_monkey
execute if entity {my_trader_monkey} run return run function {ns}:v{version}/zombies/escort/monkey_ride

# Walk-to spawn: ride all the way to the target, skipping the player releases below. Those would
# fire on the first tick — spawns are picked within 32 blocks of a player — and drop the zombie
# right back where it spawned, which is exactly what the walk exists to avoid.
execute if entity {my_trader_walk} run return run function {ns}:v{version}/zombies/escort/walk_ride

# PaP-room lure active: release once the zombie reaches the theatre centre (no player will be
# nearby there to trigger the player-based releases below)
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..{LURE_RELEASE}] run return run function {ns}:v{version}/zombies/escort/release

# Point-blank → release NOW, no line-of-sight needed: the visibility check below aims at the
# player's feet and corner/slab geometry can fail it forever while the taxi orbits the player
execute if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS_CLOSE}] run return run function {ns}:v{version}/zombies/escort/release

# Hand off to vanilla AI once a player is close AND in the zombie's line of sight: a player
# 3 blocks above through a floor is "close" but the zombie still can't path there — keep riding
scoreboard players set #zb_esc_see {ns}.data 0
execute positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS}] store result score #zb_esc_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_esc_see {ns}.data matches 1 run return run function {ns}:v{version}/zombies/escort/release

# Ride tail: TTL fallback + periodic retarget/watchdog (shared with the monkey-bomb ride below)
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# Shared "keep riding" tail: TTL countdown plus the once-a-second retarget and watchdog
	write_versioned_function("zombies/escort/escort_tail", f"""
# TTL countdown; the trader could not reach its target in time -> teleport-rescue fallback
scoreboard players remove @s {ns}.zb.escort_ttl 1
execute if score @s {ns}.zb.escort_ttl matches ..0 run return run function {ns}:v{version}/zombies/escort/give_up

# Re-aim the trader at its target every second (retarget picks player / PaP lure / monkey)
scoreboard players operation #zb_esc_mod {ns}.data = @s {ns}.zb.escort_ttl
scoreboard players operation #zb_esc_mod {ns}.data %= #20 {ns}.data
execute if score #zb_esc_mod {ns}.data matches 0 as {my_trader} at @s run function {ns}:v{version}/zombies/escort/retarget

# Watchdog every second: a trader that can't move is caught in {WATCHDOG_GIVE_UP}s, not {ESCORT_TTL // 20}s
execute if score #zb_esc_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/escort/watchdog
""")

	# Walk ride: release once the zombie stands at the spot it was sent to, so vanilla AI takes it
	# from there. A barricade crossed on the way ends the escort earlier through barricades/freeze_zombies;
	# this is what covers a target with no barricade in front of it, which would otherwise leave the
	# zombie idling on arrival until the watchdog gave up on it.
	write_versioned_function("zombies/escort/walk_ride", f"""
scoreboard players set #zb_esc_arrived {ns}.data 0
function {ns}:v{version}/zombies/escort/check_walk_arrived with entity @s data.walk_to
execute if score #zb_esc_arrived {ns}.data matches 1 run return run function {ns}:v{version}/zombies/escort/release

function {ns}:v{version}/zombies/escort/escort_tail
""")

	# @s = the travelling zombie, args = its data.walk_to
	write_versioned_function("zombies/escort/check_walk_arrived", f"""
$execute positioned $(x) $(y) $(z) if entity @s[distance=..{WALK_ARRIVAL}] run scoreboard players set #zb_esc_arrived {ns}.data 1
""")

	# Monkey ride: HOLD on arrival rather than release, since the monkey has no aggro of its own
	write_versioned_function("zombies/escort/monkey_ride", f"""
execute if entity @e[tag={ns}.monkey_bomb,distance=..{MONKEY_RELEASE}] run return run function {ns}:v{version}/zombies/escort/monkey_hold
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# Gathered at the monkey: no escort_tail, since standing still here is the goal, not a fault
	write_versioned_function("zombies/escort/monkey_hold", f"""
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}
scoreboard players set @s {ns}.zb.stuck_ticks 0
""")

	# Early give-up for a stuck trader; while escorted, stuck_x/z hold last second's block snapshot
	write_versioned_function("zombies/escort/watchdog", f"""
execute store result score #zb_esc_x {ns}.data run data get entity @s Pos[0]
execute store result score #zb_esc_z {ns}.data run data get entity @s Pos[2]
scoreboard players set #zb_esc_moved {ns}.data 0
execute unless score #zb_esc_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #zb_esc_moved {ns}.data 1
execute unless score #zb_esc_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #zb_esc_moved {ns}.data 1
scoreboard players operation @s {ns}.zb.stuck_x = #zb_esc_x {ns}.data
scoreboard players operation @s {ns}.zb.stuck_z = #zb_esc_z {ns}.data

# Moved a block since last second: reset the still counter and keep escorting
execute if score #zb_esc_moved {ns}.data matches 1 run return run scoreboard players set @s {ns}.zb.stuck_ticks 0

# Still in the same block: the trader is stuck too -> teleport-rescue fallback
scoreboard players add @s {ns}.zb.stuck_ticks 1
execute if score @s {ns}.zb.stuck_ticks matches {WATCHDOG_GIVE_UP}.. run function {ns}:v{version}/zombies/escort/give_up
""")

