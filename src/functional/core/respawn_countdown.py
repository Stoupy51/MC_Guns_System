""" Shared respawn countdown lines, reused by every mode's respawn flow. """

# Functions
def respawn_countdown_tick_lines(ns: str, mode_prefix: str, actual_respawn_function: str) -> str:
	""" Build shared 3->2->1 spectator respawn countdown commands. """
	return f"""
# 3 s respawn countdown in real time; range checks, since a 2+ tick delta can jump over an exact 0.
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=1..}}] run scoreboard players operation @s {ns}.mp.spectate_timer -= #tick_delta {ns}.data
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=21..40}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 2 seconds...","color":"gray"}}]
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=1..20}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 1 second...","color":"gray"}}]
# The countdown subtitle is cleared: Minecraft keeps the last subtitle, so a later `title` would show "Respawning in 1 second..." under it.
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=..0}},gamemode=spectator] run title @s subtitle {{"text":""}}
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=..0}},gamemode=spectator] at @s run function {actual_respawn_function}
""".strip()

