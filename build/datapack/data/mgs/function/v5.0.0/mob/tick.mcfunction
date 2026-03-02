
#> mgs:v5.0.0/mob/tick
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.0.0/tick [ as @e[tag=mgs.armed] & at @s ]
#

# Initialize mob if not yet initialized
execute unless entity @s[tag=mgs.mob_init] run function mgs:v5.0.0/mob/init

# Phase timer management: decrement timer
execute if score @s mgs.mob.timer matches 1.. run scoreboard players remove @s mgs.mob.timer 1

# Phase transitions when timer reaches 0
execute if score @s mgs.mob.timer matches 0 if entity @s[tag=mgs.mob_sleeping] run function mgs:v5.0.0/mob/wake_up
execute if score @s mgs.mob.timer matches 0 unless entity @s[tag=mgs.mob_sleeping] unless score @s mgs.mob.sleep_time matches 0 run function mgs:v5.0.0/mob/go_sleep

# If sleeping, skip everything
execute if entity @s[tag=mgs.mob_sleeping] run return 0

# Decrease weapon cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# If cooldown is active, skip shooting
execute if score @s mgs.cooldown matches 1.. run return 0

# Copy gun data from equipment mainhand to shared storage
function mgs:v5.0.0/mob/copy_gun_data

# Check if we have valid gun data
execute unless data storage mgs:gun all.stats run return 0

# Pick target: last attacker if in range, otherwise nearest player
execute on attacker run tag @s add mgs.target
execute unless entity @e[tag=mgs.target] run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add mgs.target

# No target in range, skip
execute unless entity @e[tag=mgs.target] run return 0

# Line-of-sight check: can the mob see the target?
execute positioned as @n[tag=mgs.target] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return run tag @e[tag=mgs.target] remove mgs.target

# Tag as ticking (for compatibility with existing damage/raycast system)
tag @s add mgs.ticking

# Aim at target and fire
execute anchored eyes facing entity @n[tag=mgs.target] feet run function mgs:v5.0.0/mob/fire_weapon

# Remove tags
tag @e[tag=mgs.target] remove mgs.target
tag @s remove mgs.ticking

