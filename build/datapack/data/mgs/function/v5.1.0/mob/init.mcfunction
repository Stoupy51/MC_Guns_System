
#> mgs:v5.1.0/mob/init
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.1.0/mob/tick
#

tag @s add mgs.mob_init

# 50 ticks unless set.
execute unless score @s mgs.mob.active_time matches 1.. run scoreboard players set @s mgs.mob.active_time 50

# 100 ticks unless set.
execute unless score @s mgs.mob.sleep_time matches 0.. run scoreboard players set @s mgs.mob.sleep_time 100

# 1 s.
scoreboard players set @s mgs.cooldown 20

function mgs:v5.1.0/mob/wake_up

