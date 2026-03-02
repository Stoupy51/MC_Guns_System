
#> mgs:v5.0.0/mob/init
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.0.0/mob/tick
#

# Mark as initialized
tag @s add mgs.mob_init

# Default active_time to 50 ticks if not set
execute unless score @s mgs.mob.active_time matches 1.. run scoreboard players set @s mgs.mob.active_time 50

# Default sleep_time to 100 ticks if not set
execute unless score @s mgs.mob.sleep_time matches 0.. run scoreboard players set @s mgs.mob.sleep_time 100

# Initialize cooldown to 0
scoreboard players set @s mgs.cooldown 0

# Start in active phase
function mgs:v5.0.0/mob/wake_up

