""" The game tick, the admin pause and routing a death into the downed state. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.titles import TitleTimes


# Functions
def write_zombies_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Game Tick.

	write_tick_file(f"""
# Zombies game tick. #zb_freeze (admin menu) swaps it for the freeze tick: skipping game_tick is what
# actually pauses the round — every zombies timer (spawns, bleed-out, power-ups, sales) lives inside it.
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1 run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"active"}} if score #zb_freeze {ns}.data matches 1 run function {ns}:v{version}/zombies/freeze_tick
execute if data storage {ns}:zombies game{{state:"preparing"}} run function {ns}:v{version}/zombies/prep_tick
""")

	write_versioned_function("zombies/game_tick", f"""
# Revive system tick (process downed players)
function {ns}:v{version}/zombies/revive/tick

# Call map-defined tick script
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

# Rise animation tick for spawning zombies
execute as @e[tag={ns}.zb_rising] at @s run function {ns}:v{version}/zombies/zombie_rise_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds_player

# Check round completion
execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
# Dogs still telegraphing aren't entities yet, so #zb_alive can't see them. #zb_dog_pending is only
# a fast gate though: whenever it claims dogs are pending, resync it from the real portal count so a
# desynced counter can't freeze the run. That scan only runs on the tick the round would complete.
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches 1.. store result score #zb_dog_pending {ns}.data if entity @e[tag={ns}.dog_portal]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches ..0 run function {ns}:v{version}/zombies/round_complete

# Check game over: only trigger when no healthy AND no downed players remain
# - Healthy: downed=0, gamemode=!spectator (playing normally)
# - Downed: downed=1, gamemode=spectator (spectating their mannequin, can be revived)
# - Bled out: downed=0, gamemode=spectator (waiting for next round — truly dead)
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_downed_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=1}},gamemode=spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. run scoreboard players operation #zb_alive_players {ns}.data += #zb_downed_alive {ns}.data
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 run function {ns}:v{version}/zombies/game_over

# Stuck zombie check (every 20 ticks, 24 random non-rising zombies; escorted ones are NoAI
# and already being rescued by their trader — see escort.py)
execute store result score #zb_tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #zb_tick_mod {ns}.data %= #20 {ns}.data
execute if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,limit=24,sort=random] at @s run function {ns}:v{version}/zombies/stuck_zombie_check

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn {ns}.data matches 0 run scoreboard players add #zb_stuck_timer {ns}.data 1
execute if score #zb_to_spawn {ns}.data matches 1.. run scoreboard players set #zb_stuck_timer {ns}.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer {ns}.data matches 1200.. run scoreboard players add #zb_glow_timer {ns}.data 1
execute if score #zb_glow_timer {ns}.data matches 100.. run scoreboard players set #zb_glow_timer {ns}.data 0
execute if score #zb_stuck_timer {ns}.data matches 1200.. if score #zb_glow_timer {ns}.data matches 0 if score #zb_alive {ns}.data matches 1.. run function {ns}:v{version}/zombies/glow_stuck_zombies

# Last-zombies fast path: once every zombie has spawned and only a handful remain, don't make
# players wait the full 60s before stragglers glow — glow them immediately (every 100t) so a
# single hard-to-find zombie can't drag the round out (common complaint from ~round 10 on).
execute unless score #zb_alive {ns}.data matches 1..3 run scoreboard players set #zb_fewleft_timer {ns}.data 0
execute if score #zb_to_spawn {ns}.data matches 0 if score #zb_alive {ns}.data matches 1..3 run scoreboard players add #zb_fewleft_timer {ns}.data 1
execute if score #zb_fewleft_timer {ns}.data matches 1 run function {ns}:v{version}/zombies/glow_stuck_zombies
execute if score #zb_fewleft_timer {ns}.data matches 100.. run scoreboard players set #zb_fewleft_timer {ns}.data 0

# Refresh sidebar every 5 ticks.
scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 5.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]
""")

	# Admin pause: game_tick is skipped so all timers stop.
	# Mobs get NoAI and players lose their movement/jump attributes.
	# Mobs that were ALREADY NoAI (rising spawns, escorted zombies) are left alone via the zb_frozen_ai tag, so unfreezing can't wake them up early.
	write_versioned_function("zombies/freeze_on", f"""
scoreboard players set #zb_freeze {ns}.data 1

# Mobs: only the ones actually moving right now
execute as @e[tag={ns}.zombie_round] unless data entity @s {{NoAI:1b}} run function {ns}:v{version}/zombies/freeze_mob

# Players: same attribute pair the prep countdown uses to hold everyone still
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

{TitleTimes.FREEZE.cmd(f'@a[scores={{{ns}.zb.in_game=1}}]')}
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"⏸","color":"aqua"}}]
tellraw @a [{MGS_TAG},{{"text":"An operator froze the game.","color":"aqua"}}]
""")

	write_versioned_function("zombies/freeze_mob", f"""
tag @s add {ns}.zb_frozen_ai
data merge entity @s {{NoAI:1b}}
""")

	write_versioned_function("zombies/freeze_off", f"""
scoreboard players set #zb_freeze {ns}.data 0

# Only wake the mobs freeze_on actually put to sleep
execute as @e[tag={ns}.zb_frozen_ai] run data merge entity @s {{NoAI:0b}}
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai

execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset

tellraw @a [{MGS_TAG},{{"text":"An operator unfroze the game.","color":"aqua"}}]
""")

	## Everything is paused while frozen — just keep telling players why nothing is happening.
	write_versioned_function("zombies/freeze_tick", f"""
scoreboard players add #zb_freeze_msg {ns}.data 1
execute if score #zb_freeze_msg {ns}.data matches 20.. run scoreboard players set #zb_freeze_msg {ns}.data 0
execute if score #zb_freeze_msg {ns}.data matches 0 run title @a[scores={{{ns}.zb.in_game=1}}] actionbar [{{"text":"⏸ GAME FROZEN","color":"aqua","bold":true}}]
""")

	# Death and respawn: zombies death handling enters the downed state.
	write_versioned_function("zombies/on_respawn", f"""
# Reset death counter
scoreboard players set @s {ns}.mp.death_count 0

# Increment "down count
scoreboard players add @s {ns}.zb.downs 1

# Enter downed state (revive system)
function {ns}:v{version}/zombies/revive/on_down
""")

	## Add player tick hook for zombies death detection
	write_versioned_function("player/tick", f"""
# Zombies: detect respawn
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn

# Dying Wish: tick down the escalating cooldown, and run the active berserk timer
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_cd matches 1.. run scoreboard players remove @s {ns}.zb.dw_cd 1
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_timer matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_tick
""")

