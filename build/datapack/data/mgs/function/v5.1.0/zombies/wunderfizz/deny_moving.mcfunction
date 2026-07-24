
#> mgs:v5.1.0/zombies/wunderfizz/deny_moving
#
# @executed	as @n[tag=mgs.wf_new]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_is_moving","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

