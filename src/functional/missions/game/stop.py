""" Ending a mission and late joining one. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers import MGS_TAG
from ...helpers.lifecycle import GameLifecycle


# Functions
def write_missions_stop() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Game Stop
	write_versioned_function("missions/stop", f"""
# Various cleanup and reset tasks to return to lobby state
data modify storage {ns}:missions game.state set value "lobby"
schedule clear {ns}:v{version}/missions/end_prep
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={{{ns}.mi.in_game=1}}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={{{ns}.mi.in_game=1}}] darkness
effect clear @a[scores={{{ns}.mi.in_game=1}}] blindness
effect clear @a[scores={{{ns}.mi.in_game=1}}] night_vision
gamemode adventure @a[scores={{{ns}.mi.in_game=1}},gamemode=spectator]
clear @a[scores={{{ns}.mi.in_game=1}}] compass[custom_data~{{{ns}:{{compass:true}}}}]

kill @e[tag={ns}.mission_enemy]
kill @e[tag={ns}.gm_entity]

# Remove forceload
execute if score #mi_has_boundary {ns}.data matches 1 run function {ns}:v{version}/shared/remove_forceload

# Signal mission end
function #{ns}:missions/on_mission_end

{GameLifecycle.regen_disable_lines(ns)}

tellraw @a [{MGS_TAG},{{"text":"Mission ended.","color":"red"}}]

execute as @a[scores={{{ns}.mi.in_game=1}}] run function {ns}:v{version}/shared/maps/call_script_at_base {{script:"leave"}}

# Reset in-game state
scoreboard players set @a[scores={{{ns}.mi.in_game=1}}] {ns}.mp.team 0
scoreboard players set @a {ns}.mi.in_game 0
scoreboard players set #mi_timer {ns}.data 0
scoreboard players set #mi_total_enemies {ns}.data 0
scoreboard players set #mi_has_boundary {ns}.data 0
scoreboard players set @a {ns}.mi.kills 0
scoreboard players set @a {ns}.mi.deaths 0
tag @a[tag={ns}.give_class_menu] remove {ns}.give_class_menu
""")

	## Join Ongoing Mission (late-joiner support)
	write_versioned_function("missions/join_game", GameLifecycle.late_join_flow_lines(
		ns,
		"missions",
		f"{ns}.mi.in_game",
		"No active mission to join!",
		"You are already in the mission!",
		f"""
scoreboard players set @s {ns}.mi.in_game 1
scoreboard players set @s {ns}.mp.team 1
team join {ns}.blue @s
scoreboard players set @s {ns}.mi.kills 0
scoreboard players set @s {ns}.mi.deaths 0
scoreboard players set @s {ns}.mp.death_count 0
scoreboard players set @s {ns}.mp.spectate_timer 0
""",
		f"{ns}:v{version}/missions/respawn_tp",
		"joined the mission!",
		"green",
		post_class_lines=f"item replace entity @s hotbar.3 with compass[custom_data={{{ns}:{{compass:true}}}}]",
	))

