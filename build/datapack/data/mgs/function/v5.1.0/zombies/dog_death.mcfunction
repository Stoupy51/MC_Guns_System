
#> mgs:v5.1.0/zombies/dog_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/on_zombie_dying
#

tag @s remove mgs.zb_dog

scoreboard players operation #zb_dog_left mgs.data = #zb_dog_pending mgs.data
scoreboard players operation #zb_dog_left mgs.data += #zb_to_spawn mgs.data
execute store result score #zb_dog_alive mgs.data if entity @e[tag=mgs.zb_dog]
scoreboard players operation #zb_dog_left mgs.data += #zb_dog_alive mgs.data

# ammo_done also covers the same-tick case: two hounds dying together both see the pack empty.
execute if score #zb_dog_left mgs.data matches ..0 if score #zb_dog_ammo_done mgs.data matches 0 run function mgs:v5.1.0/zombies/dog_max_ammo_at_self

