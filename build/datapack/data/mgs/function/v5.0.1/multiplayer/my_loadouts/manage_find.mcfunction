
#> mgs:v5.0.1/multiplayer/my_loadouts/manage_find
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/my_loadouts/manage
#			mgs:v5.0.1/multiplayer/my_loadouts/manage_find
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _find_iter[0].id
execute store result score #entry_owner mgs.data run data get storage mgs:temp _find_iter[0].owner_pid
execute if score #entry_id mgs.data = #loadout_id mgs.data if score #entry_owner mgs.data = @s mgs.mp.pid run return run function mgs:v5.0.1/multiplayer/my_loadouts/manage_prep
data remove storage mgs:temp _find_iter[0]
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.0.1/multiplayer/my_loadouts/manage_find

