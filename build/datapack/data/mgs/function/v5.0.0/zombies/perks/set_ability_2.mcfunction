
#> mgs:v5.0.0/zombies/perks/set_ability_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

scoreboard players set @s mgs.zb.ability 2
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.ability_set","color":"gray"},{"translate": "mgs.guardian","color":"green"},{"translate": "mgs.summon_an_iron_golem_ally","color":"gray"}]

