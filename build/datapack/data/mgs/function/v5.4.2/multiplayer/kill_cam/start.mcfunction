
#> mgs:v5.4.2/multiplayer/kill_cam/start
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/end
#

# A Search and Destroy wipe ends on its last death, logged on the deciding tick.
execute if data storage mgs:multiplayer game{gamemode:"snd"} store result score #kc_t mgs.data run data get storage mgs:kill_cam deaths[-1].t
execute if data storage mgs:multiplayer game{gamemode:"snd"} if score #kc_t mgs.data = #mp_end_tick mgs.data run scoreboard players set #kc_final mgs.data 2
execute unless score #kc_final mgs.data matches 2 run return fail
execute unless data storage mgs:kill_cam deaths[-1].killer run return fail
execute unless data storage mgs:kill_cam frames[0] run return fail
scoreboard players set #kc_window mgs.data 0

function mgs:v5.4.2/multiplayer/kill_cam/resolve_chain

# From PRE_ROLL before the first kill, and never on a frame without the killer: the camera is their eyes.
scoreboard players operation #kc_cut mgs.data = #kc_chain_start mgs.data
scoreboard players remove #kc_cut mgs.data 40
function mgs:v5.4.2/multiplayer/kill_cam/drop_early_frames
execute store result storage mgs:temp _kc.killer int 1 run scoreboard players get #kc_killer mgs.data
function mgs:v5.4.2/multiplayer/kill_cam/drop_frames_without_killer with storage mgs:temp _kc
execute unless data storage mgs:kill_cam frames[0] run return fail
execute store result score #kc_oldest mgs.data run data get storage mgs:kill_cam frames[0].t
execute if data storage mgs:kill_cam deaths[0] run function mgs:v5.4.2/multiplayer/kill_cam/trim_deaths

tag @a[scores={mgs.mp.in_game=1}] add mgs.kc_viewer
execute as @a[tag=mgs.kc_viewer] if score @s bs.id = #kc_killer mgs.data run tag @s add mgs.kc_killer
execute unless entity 006d6773-0000-0000-0000-000000006b63 at @r[tag=mgs.kc_viewer] run function mgs:v5.4.2/multiplayer/kill_cam/summon_probe
function mgs:v5.4.2/multiplayer/kill_cam/place_camera with storage mgs:temp _kc
execute as @a[tag=mgs.kc_viewer] at @s run function mgs:v5.4.2/multiplayer/kill_cam/add_viewer

title @a[tag=mgs.kc_viewer] times 5 30 10
title @a[tag=mgs.kc_viewer] title {"translate":"mgs.killcam","fallback":"KILLCAM","bold":true}
title @a[tag=mgs.kc_viewer] subtitle [["",{"text":"[","color":"dark_gray"},{"score":{"name":"@a[tag=mgs.kc_killer]","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@a[tag=mgs.kc_killer]"}],{"text":" x","color":"gold"},{"score":{"name":"#kc_chain_len","objective":"mgs.data"},"color":"gold"}]

scoreboard players set #kc_hold mgs.data 20
scoreboard players operation #kc_end_t mgs.data = #kc_final_t mgs.data
scoreboard players add #kc_end_t mgs.data 30
return 1

