
#> mgs:v5.1.0/zombies/wunderfizz/deny_requires_power
#
# @executed	as @n[tag=mgs.wf_new]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_der_wunderfizz_requires_power","color":"red"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

