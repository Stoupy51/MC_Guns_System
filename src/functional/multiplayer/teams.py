
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

	## Free-for-all has no sides: everyone shares the {ns}.ffa team (yellow, friendly fire on, no
	## nametags) — the same team game start puts them on. mp.team is cleared to 0 so nothing downstream
	## treats an FFA player as red/blue (spawn picking, team scores, the end-of-game team announce).
	write_versioned_function("multiplayer/join_ffa", f"""
scoreboard players set @s {ns}.mp.team 0
scoreboard players set @s {ns}.mp.in_game 1
team join {ns}.ffa @s
tellraw @s ["",{{"text":"You joined the ","color":"white"}},{{"text":"Free For All","color":"yellow","bold":true}}]
""")

	write_versioned_function("multiplayer/auto_assign_team", f"""
# In FFA there are no sides to balance — put everyone on the single FFA team instead of splitting
# them red/blue, which implied alliances that don't exist and sent them to opposing spawns.
execute if data storage {ns}:multiplayer game{{gamemode:"ffa"}} run return run function {ns}:v{version}/multiplayer/join_ffa

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
