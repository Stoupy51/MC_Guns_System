
#> mgs:v5.1.0/zombies/pap/anim/retreat_finish
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/step
#

kill @e[tag=mgs.pap_weapon_display,distance=..2]

scoreboard players set @s mgs.pap_anim -1

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_weapon_was_lost","color":"red","bold":true}]
playsound mgs:zombies/pap/deny ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

execute store result score #pap_mid mgs.data run scoreboard players get @s mgs.zb.pap.id
execute store result storage mgs:temp _pap_retreat.id int 1 run scoreboard players get @s mgs.zb.pap.id
function mgs:v5.1.0/zombies/pap/retreat_cleanup with storage mgs:temp _pap_retreat

