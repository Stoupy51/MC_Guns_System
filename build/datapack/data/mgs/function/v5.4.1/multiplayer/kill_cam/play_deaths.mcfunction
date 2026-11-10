
#> mgs:v5.4.1/multiplayer/kill_cam/play_deaths
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/tick
#			mgs:v5.4.1/multiplayer/kill_cam/play_deaths
#

execute store result score #kc_t mgs.data run data get storage mgs:kill_cam deaths[0].t
execute if score #kc_t mgs.data > #kc_now mgs.data run return 0
execute store result score #kc_sid mgs.data run data get storage mgs:kill_cam deaths[0].victim
kill @e[type=minecraft:mannequin,tag=mgs.kc_puppet,predicate=mgs:v5.4.1/multiplayer/kill_cam/id_match]
data remove storage mgs:kill_cam deaths[0]
execute if data storage mgs:kill_cam deaths[0] run function mgs:v5.4.1/multiplayer/kill_cam/play_deaths

