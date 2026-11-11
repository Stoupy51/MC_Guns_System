
#> mgs:v5.4.2/multiplayer/kill_cam/chain_step
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/resolve_chain
#			mgs:v5.4.2/multiplayer/kill_cam/chain_step
#

execute store result score #kc_t mgs.data run data get storage mgs:temp _kc_walk[-1].t
execute if score #kc_t mgs.data < #kc_oldest mgs.data run return 0
execute store result score #kc_victim mgs.data run data get storage mgs:temp _kc_walk[-1].victim
execute if score #kc_victim mgs.data = #kc_killer mgs.data run return 0

# An absent killer reads as 0, which no bs.id is.
execute store result score #kc_by mgs.data run data get storage mgs:temp _kc_walk[-1].killer
scoreboard players operation #kc_gap mgs.data = #kc_chain_start mgs.data
scoreboard players operation #kc_gap mgs.data -= #kc_t mgs.data
execute if score #kc_by mgs.data = #kc_killer mgs.data if score #kc_gap mgs.data matches 81.. run return 0
execute if score #kc_by mgs.data = #kc_killer mgs.data run scoreboard players add #kc_chain_len mgs.data 1
execute if score #kc_by mgs.data = #kc_killer mgs.data run scoreboard players operation #kc_chain_start mgs.data = #kc_t mgs.data
execute if score #kc_chain_len mgs.data matches 6.. run return 0

data remove storage mgs:temp _kc_walk[-1]
execute if data storage mgs:temp _kc_walk[0] run function mgs:v5.4.2/multiplayer/kill_cam/chain_step

