""" Zombies ability and passive system.

Provides passive effects and activatable abilities for the zombies game mode.

Passives: x1.2 Points, x1.5 Powerups Abilities: Coward (TP to spawn), Guardian (summon Iron Golem)
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.dialogs import Dialogs


# Functions
def generate_zombies_abilities() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Trigger values for the Zonweeb passives and abilities (dispatched in player_config).
	TRIG_ZB_PASSIVE_1: int = 6   # x1.2 points
	TRIG_ZB_PASSIVE_2: int = 7   # x1.5 powerups
	TRIG_ZB_ABILITY_1: int = 8   # Coward
	TRIG_ZB_ABILITY_2: int = 9   # Guardian

	## Shown after the variant guard of the functions below.
	Dialogs.register_dialog("zombies/passive_ability", {
		"type": "minecraft:multi_action",
		"title": {"text": "Zonweeb Passive", "color": "dark_green"},
		"body": {"type": "minecraft:plain_message", "contents": {"text": "Choose a passive effect for this game.", "color": "gray"}},
		"columns": 1,
		"after_action": "close",
		"exit_action": {"label": "Skip"},
		"actions": [
			{"label": ["", "💰 ", {"text": "x1.2 Points", "color": "gold"}], "tooltip": {"text": "Earn 20% more points from kills (permanent)"},
				"action": {"type": "run_command", "command": f"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_1}"}},
			{"label": ["", "⏱ ", {"text": "x1.5 Powerups", "color": "aqua"}], "tooltip": {"text": "All powerup durations last 50% longer"},
				"action": {"type": "run_command", "command": f"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_2}"}},
		],
	})

	write_versioned_function("zombies/passive_ability_menu", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
# The ability dialog follows.
dialog show @s {Dialogs.dialog_ref('zombies/passive_ability')}
""")

	Dialogs.register_dialog("zombies/ability", {
		"type": "minecraft:multi_action",
		"title": {"text": "Zonweeb Ability", "color": "dark_green"},
		"body": {"type": "minecraft:plain_message", "contents": {"text": "Choose an ability for this game.", "color": "gray"}},
		"columns": 1,
		"after_action": "close",
		"exit_action": {"label": "Skip"},
		"actions": [
			{"label": ["", "🏃 ", {"text": "Coward", "color": "yellow"}], "tooltip": {"text": "TP to spawn when under 50% HP (1 round cooldown)"},
				"action": {"type": "run_command", "command": f"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_1}"}},
			{"label": ["", "🛡 ", {"text": "Guardian", "color": "green"}], "tooltip": {"text": "Summon an Iron Golem ally at round start (1 round cooldown)"},
				"action": {"type": "run_command", "command": f"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_2}"}},
		],
	})

	write_versioned_function("zombies/ability_menu", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
dialog show @s {Dialogs.dialog_ref('zombies/ability')}
""")

	write_versioned_function("zombies/perks/set_passive_1", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
scoreboard players set @s {ns}.zb.passive 1
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.2 Points","color":"gold"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	write_versioned_function("zombies/perks/set_passive_2", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
scoreboard players set @s {ns}.zb.passive 2
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.5 Powerups","color":"aqua"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	write_versioned_function("zombies/perks/set_ability_1", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
scoreboard players set @s {ns}.zb.ability 1
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Coward","color":"yellow"}},{{"text":" (TP to spawn when below 50% HP)","color":"gray"}}]
""")

	write_versioned_function("zombies/perks/set_ability_2", f"""
execute unless data storage {ns}:zombies game{{variant:"zonweeb"}} run return fail
scoreboard players set @s {ns}.zb.ability 2
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Guardian","color":"green"}},{{"text":" (Summon an Iron Golem ally)","color":"gray"}}]
""")

	write_versioned_function("zombies/ability_tick", f"""
# Coward: below half health, teleport to a spawn (1-round cooldown).
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=1,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/check_coward
""")

	write_versioned_function("zombies/perks/check_coward", f"""
# 10 HP is half the default 20.
execute store result score #hp {ns}.data run data get entity @s Health 1
execute if score #hp {ns}.data matches ..10 run function {ns}:v{version}/zombies/perks/trigger_coward
""")

	write_versioned_function("zombies/perks/trigger_coward", f"""
function {ns}:v{version}/zombies/respawn_tp

scoreboard players set @s {ns}.zb.ability_cd 1

effect give @s speed 5 1 true
effect give @s regeneration 5 1 true

title @s actionbar [{{"text":"🏃 ","color":"white"}},{{"text":"Coward activated! Teleported to safety!","color":"yellow"}}]
""")

	# Guardian: an Iron Golem ally at round start (1-round cooldown).

	write_versioned_function("zombies/perks/check_guardian", f"""
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=2,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/trigger_guardian
""")

	write_versioned_function("zombies/perks/trigger_guardian", f"""
summon minecraft:iron_golem ~ ~ ~ {{Tags:["{ns}.guardian_golem","{ns}.gm_entity"],PlayerCreated:0b,CustomName:{{"text":"Guardian","color":"green"}}}}

scoreboard players set @s {ns}.zb.ability_cd 1

title @s actionbar [{{"text":"🛡 ","color":"white"}},{{"text":"Guardian activated! Iron Golem summoned!","color":"green"}}]
""")

	# Run at round start.

	write_versioned_function("zombies/perks/reduce_cooldowns", f"""
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability_cd=1..}}] run scoreboard players remove @s {ns}.zb.ability_cd 1
""")

	write_versioned_function("zombies/game_tick", f"""
# Zonweeb only.
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} run function {ns}:v{version}/zombies/ability_tick
""")

	write_versioned_function("zombies/start_round", f"""
# Zonweeb only.
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} run function {ns}:v{version}/zombies/perks/reduce_cooldowns
execute if data storage {ns}:zombies game{{variant:"zonweeb"}} run function {ns}:v{version}/zombies/perks/check_guardian
""")

