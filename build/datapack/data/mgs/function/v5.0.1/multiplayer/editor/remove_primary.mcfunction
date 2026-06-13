
#> mgs:v5.0.1/multiplayer/editor/remove_primary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

data modify storage mgs:temp editor merge value {primary:"",primary_name:"None",primary_mag:"",primary_mag_count:1,primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:""}
function mgs:v5.0.1/multiplayer/editor/hub

