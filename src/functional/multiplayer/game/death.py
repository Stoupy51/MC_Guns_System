""" Simulated death, the spectate flow, kill messages and win conditions. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import REMAINING_BULLETS
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_death_and_kills() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Simulated Death.
	# Called when lethal damage is intercepted (bullet/projectile) or for OOB kills @s = victim player; storage mgs:input with.attacker may or may not exist

	write_versioned_function("multiplayer/simulate_death", f"""
# Ignore duplicate deaths (second bullet / OOB / vanilla death landing in the same tick as another death)
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Heal to prevent actual death & Increment death stats
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mp.deaths 1

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage {ns}:input with.amount run function #{ns}:signals/damage with storage {ns}:input with

# Fire kill signal as attacker (if attacker exists in input)
execute if data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/simulate_death_fire_kill with storage {ns}:input with

# No attacker: random funny self-death message
execute unless data storage {ns}:input with.attacker run function {ns}:v{version}/multiplayer/random_death_message

# Enter death spectate (shared with vanilla-death on_respawn)
function {ns}:v{version}/multiplayer/enter_death_spectate
""")

	## Shared death-spectate flow (@s = dying player, {ns}.temp_killer may be tagged by the caller) Used by simulate_death (bullet/OOB deaths) and on_respawn (vanilla deaths)
	write_versioned_function("multiplayer/enter_death_spectate", f"""
# Drop the held gun on the ground (pickable for 30s) before anything else, while still holding it
execute at @s run function {ns}:v{version}/multiplayer/drop_held_weapon

# S&D: no respawning, mark as dead and go spectator
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_death

# Set player to spectator mode for 3 seconds (60 ticks)
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

# Spectate attacker (if tagged) or random alive player
spectate @p[tag={ns}.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/spectate_random_player
tag @a[tag={ns}.temp_killer] remove {ns}.temp_killer

# Announce death & playsound
title @s title ["☠"]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s
""")

	## Fire kill signal as attacker + death message (macro function) @s = victim, $(attacker) = attacker selector from storage
	write_versioned_function("multiplayer/simulate_death_fire_kill", f"""
$tag $(attacker) add {ns}.temp_killer

# Self-kill check: if victim(@s) is also tagged as killer, it's self-damage
execute if entity @s[tag={ns}.temp_killer] run tag @s remove {ns}.temp_killer
execute unless entity @a[tag={ns}.temp_killer] run return run function {ns}:v{version}/multiplayer/random_self_kill_message

# Normal kill: fire signal and show message
tag @s add {ns}.temp_victim
$execute as $(attacker) run function #{ns}:signals/on_kill
function {ns}:v{version}/multiplayer/random_kill_message
tag @s remove {ns}.temp_victim
""")

	## ── On-death weapon drop.
	## Captures the gun in the player's selected weapon slot (hotbar.1/2); the drop itself (spawn, 30s pickup window, spare magazine) lives in core/weapon_drop.py, shared with the mission-enemy drop.
	write_versioned_function("multiplayer/drop_held_weapon", f"""
# Only drop a gun held in a weapon slot (hotbar.1 or hotbar.2; hotbar.0 is the knife)
execute store result score #drop_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #drop_sel {ns}.data matches 1..2 run scoreboard players set #drop_sel {ns}.data 1
execute if score #drop_sel {ns}.data matches 1 unless items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0
execute if score #drop_sel {ns}.data matches 2 unless items entity @s hotbar.2 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0

# Capture the held gun item (strip the inventory Slot tag so it fits an item_display / item entity)
data remove storage {ns}:temp _dropw
execute if score #drop_sel {ns}.data matches 1 run data modify storage {ns}:temp _dropw set from entity @s Inventory[{{Slot:1b}}]
execute if score #drop_sel {ns}.data matches 2 run data modify storage {ns}:temp _dropw set from entity @s Inventory[{{Slot:2b}}]
data remove storage {ns}:temp _dropw.Slot

# The live bullet count lives on the scoreboard, not in the item (<= 0 makes the drop use half a mag)
scoreboard players operation #drop_ammo {ns}.data = @s {ns}.{REMAINING_BULLETS}
function {ns}:v{version}/shared/drops/drop
""")

	## Random death message for self-deaths (OOB, environmental)
	write_versioned_function("multiplayer/random_death_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"made a terrible mistake","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"forgot how gravity works","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"played themselves","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"left the battlefield","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"embraced the void","color":"gray"}}]
""")

	## Random self-kill message (grenade, RPG, own explosion)
	write_versioned_function("multiplayer/random_self_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"blew themselves up","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"got a taste of their own medicine","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"found out the blast radius the hard way","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"didn't throw the grenade far enough","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@s"}}," ",{{"text":"is their own worst enemy","color":"gray"}}]
""")

	## Random kill message (uses temp_killer/temp_victim tags, shared by simulate_death + on_respawn)
	write_versioned_function("multiplayer/random_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"eliminated","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"took down","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"dispatched","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"sent","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}," ",{{"text":"to the shadow realm","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{{"selector":"@a[tag={ns}.temp_killer]"}}," ",{{"text":"wiped","color":"gray"}}," ",{{"selector":"@a[tag={ns}.temp_victim]"}}," ",{{"text":"off the map","color":"gray"}}]
""")

	## Kill Tracking (Signal Listener) - now dispatches to gamemode
	write_versioned_function("multiplayer/on_kill_signal", f"""
# Only process if multiplayer game is active
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

# Dispatch to gamemode-specific kill handler
{gm_dispatch(ns, version, "on_kill", ret=True)}
""", tags=[f"{ns}:signals/on_kill"])

	## Check Team Win (shared by TDM, DOM, HP)
	write_versioned_function("multiplayer/check_team_win", f"""
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""")

	## Team Wins
	write_versioned_function("multiplayer/team_wins", f"""
# Announce winner
$tellraw @a ["","🏆 ",{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

# End game
function {ns}:v{version}/multiplayer/stop
""")

