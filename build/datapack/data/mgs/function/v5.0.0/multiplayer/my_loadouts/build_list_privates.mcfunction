
#> mgs:v5.0.0/multiplayer/my_loadouts/build_list_privates
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/browse
#			mgs:v5.0.0/multiplayer/my_loadouts/build_list_privates
#

execute store result score #entry_owner mgs.data run data get storage mgs:temp _iter[0].owner_pid
execute if score #entry_owner mgs.data = @s mgs.mp.pid run function mgs:v5.0.0/multiplayer/my_loadouts/check_private_not_fav

data remove storage mgs:temp _iter[0]
execute if data storage mgs:temp _iter[0] run function mgs:v5.0.0/multiplayer/my_loadouts/build_list_privates

