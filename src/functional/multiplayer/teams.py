
# Imports
from stewbeet import Mem, write_versioned_function


def generate_teams() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Join Teams (picking a team also opts the player into the game: in_game is the "joined" flag)
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

	write_versioned_function("multiplayer/auto_assign_team", f"""
# Count players on each team
execute store result score #red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]

# Exclude self from the count so a player never tips the balance toward their own current team
# (otherwise re-running auto-assign on already-assigned players is unstable and clumps onto one side)
execute if score @s {ns}.mp.team matches 1 run scoreboard players remove #red_count {ns}.data 1
execute if score @s {ns}.mp.team matches 2 run scoreboard players remove #blue_count {ns}.data 1

# Assign to team with fewer players (red if tied)
execute if score #red_count {ns}.data <= #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_red
execute if score #red_count {ns}.data > #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_blue
""")
