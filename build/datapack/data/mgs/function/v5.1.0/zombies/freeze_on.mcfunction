
#> mgs:v5.1.0/zombies/freeze_on
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/freeze_toggle
#

scoreboard players set #zb_freeze mgs.data 1

# Mobs: only the ones actually moving right now
execute as @e[tag=mgs.zombie_round] unless data entity @s {NoAI:1b} run function mgs:v5.1.0/zombies/freeze_mob

# Players: same attribute pair the prep countdown uses to hold everyone still
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0

title @a[scores={mgs.zb.in_game=1}] times 5 60 10
title @a[scores={mgs.zb.in_game=1}] title [{"text":"⏸","color":"aqua"}]
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_froze_the_game","color":"aqua"}]

