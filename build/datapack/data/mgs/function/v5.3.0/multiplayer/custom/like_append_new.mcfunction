
#> mgs:v5.3.0/multiplayer/custom/like_append_new
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/custom/like_modify_entry
#

data modify storage mgs:temp _new_liked set value {id:0}
execute store result storage mgs:temp _new_liked.id int 1 run scoreboard players get #loadout_id mgs.data
data modify storage mgs:temp _pd_src[0].liked append from storage mgs:temp _new_liked

