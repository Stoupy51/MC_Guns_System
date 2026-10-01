""" The per-tick escort: dragging the zombie behind its trader and the stuck watchdog. """
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

	# Escorted zombies are glued to their trader, so the nearest trader is theirs.
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	my_trader_monkey: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_monkey,distance=..8]"
	my_trader_walk: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_walk,distance=..8]"

	# Run as the escorted zombie, at the trader's position from last tick.
	write_versioned_function("zombies/escort/zombie_tick", f"""
# Trader killed externally: unfreeze, normal stuck detection takes over.
execute unless entity {my_trader} run return run function {ns}:v{version}/zombies/escort/detach

# Same position and rotation as the trader: always path-valid, and pushOtherTeams stops the overlap from pushing it.
execute at {my_trader} run tp @s ~ ~ ~ ~ ~

# Monkey-bomb lure: once every monkey is gone the escort reverts to a player escort;
# otherwise ride to the monkey and ignore the player releases below.
execute if entity {my_trader_monkey} unless entity @e[tag={ns}.monkey_bomb] run tag {my_trader} remove {ns}.zb_escort_monkey
execute if entity {my_trader_monkey} run return run function {ns}:v{version}/zombies/escort/monkey_ride

# Walk-to spawn: skip the player releases, which would fire at once (spawns are within 32 blocks of a player)
# and drop the zombie back at its spawn.
execute if entity {my_trader_walk} run return run function {ns}:v{version}/zombies/escort/walk_ride

# PaP-room lure: release at the theatre centre, where no player is near to trigger the releases below.
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..{LURE_RELEASE}] run return run function {ns}:v{version}/zombies/escort/release

# Point-blank: release without line of sight, which corner and slab geometry can fail forever.
execute if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS_CLOSE}] run return run function {ns}:v{version}/zombies/escort/release

# Release once a player is close and visible: a player above a floor is close but unreachable.
scoreboard players set #zb_esc_see {ns}.data 0
execute positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS}] store result score #zb_esc_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_esc_see {ns}.data matches 1 run return run function {ns}:v{version}/zombies/escort/release

# Shared with the monkey ride.
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# TTL countdown, then the once-a-second retarget and watchdog.
	write_versioned_function("zombies/escort/escort_tail", f"""
# TTL out: the trader could not reach the target, fall back to the teleport rescue.
scoreboard players remove @s {ns}.zb.escort_ttl 1
execute if score @s {ns}.zb.escort_ttl matches ..0 run return run function {ns}:v{version}/zombies/escort/give_up

# Every second (retarget picks player, PaP lure or monkey).
scoreboard players operation #zb_esc_mod {ns}.data = @s {ns}.zb.escort_ttl
scoreboard players operation #zb_esc_mod {ns}.data %= #20 {ns}.data
execute if score #zb_esc_mod {ns}.data matches 0 as {my_trader} at @s run function {ns}:v{version}/zombies/escort/retarget

# Catches a trader that cannot move in {WATCHDOG_GIVE_UP} s instead of {ESCORT_TTL // 20} s.
execute if score #zb_esc_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/escort/watchdog
""")

	# Release at the target spot. A barricade on the way ends the escort earlier (barricades/freeze_zombies);
	# without this, a zombie at a target with no barricade would idle until the watchdog gave up.
	write_versioned_function("zombies/escort/walk_ride", f"""
scoreboard players set #zb_esc_arrived {ns}.data 0
function {ns}:v{version}/zombies/escort/check_walk_arrived with entity @s data.walk_to
execute if score #zb_esc_arrived {ns}.data matches 1 run return run function {ns}:v{version}/zombies/escort/release

function {ns}:v{version}/zombies/escort/escort_tail
""")

	# Run as the travelling zombie, with its data.walk_to.
	write_versioned_function("zombies/escort/check_walk_arrived", f"""
$execute positioned $(x) $(y) $(z) if entity @s[distance=..{WALK_ARRIVAL}] run scoreboard players set #zb_esc_arrived {ns}.data 1
""")

	# Hold on arrival: the monkey has no aggro of its own.
	write_versioned_function("zombies/escort/monkey_ride", f"""
execute if entity @e[tag={ns}.monkey_bomb,distance=..{MONKEY_RELEASE}] run return run function {ns}:v{version}/zombies/escort/monkey_hold
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# No escort_tail: standing still here is the goal.
	write_versioned_function("zombies/escort/monkey_hold", f"""
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}
scoreboard players set @s {ns}.zb.stuck_ticks 0
""")

	# While escorted, stuck_x and stuck_z hold last second's block.
	write_versioned_function("zombies/escort/watchdog", f"""
execute store result score #zb_esc_x {ns}.data run data get entity @s Pos[0]
execute store result score #zb_esc_z {ns}.data run data get entity @s Pos[2]
scoreboard players set #zb_esc_moved {ns}.data 0
execute unless score #zb_esc_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #zb_esc_moved {ns}.data 1
execute unless score #zb_esc_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #zb_esc_moved {ns}.data 1
scoreboard players operation @s {ns}.zb.stuck_x = #zb_esc_x {ns}.data
scoreboard players operation @s {ns}.zb.stuck_z = #zb_esc_z {ns}.data

execute if score #zb_esc_moved {ns}.data matches 1 run return run scoreboard players set @s {ns}.zb.stuck_ticks 0

# The trader is stuck too: teleport rescue.
scoreboard players add @s {ns}.zb.stuck_ticks 1
execute if score @s {ns}.zb.stuck_ticks matches {WATCHDOG_GIVE_UP}.. run function {ns}:v{version}/zombies/escort/give_up
""")

