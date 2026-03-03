
#> mgs:v5.0.0/multiplayer/custom/fav_append_new
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/fav_modify_entry
#

# Create a new favorite entry with the loadout ID
data modify storage mgs:temp _new_fav set value {id:0}
execute store result storage mgs:temp _new_fav.id int 1 run scoreboard players get #loadout_id mgs.data
data modify storage mgs:temp _pd_src[0].favorites append from storage mgs:temp _new_fav

