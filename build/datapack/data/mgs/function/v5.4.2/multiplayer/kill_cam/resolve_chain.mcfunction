
#> mgs:v5.4.2/multiplayer/kill_cam/resolve_chain
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/start
#

execute store result score #kc_killer mgs.data run data get storage mgs:kill_cam deaths[-1].killer
execute store result score #kc_final_t mgs.data run data get storage mgs:kill_cam deaths[-1].t
execute store result score #kc_oldest mgs.data run data get storage mgs:kill_cam frames[0].t
scoreboard players set #kc_chain_len mgs.data 1
scoreboard players operation #kc_chain_start mgs.data = #kc_final_t mgs.data

data modify storage mgs:temp _kc_walk set from storage mgs:kill_cam deaths
data remove storage mgs:temp _kc_walk[-1]
execute if data storage mgs:temp _kc_walk[0] run function mgs:v5.4.2/multiplayer/kill_cam/chain_step
data remove storage mgs:temp _kc_walk

