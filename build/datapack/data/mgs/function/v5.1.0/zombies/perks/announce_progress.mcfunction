
#> mgs:v5.1.0/zombies/perks/announce_progress
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/on_right_click
#

function mgs:v5.1.0/zombies/perks/get_hover_name
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"🥤 ","color":"dark_purple"},{"storage":"mgs:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true},{"text":": ","color":"gray"},{"score":{"name":"#pk_paid","objective":"mgs.data"},"color":"green"},{"text":"/","color":"gray"},{"score":{"name":"#pk_total","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_paid"}]]
playsound minecraft:block.note_block.pling ambient @s ~ ~ ~ 0.8 1.45

