
#> mgs:v5.0.0/zombies/pap/pap_chat_message
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.machine","color":"gray"},{"storage":"mgs:temp","nbt":"_pap_machine.name","color":"gold","italic":false,"interpret":true},[{"text":"\n","color":"gray"}, {"translate":"mgs.level"}],{"score":{"name":"#pap_next","objective":"mgs.data"},"color":"aqua"},{"text":"/","color":"dark_gray"},{"score":{"name":"#pap_max","objective":"mgs.data"},"color":"aqua"},[{"text":"  ","color":"gray"}, {"translate":"mgs.cost"}, ": -"],{"score":{"name":"#pap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]]
tellraw @s [{"translate":"mgs.weapon_stats","color":"gray","italic":true}]
execute store result score #pap_lore_len mgs.data run data get storage mgs:temp _pap_extract.lore
scoreboard players remove #pap_lore_len mgs.data 2
scoreboard players set #pap_li mgs.data 0
execute if score #pap_li mgs.data < #pap_lore_len mgs.data run function mgs:v5.0.0/zombies/pap/pap_chat_lore_loop

