
#> mgs:v5.2.0/zombies/perks/set_ability_1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/config/process
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.ability 1
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ability_set","fallback":"Ability set: ","color":"gray"},{"translate":"mgs.coward","fallback":"Coward","color":"yellow"},{"translate":"mgs.tp_to_spawn_when_below_50_hp","fallback":" (TP to spawn when below 50% HP)","color":"gray"}]

