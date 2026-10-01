
#> mgs:v5.1.0/zombies/perks/trigger_guardian
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/check_guardian [ at @s ]
#

summon minecraft:iron_golem ~ ~ ~ {Tags:["mgs.guardian_golem","mgs.gm_entity"],PlayerCreated:0b,CustomName:{"translate":"mgs.guardian","color":"green"}}

scoreboard players set @s mgs.zb.ability_cd 1

title @s actionbar [{"text":"🛡 ","color":"white"},{"translate":"mgs.guardian_activated_iron_golem_summoned","color":"green"}]

