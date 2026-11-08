
#> mgs:v5.4.1/multiplayer/custom/fav_append_new
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/custom/fav_modify_entry
#

data modify storage mgs:temp _new_fav set value {id:0}
execute store result storage mgs:temp _new_fav.id int 1 run scoreboard players get #loadout_id mgs.data
data modify storage mgs:temp _pd_src[0].favorites append from storage mgs:temp _new_fav

