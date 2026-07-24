
#> mgs:v5.1.0/zombies/wallbuys/deny_equipment_full
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/refill_lethal
#			mgs:v5.1.0/zombies/wallbuys/refill_tactical
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.your_equipment_is_already_full","color":"yellow"}]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

