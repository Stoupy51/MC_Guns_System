
#> mgs:v5.3.0/zombies/spawn_setup
#
# @executed	as @n[type=minecraft:marker,tag=mgs.new_spawn]
#
# @within	mgs:v5.3.0/zombies/summon_spawn_iter [ as @n[type=minecraft:marker,tag=mgs.new_spawn] ]
#

tag @s remove mgs.new_spawn
scoreboard players operation @s mgs.zb.spawn.sid = #zb_spawn_sid mgs.data
execute store result score @s mgs.zb.spawn.gid run data get storage mgs:temp _spawn.group_id

data modify entity @s data.mob set from storage mgs:temp _spawn.mob
execute if data storage mgs:temp _spawn{arrival:"floor"} run tag @s add mgs.arrive_floor
execute if data storage mgs:temp _spawn{arrival:"ceiling"} run tag @s add mgs.arrive_ceiling
execute if data storage mgs:temp _spawn{arrival:"portal"} run tag @s add mgs.arrive_portal
execute if data storage mgs:temp _spawn{arrival:"instant"} run tag @s add mgs.arrive_instant
execute store result score @s mgs.zb.rise_tick run data get storage mgs:temp _spawn.rise_ticks
execute if score @s mgs.zb.rise_tick matches ..0 run scoreboard players set @s mgs.zb.rise_tick 1

# [x, y, z, dx, dy, dz] from the spawn (all 6 needed): only usable while an alive player stands in it (see check_boxes).
execute if data storage mgs:temp _spawn.activation_box[5] run function mgs:v5.3.0/zombies/store_spawn_abox
execute unless data storage mgs:temp _spawn.activation_box[5] run tag @s add mgs.spawn_abox_ok

# Enemies of this spawn are escorted to this spot.
execute if data storage mgs:temp _spawn.walk_to[2] run function mgs:v5.3.0/zombies/store_spawn_walk_to

# Bounds are checked at each round start (see check_rounds); max_round 0 never ends.
execute store result score @s mgs.zb.spawn.rmin run data get storage mgs:temp _spawn.min_round
execute store result score @s mgs.zb.spawn.rmax run data get storage mgs:temp _spawn.max_round
execute if score @s mgs.zb.spawn.rmin matches ..0 if score @s mgs.zb.spawn.rmax matches ..0 run tag @s add mgs.spawn_round_ok
execute unless entity @s[tag=mgs.spawn_round_ok] run tag @s add mgs.spawn_ranged
execute if score @s mgs.zb.spawn.rmax matches ..0 run scoreboard players set @s mgs.zb.spawn.rmax 2147483647

# Switched on with the power (see power/on_activate).
execute store result score #zb_spawn_power mgs.data run data get storage mgs:temp _spawn.power
execute unless score #zb_spawn_power mgs.data matches 1.. run tag @s add mgs.spawn_powered

