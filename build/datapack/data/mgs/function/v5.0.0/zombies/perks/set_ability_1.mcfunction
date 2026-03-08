
#> mgs:v5.0.0/zombies/perks/set_ability_1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

scoreboard players set @s mgs.zb.ability 1
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.ability_set","color":"gray"},{"translate": "mgs.coward","color":"yellow"},{"translate": "mgs.tp_to_spawn_when_below_50_hp","color":"gray"}]

