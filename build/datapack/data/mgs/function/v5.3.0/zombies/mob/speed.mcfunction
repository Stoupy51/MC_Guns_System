
#> mgs:v5.3.0/zombies/mob/speed
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#

execute if entity @s[type=minecraft:wolf] run return run function mgs:v5.3.0/zombies/mob/speed/hound
execute if score #zb_round mgs.data matches ..1 run attribute @s minecraft:movement_speed base set 0.2
execute if score #zb_round mgs.data matches 2 run attribute @s minecraft:movement_speed base set 0.21
execute if score #zb_round mgs.data matches 3 run attribute @s minecraft:movement_speed base set 0.22
execute if score #zb_round mgs.data matches 4 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round mgs.data matches 5 run attribute @s minecraft:movement_speed base set 0.24
execute if score #zb_round mgs.data matches 6 run attribute @s minecraft:movement_speed base set 0.25
execute if score #zb_round mgs.data matches 7 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_round mgs.data matches 8 run attribute @s minecraft:movement_speed base set 0.27
execute if score #zb_round mgs.data matches 9 run attribute @s minecraft:movement_speed base set 0.28
execute if score #zb_round mgs.data matches 10 run attribute @s minecraft:movement_speed base set 0.29
execute if score #zb_round mgs.data matches 11..29 run attribute @s minecraft:movement_speed base set 0.3
execute if score #zb_round mgs.data matches 30..35 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round mgs.data matches 36.. run attribute @s minecraft:movement_speed base set 0.32

# Speed 0.29+ is the BO2 sprint gait, which screams (3-5 s clips) instead of groaning (see vocals).
execute if score #zb_round mgs.data matches 10.. run tag @s add mgs.zb_sprint

# From round 15, 10% are walkers (0.20); never a Zonweeb type, whose speed is a factor of the round's.
scoreboard players set #zb_speed_roll mgs.data 0
execute if score #zb_round mgs.data matches 15.. if score #zb_type mgs.data matches 0 store result score #zb_speed_roll mgs.data run random value 1..10
execute if score #zb_speed_roll mgs.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_speed_roll mgs.data matches 1 run tag @s remove mgs.zb_sprint

