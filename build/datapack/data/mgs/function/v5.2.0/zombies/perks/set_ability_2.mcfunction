
#> mgs:v5.2.0/zombies/perks/set_ability_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/config/process
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set @s mgs.zb.ability 2
scoreboard players set @s mgs.zb.ability_cd 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.ability_set","fallback":"Ability set: ","color":"gray"},{"translate":"mgs.guardian","fallback":"Guardian","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.summon_an_iron_golem_ally","fallback":"(Summon an Iron Golem ally)"}]]

