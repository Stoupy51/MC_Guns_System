""" The game tick, the admin pause, the suspension of a run nobody is online for, and routing a death into the downed state. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.titles import TitleTimes
from ...player.revive.shared import SOLO_QR_MAX


# Functions
def write_zombies_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# #zb_freeze swaps in the freeze tick: 1 for the admin pause, 2 for a suspended run. Every zombies timer lives in game_tick,
	# so skipping it pauses the round. Offline players keep their scores, so the roster survives a restart.
	write_tick_file(f"""
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1.. unless entity @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/suspend
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1.. run function {ns}:v{version}/zombies/game_tick
execute if data storage {ns}:zombies game{{state:"active"}} if score #zb_freeze {ns}.data matches 1.. run function {ns}:v{version}/zombies/freeze_tick
""")

	write_versioned_function("zombies/game_tick", f"""
function {ns}:v{version}/zombies/revive/tick

function {ns}:v{version}/shared/maps/call_script_at_base {{mode:"zombies",script:"tick"}}

execute if score #zb_to_spawn {ns}.data matches 1.. run function {ns}:v{version}/zombies/spawn_tick

# Untyped: a spawn's mob can be any entity.
execute as @e[tag={ns}.zb_rising] at @s run function {ns}:v{version}/zombies/zombie_rise_tick
execute as @e[type=minecraft:marker,tag={ns}.zb_rise_dust] at @s run function {ns}:v{version}/zombies/rise_dust_tick

# Only when the map has bounds.
execute if score #zb_has_bounds {ns}.data matches 1 as @e[tag={ns}.zombie_round] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #zb_has_bounds {ns}.data matches 1 as @e[type=player,scores={{{ns}.zb.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/zombies/check_bounds_player

execute store result score #zb_alive {ns}.data if entity @e[tag={ns}.zombie_round]
# Enemies still in their portal are not entities. #zb_portal_pending is only a fast gate: when it claims pending enemies,
# it is resynced from the real portal count so a desynced counter cannot freeze the run.
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_portal_pending {ns}.data matches 1.. store result score #zb_portal_pending {ns}.data if entity @e[type=minecraft:marker,tag={ns}.zb_portal]
execute if score #zb_alive {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches 0 if score #zb_portal_pending {ns}.data matches ..0 run function {ns}:v{version}/zombies/round_complete

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
function {ns}:v{version}/zombies/freeze_world

{TitleTimes.FREEZE.cmd(f'@a[scores={{{ns}.zb.in_game=1}}]')}
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"⏸","color":"white"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"An operator froze the game.","color":"aqua"}}]
""")

	write_versioned_function("zombies/freeze_world", f"""
execute as @e[tag={ns}.zombie_round] unless data entity @s {{NoAI:1b}} run function {ns}:v{version}/zombies/freeze_mob
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/freeze_player
""")

	# The attribute pair the prep countdown uses.
	write_versioned_function("zombies/freeze_player", """
attribute @s minecraft:movement_speed base set 0
attribute @s minecraft:jump_strength base set 0
""")

	write_versioned_function("zombies/freeze_mob", f"""
tag @s add {ns}.zb_frozen_ai
data merge entity @s {{NoAI:1b}}
""")

	write_versioned_function("zombies/freeze_off", f"""
function {ns}:v{version}/zombies/unfreeze_world
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"An operator unfroze the game.","color":"aqua"}}]
""")

	write_versioned_function("zombies/unfreeze_world", f"""
scoreboard players set #zb_freeze {ns}.data 0
scoreboard players set #zb_resume_timer {ns}.data 0

# Only the mobs freeze_world put to sleep.
execute as @e[tag={ns}.zb_frozen_ai] run data merge entity @s {{NoAI:0b}}
tag @e[tag={ns}.zb_frozen_ai] remove {ns}.zb_frozen_ai

execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.zb.in_game=1}}] run attribute @s minecraft:jump_strength base reset
""")

	write_versioned_function("zombies/suspend", f"""
scoreboard players set #zb_freeze {ns}.data 2
function {ns}:v{version}/zombies/freeze_world
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Zombies game paused: nobody in it is online.","color":"aqua"}}]
""")

	## Every timer is paused; remind players why.
	write_versioned_function("zombies/freeze_tick", f"""
execute if score #zb_freeze {ns}.data matches 2 run return run function {ns}:v{version}/zombies/suspended_tick
scoreboard players add #zb_freeze_msg {ns}.data 1
execute if score #zb_freeze_msg {ns}.data matches 20.. run scoreboard players set #zb_freeze_msg {ns}.data 0
execute if score #zb_freeze_msg {ns}.data matches 0 run title @a[scores={{{ns}.zb.in_game=1}}] actionbar [{{"text":"⏸ ","color":"white"}},{{"text":"GAME FROZEN","color":"aqua","bold":true}}]
""")

	## Resumes 5 s after a roster player is back; the count restarts if they all leave again.
	write_versioned_function("zombies/suspended_tick", f"""
execute unless entity @a[scores={{{ns}.zb.in_game=1}}] run return run scoreboard players set #zb_resume_timer {ns}.data 0
scoreboard players add #zb_resume_timer {ns}.data 1
scoreboard players set #zb_resume_left {ns}.data 119
scoreboard players operation #zb_resume_left {ns}.data -= #zb_resume_timer {ns}.data
scoreboard players operation #zb_resume_left {ns}.data /= #20 {ns}.data
title @a[scores={{{ns}.zb.in_game=1}}] actionbar [{{"text":"⏸ ","color":"white"}},{{"text":"PAUSED","color":"aqua","bold":true}},{{"text":", resuming in ","color":"gray"}},{{"score":{{"name":"#zb_resume_left","objective":"{ns}.data"}},"color":"white"}}]
execute if score #zb_resume_timer {ns}.data matches 100.. run function {ns}:v{version}/zombies/resume
""")

	write_versioned_function("zombies/resume", f"""
function {ns}:v{version}/zombies/unfreeze_world
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The game resumes!","color":"green"}}]
""")

	## Run as a roster player back in the run they left, which kept the rest of their state.
	write_versioned_function("zombies/rejoin", f"""
execute if score #zb_freeze {ns}.data matches 1.. run function {ns}:v{version}/zombies/freeze_player
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s"}},{{"text":" is back in the game.","color":"green"}}]

# A body is removed while its owner is away (revive/orphan_check). A downed player then comes back as at a round end, a doppelganger without a body forfeits it.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute if entity @s[tag={ns}.downed_spectator] unless entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] run function {ns}:v{version}/zombies/revive/do_round_respawn
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.ww.id
execute if entity @s[tag={ns}.ww_active] unless entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] run function {ns}:v{version}/zombies/whos_who/forfeit
""")

	write_versioned_function("zombies/on_respawn", f"""
scoreboard players set @s {ns}.mp.death_count 0

scoreboard players add @s {ns}.zb.downs 1

function {ns}:v{version}/zombies/revive/on_down
""")

	write_versioned_function("player/tick", f"""
execute if score @s {ns}.zb.rejoins matches 1.. run function {ns}:v{version}/zombies/on_rejoin
execute if data storage {ns}:zombies game{{state:"active"}} if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/zombies/on_respawn

# Dying Wish: escalating cooldown and berserk timer.
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1.. if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_cd matches 1.. run scoreboard players remove @s {ns}.zb.dw_cd 1
execute if data storage {ns}:zombies game{{state:"active"}} unless score #zb_freeze {ns}.data matches 1.. if score @s {ns}.zb.in_game matches 1.. if score @s {ns}.zb.dw_timer matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_tick
""")

