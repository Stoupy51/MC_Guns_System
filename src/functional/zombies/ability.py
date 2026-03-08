
# ruff: noqa: E501
# Zombies Ability & Passive System
# Provides passive effects and activatable abilities for the zombies game mode.
# Passives: x1.2 Points, x1.5 Powerups
# Abilities: Coward (TP to spawn), Guardian (summon Iron Golem)
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


def generate_zombies_abilities() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Selection Dialogs
	# Trigger values for zombies perks (dispatched in player_config.py)
	TRIG_ZB_PASSIVE_1: int = 6   # x1.2 points
	TRIG_ZB_PASSIVE_2: int = 7   # x1.5 powerups
	TRIG_ZB_ABILITY_1: int = 8   # Coward
	TRIG_ZB_ABILITY_2: int = 9   # Guardian

	write_versioned_function("zombies/passive_ability_menu", f"""
# Show the passive selection dialog (ability dialog is shown after)
dialog show @s {{type:"minecraft:multi_action",title:{{text:"Zonweeb Passive",color:"dark_green"}},body:{{type:"minecraft:plain_message",contents:{{text:"Choose a passive effect for this game.",color:"gray"}}}},columns:1,after_action:"close",exit_action:{{label:"Skip"}},actions:[{{label:[{{"text":"💰 ","color":"gold"}},{{"text":"x1.2 Points"}}],tooltip:{{text:"Earn 20% more points from kills (permanent)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_1}"}}}},{{label:[{{"text":"⏱ ","color":"aqua"}},{{"text":"x1.5 Powerups"}}],tooltip:{{text:"All powerup durations last 50% longer"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_PASSIVE_2}"}}}}]}}
""")

	write_versioned_function("zombies/ability_menu", f"""
# Show the ability selection dialog
dialog show @s {{type:"minecraft:multi_action",title:{{text:"Zonweeb Ability",color:"dark_green"}},body:{{type:"minecraft:plain_message",contents:{{text:"Choose an ability for this game.",color:"gray"}}}},columns:1,after_action:"close",exit_action:{{label:"Skip"}},actions:[{{label:[{{"text":"🏃 ","color":"yellow"}},{{"text":"Coward"}}],tooltip:{{text:"TP to spawn when under 50% HP (1 round cooldown)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_1}"}}}},{{label:[{{"text":"🛡 ","color":"green"}},{{"text":"Guardian"}}],tooltip:{{text:"Summon an Iron Golem ally at round start (1 round cooldown)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_ABILITY_2}"}}}}]}}
""")

	# Passive Selection (called via trigger dispatch) ───────────

	write_versioned_function("zombies/perks/set_passive_1", f"""
scoreboard players set @s {ns}.zb.passive 1
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.2 Points","color":"gold"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	write_versioned_function("zombies/perks/set_passive_2", f"""
scoreboard players set @s {ns}.zb.passive 2
tellraw @s [{MGS_TAG},{{"text":"Passive set: ","color":"gray"}},{{"text":"x1.5 Powerups","color":"aqua"}}]
function {ns}:v{version}/zombies/ability_menu
""")

	# Ability Selection (called via trigger dispatch) ────────────

	write_versioned_function("zombies/perks/set_ability_1", f"""
scoreboard players set @s {ns}.zb.ability 1
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Coward","color":"yellow"}},{{"text":" (TP to spawn when below 50% HP)","color":"gray"}}]
""")

	write_versioned_function("zombies/perks/set_ability_2", f"""
scoreboard players set @s {ns}.zb.ability 2
scoreboard players set @s {ns}.zb.ability_cd 0
tellraw @s [{MGS_TAG},{{"text":"Ability set: ","color":"gray"}},{{"text":"Guardian","color":"green"}},{{"text":" (Summon an Iron Golem ally)","color":"gray"}}]
""")

	# Ability Tick (check and trigger abilities) ────────────────

	write_versioned_function("zombies/ability_tick", f"""
# Coward: TP to spawn when under 50% health (10 HP out of 20), cooldown not active
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=1,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/check_coward
""")

	write_versioned_function("zombies/perks/check_coward", f"""
# Check health: 10 HP = 50% of default 20 HP max
execute store result score #hp {ns}.data run data get entity @s Health 1
execute if score #hp {ns}.data matches ..10 run function {ns}:v{version}/zombies/perks/trigger_coward
""")

	write_versioned_function("zombies/perks/trigger_coward", f"""
# Teleport to a player spawn point
function {ns}:v{version}/zombies/respawn_tp

# Set cooldown (1 round)
scoreboard players set @s {ns}.zb.ability_cd 1

# Effects
effect give @s speed 5 1 true
effect give @s regeneration 5 1 true

# Announce
title @s actionbar [{{"text":"🏃 Coward activated! Teleported to safety!","color":"yellow"}}]
""")

	# Guardian: summon Iron Golem at round start ─────────────────

	write_versioned_function("zombies/perks/check_guardian", f"""
# Check guardian ability for all players with it ready
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability=2,{ns}.zb.ability_cd=0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/perks/trigger_guardian
""")

	write_versioned_function("zombies/perks/trigger_guardian", f"""
# Summon an Iron Golem ally near the player
summon minecraft:iron_golem ~ ~ ~ {{Tags:["{ns}.guardian_golem","{ns}.gm_entity"],PlayerCreated:0b,CustomName:{{"text":"Guardian","color":"green"}}}}

# Set cooldown (1 round)
scoreboard players set @s {ns}.zb.ability_cd 1

# Announce
title @s actionbar [{{"text":"🛡 Guardian activated! Iron Golem summoned!","color":"green"}}]
""")

	# Cooldown Reduction (called at round start) ────────────────

	write_versioned_function("zombies/perks/reduce_cooldowns", f"""
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.ability_cd=1..}}] run scoreboard players remove @s {ns}.zb.ability_cd 1
""")

	# Hooks into game_tick and start_round (APPENDS) ────────────

	# Hook ability tick into game_tick
	write_versioned_function("zombies/game_tick", f"""
# Ability tick
function {ns}:v{version}/zombies/ability_tick
""")

	# Hook cooldown reduction and guardian into round start
	write_versioned_function("zombies/start_round", f"""
# Reduce ability cooldowns
function {ns}:v{version}/zombies/perks/reduce_cooldowns

# Check guardian ability (summon golem at round start)
function {ns}:v{version}/zombies/perks/check_guardian
""")

