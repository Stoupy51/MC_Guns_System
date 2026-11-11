
#> mgs:v5.4.2/multiplayer/kill_cam/tick
#
# @within	mgs:v5.4.2/tick
#			mgs:v5.4.2/dialog/close_then
#

execute unless score #in_multiplayer_map mgs.data matches 1 run return run function mgs:v5.4.2/shared/enter_map {mode:"multiplayer",fn:"mgs:v5.4.2/multiplayer/kill_cam/tick"}

# Sneaking stops spectating, so every viewer is put back on the camera; setCamera ignores the camera a viewer already has.
execute as @a[tag=mgs.kc_viewer] run spectate @n[type=minecraft:item_display,tag=mgs.kc_camera] @s
execute if score #kc_hold mgs.data matches 1.. run return run scoreboard players remove #kc_hold mgs.data 1
execute unless data storage mgs:kill_cam frames[0] run return run function mgs:v5.4.2/multiplayer/kill_cam/post_roll

data modify storage mgs:kill_cam frame set from storage mgs:kill_cam frames[0]
data remove storage mgs:kill_cam frames[0]
execute store result score #kc_now mgs.data run data get storage mgs:kill_cam frame.t

execute unless entity 006d6773-0000-0000-0000-000000006b63 at @n[type=minecraft:item_display,tag=mgs.kc_camera] run function mgs:v5.4.2/multiplayer/kill_cam/summon_probe
execute if data storage mgs:kill_cam frame.s[0] run function mgs:v5.4.2/multiplayer/kill_cam/play_sample

# After the samples, as a death outside the function tick (a command, an advancement reward) comes after its tick's frame.
# Before the vanish, so the victim falls on screen.
execute if data storage mgs:kill_cam deaths[0] run function mgs:v5.4.2/multiplayer/kill_cam/play_deaths
execute as @e[type=minecraft:mannequin,tag=mgs.kc_puppet,tag=!mgs.kc_seen] at @s run function mgs:v5.4.2/multiplayer/kill_cam/vanish
tag @e[type=minecraft:mannequin,tag=mgs.kc_seen] remove mgs.kc_seen
execute if data storage mgs:kill_cam frame.shots[0] run function mgs:v5.4.2/multiplayer/kill_cam/play_shot

