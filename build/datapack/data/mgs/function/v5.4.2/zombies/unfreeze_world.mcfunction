
#> mgs:v5.4.2/zombies/unfreeze_world
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/freeze_off
#			mgs:v5.4.2/zombies/resume
#

scoreboard players set #zb_freeze mgs.data 0
scoreboard players set #zb_resume_timer mgs.data 0

# Only the mobs freeze_world put to sleep.
execute as @e[tag=mgs.zb_frozen_ai] run data merge entity @s {NoAI:0b}
tag @e[tag=mgs.zb_frozen_ai] remove mgs.zb_frozen_ai

execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base reset

