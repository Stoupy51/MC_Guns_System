
# Imports
pass

# Functions
def respawn_countdown_tick_lines(ns: str, mode_prefix: str, actual_respawn_function: str) -> str:
	""" Build shared 3->2->1 spectator respawn countdown commands. """
	return f"""
# Spectate Timer (3s respawn cooldown, real-time via #tick_delta).
# Range checks instead of exact values: a 2+ tick delta under lag can jump over any single value
# (an exact =0 respawn check would then never fire)
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=1..}}] run scoreboard players operation @s {ns}.mp.spectate_timer -= #tick_delta {ns}.data
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=21..40}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 2 seconds...","color":"gray"}}]
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=1..20}},gamemode=spectator] run title @s subtitle [{{"text":"Respawning in 1 second...","color":"gray"}}]
# Clear the countdown subtitle on respawn: Minecraft keeps the last subtitle until something
# replaces it, so any later `title` (a round banner, the hit indicator) would redisplay a stale
# "Respawning in 1 second..." underneath it.
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=..0}},gamemode=spectator] run title @s subtitle {{"text":""}}
execute as @a[scores={{{ns}.{mode_prefix}.in_game=1,{ns}.mp.spectate_timer=..0}},gamemode=spectator] at @s run function {actual_respawn_function}
""".strip()

