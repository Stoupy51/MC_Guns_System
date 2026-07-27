""" The game tick, preload, start and stop hooks. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import TRADER_REACH_GUARD


# Functions
def write_escort_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Hook the escort loop into the zombies game tick (count-gated: zero cost with no escort)
	write_versioned_function("zombies/game_tick", f"""
# Escort system (escort.py): drag escorted zombies behind their pathfinding traders
execute if score #zb_escort_count {ns}.data matches 1.. as @e[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/zombie_tick

# Interaction safeguard (count-INDEPENDENT, every tick)
execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag=!{ns}.zb_escort_monkey] at @s if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{TRADER_REACH_GUARD}] run function {ns}:v{version}/zombies/escort/end_at_trader

# Every 2s: resync the escort counter from reality
scoreboard players operation #zb_esc_sweep {ns}.data = #total_tick {ns}.data
scoreboard players operation #zb_esc_sweep {ns}.data %= #40 {ns}.data
execute if score #zb_esc_sweep {ns}.data matches 0 store result score #zb_escort_count {ns}.data if entity @e[tag={ns}.zb_escorted]
execute if score #zb_esc_sweep {ns}.data matches 0 as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort] at @s unless entity @e[tag={ns}.zb_escorted,distance=..8] run function {ns}:v{version}/zombies/escort/discard_trader

# PaP-room lure: recompute lure state every 2s (inert unless the map defined a lure centre)
execute if score #zb_esc_sweep {ns}.data matches 20 if score #zb_pap_has {ns}.data matches 1 run function {ns}:v{version}/zombies/escort/update_lure
""")

	# Place the map's lure center at preload, once base coords are loaded
	write_versioned_function("zombies/preload_complete", f"""
# PaP-room lure setup (escort.py)
function {ns}:v{version}/zombies/escort/setup_lure_center
""")

	write_versioned_function("zombies/start", f"""
# Escort system (escort.py)
scoreboard players set #zb_escort_count {ns}.data 0
scoreboard players set #zb_escort_mode {ns}.data 0
scoreboard players set #zb_lure {ns}.data 0
gamerule spawn_wandering_traders false
gamerule spawn_mobs false
""")

	# Traders themselves are killed with the gm_entity sweep in game.py's stop
	write_versioned_function("zombies/stop", f"""
# Escort cleanup (escort.py); the traders themselves die with the {ns}.gm_entity kill above
scoreboard players set #zb_escort_count {ns}.data 0
""")

