
#> mgs:v5.0.0/multiplayer/custom/like_append_new
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/like_modify_entry
#

data modify storage mgs:temp _new_liked set value {id:0}
execute store result storage mgs:temp _new_liked.id int 1 run scoreboard players get #loadout_id mgs.data
data modify storage mgs:temp _pd_src[0].liked append from storage mgs:temp _new_liked

