
#> mgs:v5.0.0/multiplayer/custom/find_and_apply
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/select
#			mgs:v5.0.0/multiplayer/custom/find_and_apply
#

# Check if this entry's ID matches the target
execute store result score #entry_id mgs.data run data get storage mgs:temp _find_iter[0].id
execute if score #entry_id mgs.data = #loadout_id mgs.data run return run function mgs:v5.0.0/multiplayer/custom/apply_found

# Not found yet, continue search
data remove storage mgs:temp _find_iter[0]
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.0.0/multiplayer/custom/find_and_apply

