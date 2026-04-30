
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function


def generate_teams() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Join Teams
	write_versioned_function("multiplayer/join_red", f"""
scoreboard players set @s {ns}.mp.team 1
team join {ns}.red @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Red Team","color":"red","bold":true}}]
""")

	write_versioned_function("multiplayer/join_blue", f"""
scoreboard players set @s {ns}.mp.team 2
team join {ns}.blue @s
tellraw @s ["",{{"text":"You joined ","color":"white"}},{{"text":"Blue Team","color":"blue","bold":true}}]
""")

	write_versioned_function("multiplayer/auto_assign_team", f"""
# Count players on each team
execute store result score #red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]

# Assign to team with fewer players (red if tied)
execute if score #red_count {ns}.data <= #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_red
execute if score #red_count {ns}.data > #blue_count {ns}.data run function {ns}:v{version}/multiplayer/join_blue
""")

	## Show Team Roster
	sep = '{"text":"============================================","color":"dark_gray"}'
	write_versioned_function("multiplayer/show_teams", f"""
tellraw @s {sep}
tellraw @s ["",["","  👥 ",{{"text":"Team Roster","bold":true}}]]
tellraw @s {sep}
execute store result score #team_red_count {ns}.data if entity @a[scores={{{ns}.mp.team=1}}]
execute store result score #team_blue_count {ns}.data if entity @a[scores={{{ns}.mp.team=2}}]
execute store result score #team_total {ns}.data if entity @a[scores={{{ns}.mp.team=1..}}]
tellraw @s ["",{{"text":"  Red Team","color":"red","bold":true}},{{"text":" ("}},{{"score":{{"name":"#team_red_count","objective":"{ns}.data"}}}},{{"text":")"}},{{"text":": "}},{{"selector":"@a[scores={{{ns}.mp.team=1}}]","color":"red"}}]
tellraw @s ["",{{"text":"  Blue Team","color":"blue","bold":true}},{{"text":" ("}},{{"score":{{"name":"#team_blue_count","objective":"{ns}.data"}}}},{{"text":")"}},{{"text":": "}},{{"selector":"@a[scores={{{ns}.mp.team=2}}]","color":"blue"}}]
execute unless score #team_total {ns}.data matches 1.. run tellraw @s ["  ",{{"text":"⚠ No players have joined a team yet!","color":"yellow"}}]
tellraw @s {sep}
""")  # noqa: E501

	## Team Setup (load)
	write_load_file(
f"""
# Create teams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red color red
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red friendlyFire true
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.red nametagVisibility hideForOtherTeams
execute unless score #mp_teams_created {ns}.data matches 1 run team add {ns}.blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue color blue
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue friendlyFire true
execute unless score #mp_teams_created {ns}.data matches 1 run team modify {ns}.blue nametagVisibility hideForOtherTeams
scoreboard players set #mp_teams_created {ns}.data 1
""")

