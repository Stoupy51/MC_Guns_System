
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

# Find nearest target (player within 64 blocks, not in spectator/creative)
execute unless entity @a[distance=..64,gamemode=!spectator,gamemode=!creative] run return 0

# Line-of-sight check: can the mob see the nearest target? (Bookshelf view check)
# @s = mob (observer), positioned at target player's position
execute positioned as @p[distance=..64,gamemode=!spectator,gamemode=!creative] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return 0

# Tag as ticking (for compatibility with existing damage/raycast system)
tag @s add mgs.ticking

# Aim at nearest valid target and fire
execute anchored eyes facing entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] feet run function mgs:v5.0.0/mob/fire_weapon

# Remove ticking tag
tag @s remove mgs.ticking

