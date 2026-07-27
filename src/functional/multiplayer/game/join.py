""" Late joining an ongoing match. """
# Imports
from stewbeet import Mem, write_versioned_function

from ...helpers.lifecycle import GameLifecycle


# Functions
def write_multiplayer_join() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Join Ongoing Game (late-joiner support)
	write_versioned_function("multiplayer/join_game", GameLifecycle.late_join_flow_lines(
	ns,
	"multiplayer",
	f"{ns}.mp.in_game",
	"No active game to join!",
	"You are already in the game!",
	f"""
scoreboard players set @s {ns}.mp.in_game 1
scoreboard players set @s {ns}.mp.kills 0
scoreboard players set @s {ns}.mp.deaths 0
scoreboard players set @s {ns}.mp.death_count 0
scoreboard players set @s {ns}.mp.spectate_timer 0
scoreboard players set @s {ns}.last_hit 0
execute store result score @s {ns}.hp_prev run data get entity @s Health 1

# Assign to FFA team for ffa mode, otherwise auto-assign to team
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run team join {ns}.ffa @s
execute unless data storage {ns}:multiplayer game{{gamemode:"ffa"}} unless score @s {ns}.mp.team matches 1.. run function {ns}:v{version}/multiplayer/auto_assign_team
""",
	f"{ns}:v{version}/multiplayer/respawn_tp",
	"joined the game!",
	"yellow",
	allow_preparing=True,
	setup_extra_lines="attribute @s minecraft:waypoint_receive_range base set 0.0",
))

