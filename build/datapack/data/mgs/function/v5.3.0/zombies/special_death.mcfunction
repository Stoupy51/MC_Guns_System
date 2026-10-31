
#> mgs:v5.3.0/zombies/special_death
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/on_zombie_dying
#

tag @s remove mgs.zombie_round

scoreboard players operation #zb_special_left mgs.data = #zb_portal_pending mgs.data
scoreboard players operation #zb_special_left mgs.data += #zb_to_spawn mgs.data
execute store result score #zb_special_alive mgs.data if entity @e[tag=mgs.zombie_round]
scoreboard players operation #zb_special_left mgs.data += #zb_special_alive mgs.data

# ammo_done also covers two enemies dying in the same tick.
execute if score #zb_special_left mgs.data matches ..0 if score #zb_special_ammo_done mgs.data matches 0 run function mgs:v5.3.0/zombies/special_max_ammo

