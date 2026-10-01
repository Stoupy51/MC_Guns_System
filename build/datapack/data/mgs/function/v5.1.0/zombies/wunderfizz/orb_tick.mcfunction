
#> mgs:v5.1.0/zombies/wunderfizz/orb_tick
#
# @executed	as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s ]
#

particle minecraft:end_rod ~ ~ ~ 0.25 0.25 0.25 0.02 1 force @a[distance=..48]
particle minecraft:electric_spark ~ ~0.3 ~ 0.3 0.3 0.3 0.05 1 force @a[distance=..48]

scoreboard players remove @s mgs.zb.wf.anim 1
# Timeslip: 2x spin speed. anim starts even (100), so the extra step lands exactly on 0;
# the ready window still counts down at normal speed.
execute if score @s mgs.zb.wf.timeslip matches 1 if score @s mgs.zb.wf.anim matches 1.. run scoreboard players remove @s mgs.zb.wf.anim 1
execute if score @s mgs.zb.wf.anim matches 1.. run function mgs:v5.1.0/zombies/wunderfizz/spin_cycle
execute if score @s mgs.zb.wf.anim matches 0 run function mgs:v5.1.0/zombies/wunderfizz/land
execute if score @s mgs.zb.wf.anim matches ..-200 run function mgs:v5.1.0/zombies/wunderfizz/orb_expire

