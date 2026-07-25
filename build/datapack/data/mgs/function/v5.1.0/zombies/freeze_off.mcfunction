
#> mgs:v5.1.0/zombies/freeze_off
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/admin/freeze_toggle
#

scoreboard players set #zb_freeze mgs.data 0

# Only wake the mobs freeze_on actually put to sleep
execute as @e[tag=mgs.zb_frozen_ai] run data merge entity @s {NoAI:0b}
tag @e[tag=mgs.zb_frozen_ai] remove mgs.zb_frozen_ai

execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base reset

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_unfroze_the_game","color":"aqua"}]

