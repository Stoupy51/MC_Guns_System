""" The game tick, preload, start and stop hooks. """
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import TRADER_REACH_GUARD


# Functions
def write_escort_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Count-gated, so free when no escort runs.
	write_versioned_function("zombies/game_tick", f"""
execute if score #zb_escort_count {ns}.data matches 1.. as @e[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/zombie_tick

# Interaction safeguard, every tick. Monkey and walk-to escorts are exempt: map makers aim walks where the action is,
# so it would cancel them short of the target. Their eaten click is recovered in weapon/common.
execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag=!{ns}.zb_escort_monkey,tag=!{ns}.zb_escort_walk] at @s if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{TRADER_REACH_GUARD}] run function {ns}:v{version}/zombies/escort/end_at_trader

# Every 2 s the counter is resynced from the entities.
scoreboard players operation #zb_esc_sweep {ns}.data = #total_tick {ns}.data
scoreboard players operation #zb_esc_sweep {ns}.data %= #40 {ns}.data
execute if score #zb_esc_sweep {ns}.data matches 0 store result score #zb_escort_count {ns}.data if entity @e[tag={ns}.zb_escorted]
execute if score #zb_esc_sweep {ns}.data matches 0 as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort] at @s unless entity @e[tag={ns}.zb_escorted,distance=..8] run function {ns}:v{version}/zombies/escort/discard_trader

# Inert unless the map defined a lure centre.
execute if score #zb_esc_sweep {ns}.data matches 20 if score #zb_pap_has {ns}.data matches 1 run function {ns}:v{version}/zombies/escort/update_lure
""")

	# At preload, once the base coordinates are loaded.
	write_versioned_function("zombies/preload_complete", f"""
function {ns}:v{version}/zombies/escort/setup_lure_center
""")

	write_versioned_function("zombies/start", f"""
scoreboard players set #zb_escort_count {ns}.data 0
scoreboard players set #zb_escort_mode {ns}.data 0
scoreboard players set #zb_lure {ns}.data 0
gamerule spawn_wandering_traders false
gamerule spawn_mobs false
""")

	# The gm_entity sweep in stop kills the traders.
	write_versioned_function("zombies/stop", f"""
scoreboard players set #zb_escort_count {ns}.data 0
""")

