""" Simulated death, the spectate flow, kill messages and win conditions. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import REMAINING_BULLETS
from ...helpers.probes import Probe
from ...helpers.text import Text
from ...helpers.titles import TitleTimes
from ...progression.awards import MP_AWARDS
from ..gamemodes.dispatch import gm_dispatch


# Functions
def write_death_and_kills() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Run as the victim when lethal damage is intercepted (bullet, projectile) or on an OOB kill; mgs:input with.attacker may be absent.

	write_versioned_function("multiplayer/simulate_death", f"""
# A second bullet, OOB or vanilla death in the same tick.
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

# Healed so the player never really dies.
effect give @s instant_health 1 100 true
scoreboard players add @s {ns}.mp.deaths 1

# `{ns}:input with` is shared scratch that the signals below reuse (Scavenger refills, lore rewrites clear it),
# so the branch is decided on a score taken now and the signals get a private copy.
execute store success score #mp_death_attacked {ns}.data if data storage {ns}:input with.attacker
data modify storage {ns}:temp _mp_death set from storage {ns}:input with

# raycast/apply_damage sets `input with.headshot`. Read into a score because the key is absent for non-bullet deaths,
# and a macro naming a missing key fails the whole function.
scoreboard players set #mp_kill_headshot {ns}.data 0
execute store result score #mp_kill_headshot {ns}.data run data get storage {ns}:temp _mp_death.headshot

# Hit effects, hitmarker and DPS, for bullet hits.
execute if data storage {ns}:temp _mp_death.amount run function #{ns}:signals/damage with storage {ns}:temp _mp_death

execute if score #mp_death_attacked {ns}.data matches 1 run function {ns}:v{version}/multiplayer/simulate_death_fire_kill with storage {ns}:temp _mp_death

# No attacker: a random self-death message.
execute if score #mp_death_attacked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/random_death_message

# Shared with vanilla deaths (on_respawn).
function {ns}:v{version}/multiplayer/enter_death_spectate
""")

	## Run as the dying player; the caller may tag {ns}.temp_killer. Used by simulate_death and on_respawn.
	write_versioned_function("multiplayer/enter_death_spectate", f"""
# First, while the gun is still held: it can be picked up for 30 s.
execute at @s run function {ns}:v{version}/multiplayer/drop_held_weapon

# S&D: no respawn.
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} run return run function {ns}:v{version}/multiplayer/gamemodes/snd/on_death

# 3 s of spectating.
gamemode spectator @s
scoreboard players set @s {ns}.mp.spectate_timer 60

spectate @p[tag={ns}.temp_killer,gamemode=!spectator] @s
execute unless entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/spectate_random_player
tag @a[tag={ns}.temp_killer] remove {ns}.temp_killer

{TitleTimes.RESPAWN.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"Respawning in 3 seconds...","color":"gray"}}]
execute at @s run playsound minecraft:entity.player.hurt ambient @s
""")

	## Run as the victim; $(attacker) is the attacker selector.
	write_versioned_function("multiplayer/simulate_death_fire_kill", f"""
$tag $(attacker) add {ns}.temp_killer

# The victim tagged as killer: self-damage.
execute if entity @s[tag={ns}.temp_killer] run tag @s remove {ns}.temp_killer
execute unless entity @a[tag={ns}.temp_killer] run return run function {ns}:v{version}/multiplayer/random_self_kill_message

tag @s add {ns}.temp_victim
$execute as $(attacker) run function #{ns}:signals/on_kill
function {ns}:v{version}/multiplayer/random_kill_message
tag @s remove {ns}.temp_victim
""")

	## Captures the gun in hotbar.1 or 2 (hotbar.0 is the knife); the drop itself lives in core/weapon_drop, shared with mission enemies.
	write_versioned_function("multiplayer/drop_held_weapon", f"""
execute store result score #drop_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #drop_sel {ns}.data matches 1..2 run scoreboard players set #drop_sel {ns}.data 1
execute if score #drop_sel {ns}.data matches 1 unless items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0
execute if score #drop_sel {ns}.data matches 2 unless items entity @s hotbar.2 *[custom_data~{{{ns}:{{gun:true}}}}] run return 0

# Without its inventory Slot tag, so it fits an item_display or item entity.
execute if score #drop_sel {ns}.data matches 1 run {Probe.item("hotbar.1")}
execute if score #drop_sel {ns}.data matches 2 run {Probe.item("hotbar.2")}
data modify storage {ns}:temp _dropw set from entity {Probe.ITEM_DISPLAY} item

# The bullet count lives in the score; <= 0 makes the drop use half a magazine.
scoreboard players operation #drop_ammo {ns}.data = @s {ns}.{REMAINING_BULLETS}
function {ns}:v{version}/shared/drops/drop
""")

	## Self-deaths (OOB, environment).
	write_versioned_function("multiplayer/random_death_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"made a terrible mistake","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"forgot how gravity works","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"played themselves","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"left the battlefield","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"embraced the void","color":"gray"}}]
""")

	## Own grenade, RPG or explosion.
	write_versioned_function("multiplayer/random_self_kill_message", f"""
execute store result score #random_message {ns}.data run random value 1..5
execute if score #random_message {ns}.data matches 1 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"blew themselves up","color":"gray"}}]
execute if score #random_message {ns}.data matches 2 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"got a taste of their own medicine","color":"gray"}}]
execute if score #random_message {ns}.data matches 3 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"found out the blast radius the hard way","color":"gray"}}]
execute if score #random_message {ns}.data matches 4 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"didn't throw the grenade far enough","color":"gray"}}]
execute if score #random_message {ns}.data matches 5 run tellraw @a[scores={{{ns}.mp.in_game=1..}}] ["",{Text.player(ns, "@s")}," ",{{"text":"is their own worst enemy","color":"gray"}}]
""")

	## Kill messages, shared by simulate_death and on_respawn. Each verb exists with and without the headshot marker
	## (chosen on #mp_kill_headshot), since a tellraw cannot be appended to after it is sent.
	kill_verbs: list[tuple[str, str]] = [
		("eliminated",  ""),
		("took down",   ""),
		("dispatched",  ""),
		("sent",        "to the shadow realm"),
		("wiped",       "off the map"),
	]
	## Each line is sent twice: to the killer with the XP the kill was worth, and to everyone else without it.
	## Both copies share the #random_message guard, so the verb matches.
	kill_lines: list[str] = []
	for idx, (verb, tail) in enumerate(kill_verbs, start=1):
		body: str = (
			f'["",{Text.player(ns, f"@a[tag={ns}.temp_killer]")}," ",{{"text":"{verb}","color":"gray"}}'
			f',[" ",{Text.player(ns, f"@a[tag={ns}.temp_victim]")}]'
		)
		body += f',[" ",{{"text":"{tail}","color":"gray"}}]' if tail else ""
		for hs, hs_check in ((True, "matches 1"), (False, "matches 0")):
			marker: str = ',[" ",{"text":"💀 ","color":"white"},{"text":"HEADSHOT","color":"red","bold":true}]' if hs else ""
			# Kill plus headshot, and the killer's line says so.
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

	## Dispatched to the gamemode.
	write_versioned_function("multiplayer/on_kill_signal", f"""
execute unless data storage {ns}:multiplayer game{{state:"active"}} run return fail

{gm_dispatch(ns, version, "on_kill", ret=True)}
""", tags=[f"{ns}:signals/on_kill"])

	## Shared by TDM, DOM and HP.
	write_versioned_function("multiplayer/check_team_win", f"""
execute store result score #score_limit {ns}.data run data get storage {ns}:multiplayer game.score_limit
execute if score #red {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #score_limit {ns}.data run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}
""")

	write_versioned_function("multiplayer/team_wins", f"""
$tellraw @a ["","🏆 ",{{"text":"$(team) Team Wins!","color":"gold","bold":true}}]
tellraw @a ["",[{{"text":"","color":"gray"}},"  ",{{"text":"Final Score - Red"}},": "],{{"score":{{"name":"#red","objective":"{ns}.mp.team"}},"color":"red"}},[{{"text":"","color":"gray"}}," ",{{"text":"vs Blue"}},": "],{{"score":{{"name":"#blue","objective":"{ns}.mp.team"}},"color":"blue"}}]

function {ns}:v{version}/multiplayer/stop
""")

