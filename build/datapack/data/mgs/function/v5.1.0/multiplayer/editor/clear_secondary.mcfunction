
#> mgs:v5.1.0/multiplayer/editor/clear_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/remove_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_perk
#

data modify storage mgs:temp editor merge value {secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:""}

