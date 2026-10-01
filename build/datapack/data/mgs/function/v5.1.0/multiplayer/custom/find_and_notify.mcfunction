
#> mgs:v5.1.0/multiplayer/custom/find_and_notify
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/custom/select
#			mgs:v5.1.0/multiplayer/custom/find_and_notify
#

execute store result score #entry_id mgs.data run data get storage mgs:temp _find_iter[0].id
execute if score #entry_id mgs.data = #loadout_id mgs.data run return run function mgs:v5.1.0/multiplayer/custom/notify_selected with storage mgs:temp _find_iter[0]

data remove storage mgs:temp _find_iter[0]
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.1.0/multiplayer/custom/find_and_notify

