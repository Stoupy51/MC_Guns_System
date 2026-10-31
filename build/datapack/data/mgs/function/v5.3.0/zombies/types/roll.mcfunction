
#> mgs:v5.3.0/zombies/types/roll
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#

execute store result score #zb_type_roll mgs.data run random value 1..100
execute if score #zb_type_roll mgs.data matches 1..15 if score #zb_round mgs.data matches 5.. run scoreboard players set #zb_type mgs.data 1
execute if score #zb_type_roll mgs.data matches 16..23 if score #zb_round mgs.data matches 10.. run scoreboard players set #zb_type mgs.data 2
execute if score #zb_type_roll mgs.data matches 24..28 if score #zb_round mgs.data matches 15.. run scoreboard players set #zb_type mgs.data 3
execute if score #zb_type_roll mgs.data matches 29..31 if score #zb_round mgs.data matches 20.. unless entity @e[type=minecraft:zombie,tag=mgs.zb_aura,limit=1] run scoreboard players set #zb_type mgs.data 4

