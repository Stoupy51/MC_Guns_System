""" Team assignment and the red/blue team definitions. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def generate_teams() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Picking a team also opts the player in: in_game is the "joined" flag.
	write_versioned_function("multiplayer/join_red", f"""
scoreboard players set @s {ns}.mp.team 1
scoreboard players set @s {ns}.mp.in_game 1
team join {ns}.red @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Red Team","color":"red","bold":true}}]
""")

	write_versioned_function("multiplayer/join_blue", f"""
scoreboard players set @s {ns}.mp.team 2
scoreboard players set @s {ns}.mp.in_game 1
team join {ns}.blue @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Blue Team","color":"blue","bold":true}}]
""")

	## FFA has no sides: everyone shares the yellow {ns}.ffa team (friendly fire on, no nametags), as at game start.
	## mp.team is 0, so spawns, team scores and the end announce never treat an FFA player as red or blue.
	write_versioned_function("multiplayer/join_ffa", f"""
scoreboard players set @s {ns}.mp.team 0
scoreboard players set @s {ns}.mp.in_game 1
team join {ns}.ffa @s
tellraw @s ["",{{"text":"You joined the ","color":"white"}},{{"text":"Free For All","color":"yellow","bold":true}}]
""")

	write_versioned_function("multiplayer/auto_assign_team", f"""
# FFA: everyone goes to the single FFA team instead of being split red and blue.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run return run function {ns}:v{version}/multiplayer/join_ffa

execute store result score #red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]

# The player's own team does not count, so re-running auto-assign stays stable instead of clumping onto one side.
execute if score @s {ns}.mp.team matches 1 run scoreboard players remove #red_count {ns}.data 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players remove #blue_count {ns}.data 1

# The smaller team, red when tied.
execute if score #red_count {ns}.data <= #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_red
execute if score #red_count {ns}.data > #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_blue
""")

