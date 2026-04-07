
# Imports
pass

# Functions
def respawn_countdown_tick_lines(ns: str, mode_prefix: str, actual_respawn_function: str) -> str:
	""" Build shared 3->2->1 spectator respawn countdown commands. """
	return f"""
# Spectate Timer (3s respawn cooldown)
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=1..}}] run scoreboard players remove @s {ns}.mp.spectate_timer 1
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=40}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 2 seconds...","color":"gray"}}]
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=20}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 1 second...","color":"gray"}}]
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=0}},gamemode=spectator] at @s run function {actual_respawn_function}
""".strip()

