
#> mgs:v5.4.2/weapon/hit_direction
#
# @within	#mgs:signals/damage
#			mgs:v5.4.2/dialog/close_then
#

# Player victims only.
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no direction (hitscan cannot self-hit).
execute if entity @s[tag=mgs.temp_shooter] run return 0

scoreboard players set #hit_src mgs.data 0
execute at @s if entity @n[tag=mgs.ticking] run scoreboard players set #hit_src mgs.data 1
execute at @s if score #hit_src mgs.data matches 0 if entity @n[tag=mgs.temp_shooter] run scoreboard players set #hit_src mgs.data 2
execute if score #hit_src mgs.data matches 0 run return 0

# Yaw toward the shooter (x100) from a scratch marker at the victim facing the shooter.
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["mgs.hit_dir_marker"]}
execute at @s if score #hit_src mgs.data matches 1 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.ticking] eyes
execute at @s if score #hit_src mgs.data matches 2 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.temp_shooter] eyes
execute at @s store result score #hit_dir mgs.data run data get entity @n[tag=mgs.hit_dir_marker] Rotation[0] 100
execute at @s run kill @n[tag=mgs.hit_dir_marker]

# Sector 0..35 from the victim's facing (0 front, clockwise; scoreboard %= is floorMod); the half-sector offset centres each sector on its direction.
execute store result score #hit_yaw mgs.data run data get entity @s Rotation[0] 100
scoreboard players operation #hit_dir mgs.data -= #hit_yaw mgs.data
scoreboard players add #hit_dir mgs.data 500
scoreboard players operation #hit_dir mgs.data %= #36000 mgs.data
scoreboard players operation #hit_dir mgs.data /= #1000 mgs.data

function mgs:v5.4.2/player/hit_dir_show

