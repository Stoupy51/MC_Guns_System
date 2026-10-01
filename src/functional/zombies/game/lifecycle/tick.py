""" The game tick, the admin pause and routing a death into the downed state. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.titles import TitleTimes
from ...player.revive.shared import SOLO_QR_MAX


# Functions
def write_zombies_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_tick_file(f"""
# #zb_freeze (admin menu) swaps in the freeze tick: every zombies timer lives in game_tick, so skipping it pauses the round.
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1 run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"active"}} if score #zb_freeze {ns}.data matches 1 run function {ns}:v{version}/zombies/freeze_tick
""")

	write_versioned_function("zombies/game_tick", f"""
function {ns}:v{version}/zombies/revive/tick

function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}

execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

execute as @e[type=minecraft:zombie,tag={ns}.zb_rising] at @s run function {ns}:v{version}/zombies/zombie_rise_tick

# Only when the map has bounds.
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds_player

execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
# Dogs still in their portal are not entities. #zb_dog_pending is only a fast gate: when it claims pending dogs,
# it is resynced from the real portal count so a desynced counter cannot freeze the run.
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches 1.. store result score #zb_dog_pending {ns}.data if entity @e[type=minecraft:marker,tag={ns}.dog_portal]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_dog_pending {ns}.data matches ..0 run function {ns}:v{version}/zombies/round_complete

# Game over once nobody is left to revive anyone. Healthy: downed=0, not spectator (Who's Who owners included);
# downed: downed=1, spectator; bled out: downed=0, spectator. Solo Quick Revive with uses left revives on its own.
execute if score #zb_round_grace {ns}.data matches 1.. run scoreboard players remove #zb_round_grace {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. store result score #zb_alive_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 if score #zb_ingame_total {ns}.data matches 1 store success score #zb_alive_players {ns}.data as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=1}},tag={ns}.zb_qr_armed] unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}..

# Nobody left for two ticks in a row, so a revive or respawn landing on the same tick cannot end the run.
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 1.. run scoreboard players set #zb_nobody_ticks {ns}.data 0
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_alive_players {ns}.data matches 0 run scoreboard players add #zb_nobody_ticks {ns}.data 1
execute unless score #zb_round_grace {ns}.data matches 1.. if score #zb_nobody_ticks {ns}.data matches 2.. run function {ns}:v{version}/zombies/game_over

# Every 20 ticks, 24 random non-rising zombies; escorted ones are NoAI and already being rescued (see escort).
execute store result score #zb_tick_mod {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #zb_tick_mod {ns}.data %= #20 {ns}.data
execute if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,limit=24,sort=random] at @s run function {ns}:v{version}/zombies/stuck_zombie_check

# Every player in the run glows yellow.
execute if score #zb_tick_mod {ns}.data matches 0 run effect give @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] minecraft:glowing 3 0 true

# Stragglers glow 60 s (1200 ticks) after the last spawn.
execute if score #zb_to_spawn {ns}.data matches 0 run scoreboard players add #zb_stuck_timer {ns}.data 1
execute if score #zb_to_spawn {ns}.data matches 1.. run scoreboard players set #zb_stuck_timer {ns}.data 0
# Then glowing for 6 s every 5 s.
execute if score #zb_stuck_timer {ns}.data matches 1200.. run scoreboard players add #zb_glow_timer {ns}.data 1
execute if score #zb_glow_timer {ns}.data matches 100.. run scoreboard players set #zb_glow_timer {ns}.data 0
execute if score #zb_stuck_timer {ns}.data matches 1200.. if score #zb_glow_timer {ns}.data matches 0 if score #zb_alive {ns}.data matches 1.. run function {ns}:v{version}/zombies/glow_stuck_zombies

# With 3 or fewer zombies left they glow every 5 s right away, so one hard-to-find zombie cannot drag the round out.
execute unless score #zb_alive {ns}.data matches 1..3 run scoreboard players set #zb_fewleft_timer {ns}.data 0
execute if score #zb_to_spawn {ns}.data matches 0 if score #zb_alive {ns}.data matches 1..3 run scoreboard players add #zb_fewleft_timer {ns}.data 1
execute if score #zb_fewleft_timer {ns}.data matches 1 run function {ns}:v{version}/zombies/glow_stuck_zombies
execute if score #zb_fewleft_timer {ns}.data matches 100.. run scoreboard players set #zb_fewleft_timer {ns}.data 0

scoreboard players add #zb_sidebar_timer {ns}.data 1
execute if score #zb_sidebar_timer {ns}.data matches 5.. run scoreboard players set #zb_sidebar_timer {ns}.data 0
execute if score #zb_sidebar_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/refresh_sidebar

kill @e[type=experience_orb]
""")

	# Admin pause: mobs get NoAI and players lose movement and jump.
	# Mobs already NoAI (rising, escorted) carry zb_frozen_ai, so unfreezing cannot wake them early.
	write_versioned_function("zombies/freeze_on", f"""
scoreboard players set #zb_freeze {ns}.data 1

execute as @e[tag={ns}.zombie_round] unless data entity @s {{NoAI:1b}} run function {ns}:v{version}/zombies/freeze_mob

# The attribute pair the prep countdown uses.
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base set 0

{TitleTimes.FREEZE.cmd(f'@a[scores={{{ns}.zb.in_game=1}}]')}
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"⏸","color":"white"}}]
tellraw @a [{MGS_TAG},{{"text":"An operator froze the game.","color":"aqua"}}]
""")

	write_versioned_function("zombies/freeze_mob", f"""
tag @s add {ns}.zb_frozen_ai
data merge entity @s {{NoAI:1b}}
""")

	write_versioned_function("zombies/freeze_off", f"""
scoreboard players set #zb_freeze {ns}.data 0

# Only the mobs freeze_on put to sleep.
execute as @e[tag={ns}.zb_frozen_ai] run data merge entity @s {{NoAI:0b}}
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai

execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset

tellraw @a [{MGS_TAG},{{"text":"An operator unfroze the game.","color":"aqua"}}]
""")

	## Every timer is paused; remind players why.
	write_versioned_function("zombies/freeze_tick", f"""
scoreboard players add #zb_freeze_msg {ns}.data 1
execute if score #zb_freeze_msg {ns}.data matches 20.. run scoreboard players set #zb_freeze_msg {ns}.data 0
execute if score #zb_freeze_msg {ns}.data matches 0 run title @a[scores={{{ns}.zb.in_game=1}}] actionbar [{{"text":"⏸ ","color":"white"}},{{"text":"GAME FROZEN","color":"aqua","bold":true}}]
""")

	write_versioned_function("zombies/on_respawn", f"""
scoreboard players set @s {ns}.mp.death_count 0

scoreboard players add @s {ns}.zb.downs 1

function {ns}:v{version}/zombies/revive/on_down
""")

	write_versioned_function("player/tick", f"""
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn

# Dying Wish: escalating cooldown and berserk timer.
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_cd matches 1.. run scoreboard players remove @s {ns}.zb.dw_cd 1
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_timer matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_tick
""")

