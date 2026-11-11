
#> mgs:v5.4.2/multiplayer/kill_cam/record
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/game_tick
#

data modify storage mgs:kill_cam frames append value {s:[]}
execute store result storage mgs:kill_cam frames[-1].t int 1 run scoreboard players get #total_tick mgs.data
execute if data storage mgs:kill_cam pending_shots[0] run data modify storage mgs:kill_cam frames[-1].shots set from storage mgs:kill_cam pending_shots
data remove storage mgs:kill_cam pending_shots

# The probe stays where the last sample left it, which a player leaving can unload.
execute unless entity 006d6773-0000-0000-0000-000000006b63 at @r[scores={mgs.mp.in_game=1},gamemode=!spectator] run function mgs:v5.4.2/multiplayer/kill_cam/summon_probe
execute as @a[scores={mgs.mp.in_game=1},gamemode=!spectator] at @s run function mgs:v5.4.2/multiplayer/kill_cam/sample

execute if data storage mgs:kill_cam frames[440] run function mgs:v5.4.2/multiplayer/kill_cam/trim

