
#> mgs:v5.3.0/maps/compact/leaderboard
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.3.0/maps/editor/save_zb_object
#

data remove storage mgs:temp _save_zb.group_id
data remove storage mgs:temp _save_zb.yaw
execute if data storage mgs:temp _save_zb{board:"level_zb"} run data remove storage mgs:temp _save_zb.board
execute if data storage mgs:temp _save_zb{map_id:""} run data remove storage mgs:temp _save_zb.map_id
execute if data storage mgs:temp _save_zb{players:"all"} run data remove storage mgs:temp _save_zb.players
data modify storage mgs:temp map_edit.map.leaderboards append from storage mgs:temp _save_zb

