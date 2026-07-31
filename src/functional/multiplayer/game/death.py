""" Simulated death, the spectate flow, kill messages and win conditions. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import REMAINING_BULLETS
from ...helpers.text import Text
from ...helpers.titles import TitleTimes
from ...progression.awards import MP_AWARDS
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

# `{ns}:input with` is GLOBAL scratch: the signals fired below reuse it (the killer's Scavenger perk
# refills their magazines, and every lore rewrite clears `input with`), so re-reading it after
# a signal used to lose the attacker and print an unattributed death message on top of the kill
# message. Decide the branch on a score taken now, and pass the signals a private copy.
execute store success score #mp_death_attacked {ns}.data if data storage {ns}:input with.attacker
data modify storage {ns}:temp _mp_death set from storage {ns}:input with

# Was the killing hit a headshot? Set by raycast/apply_damage into `input with.headshot`. Read into a score
# rather than passed through the kill macro because the key is simply absent for non-bullet deaths (an
# explosion, the void), and a macro referencing a missing key fails the whole function.
scoreboard players set #mp_kill_headshot {ns}.data 0
execute store result score #mp_kill_headshot {ns}.data run data get storage {ns}:temp _mp_death.headshot

# Fire damage signal (hit effects, hitmarker, DPS) if this came from a bullet hit
execute if data storage {ns}:temp _mp_death.amount run function #{ns}:signals/damage with storage {ns}:temp _mp_death

# Fire kill signal as attacker (if attacker exists in input)
execute if score #mp_death_attacked {ns}.data matches 1 run function {ns}:v{version}/multiplayer/simulate_death_fire_kill with storage {ns}:temp _mp_death

# No attacker: random funny self-death message
execute if score #mp_death_attacked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/random_death_message

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
{TitleTimes.RESPAWN.cmd()}
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
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"made a terrible mistake","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"forgot how gravity works","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"played themselves","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"left the battlefield","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"embraced the void","color":"gray"}}]
""")

	## Random self-kill message (grenade, RPG, own explosion)
	write_versioned_function("multiplayer/random_self_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"blew themselves up","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"got a taste of their own medicine","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"found out the blast radius the hard way","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"didn't throw the grenade far enough","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"is their own worst enemy","color":"gray"}}]
""")

	## Random kill message (uses temp_killer/temp_victim tags, shared by simulate_death + on_respawn).
	## Each verb exists twice, with and without the headshot marker, chosen on #mp_kill_headshot: a tellraw
	## is one atomic message, so the marker cannot be appended to an already-sent line, and putting it on a
	## second line would double every kill in the feed. The pair is generated rather than written out.
	kill_verbs: list[tuple[str, str]] = [
		("eliminated",  ""),
		("took down",   ""),
		("dispatched",  ""),
		("sent",        "to the shadow realm"),
		("wiped",       "off the map"),
	]
	## Every line is emitted twice more than it looks: once to the killer, carrying the XP that kill was
	## worth, and once to everyone else without it. A score component resolves in the executor's context
	## rather than per recipient, so one tellraw cannot say "+20 XP" to only one of the people reading it.
	## Both copies sit under the same #random_message guard, so the verb stays identical between them.
	kill_lines: list[str] = []
	for idx, (verb, tail) in enumerate(kill_verbs, start=1):
		body: str = (
			f'["",{Text.player(ns, f"@a[tag={ns}.temp_killer]")}," ",{{"text":"{verb}","color":"gray"}}'
			f',[" ",{Text.player(ns, f"@a[tag={ns}.temp_victim]")}]'
		)
		body += f',[" ",{{"text":"{tail}","color":"gray"}}]' if tail else ""
		for hs, hs_check in ((True, "matches 1"), (False, "matches 0")):
			marker: str = ',[" ",{"text":"💀 HEADSHOT","color":"red","bold":true}]' if hs else ""
			# A headshot kill is worth kill + headshot, and the killer's line says so
			earned: int = MP_AWARDS["kill"].amount + (MP_AWARDS["headshot"].amount if hs else 0)
			for who, xp in (
				(f"@a[scores={{{ns}.mp.in_game=1..}},tag=!{ns}.temp_killer]", ""),
				(f"@a[tag={ns}.temp_killer]", f',[" ",{{"text":"+{earned} XP","color":"gold"}}]'),
			):
				kill_lines.append(
					f"execute if score #random_message {ns}.data matches {idx}"
					f" if score #mp_kill_headshot {ns}.data {hs_check}"
					f" run tellraw {who} {body}{marker}{xp}]"
				)
	newline: str = "\n"
	write_versioned_function("multiplayer/random_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..{len(kill_verbs)}
{newline.join(kill_lines)}
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

