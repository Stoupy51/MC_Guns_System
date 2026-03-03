
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


def generate_teams() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Join Teams
	## ============================
	write_versioned_function("multiplayer/join_red",
f"""
scoreboard players set @s {ns}.mp.team 1
team join {ns}.red @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Red Team","color":"red","bold":true}}]
""")

	write_versioned_function("multiplayer/join_blue",
f"""
scoreboard players set @s {ns}.mp.team 2
team join {ns}.blue @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Blue Team","color":"blue","bold":true}}]
""")

	write_versioned_function("multiplayer/auto_assign_team",
f"""
# Count players on each team
execute store result score #red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]

# Assign to team with fewer players (red if tied)
execute if score #red_count {ns}.data <= #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_red
execute if score #red_count {ns}.data > #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_blue
""")

	## ============================
	## Team Setup (load)
	## ============================
	write_load_file(
f"""
# Create teams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red color red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red friendlyFire false
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red nametagVisibility hideForOtherTeams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue color blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue friendlyFire false
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue nametagVisibility hideForOtherTeams
scoreboard players set #mp_teams_created {ns}.data 1
""")

