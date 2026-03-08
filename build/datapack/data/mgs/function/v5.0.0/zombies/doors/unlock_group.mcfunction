
#> mgs:v5.0.0/zombies/doors/unlock_group
#
# @executed	as @e[tag=mgs.door] & at @s
#
# @within	mgs:v5.0.0/zombies/doors/open_one with storage mgs:temp _door_unlock
#			mgs:v5.0.0/zombies/doors/unlock_back_group with storage mgs:temp _door_unlock
#
# @args		gid (unknown)
#

$data modify storage mgs:zombies game.unlocked_groups."$(gid)" set value 1b

# Tag spawn markers with matching group_id as unlocked
$scoreboard players set #_unlock_gid mgs.data $(gid)
execute as @e[tag=mgs.spawn_point] if score @s mgs.zb.spawn.gid = #_unlock_gid mgs.data run tag @s add mgs.spawn_unlocked

