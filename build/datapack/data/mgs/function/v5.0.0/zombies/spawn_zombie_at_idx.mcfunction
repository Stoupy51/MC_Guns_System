
#> mgs:v5.0.0/zombies/spawn_zombie_at_idx
#
# @within	mgs:v5.0.0/zombies/spawn_zombie
#			mgs:v5.0.0/zombies/spawn_zombie_at_idx
#

execute if score #_zs_idx mgs.data matches 1.. run data remove storage mgs:temp _zs_iter[0]
execute if score #_zs_idx mgs.data matches 1.. run scoreboard players remove #_zs_idx mgs.data 1
execute if score #_zs_idx mgs.data matches 1.. run function mgs:v5.0.0/zombies/spawn_zombie_at_idx

# Now at the right index, read position
execute if score #_zs_idx mgs.data matches 0 run function mgs:v5.0.0/zombies/do_spawn_zombie

