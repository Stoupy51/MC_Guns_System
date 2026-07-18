
#> mgs:v5.1.0/mob/tick
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.1.0/tick [ as @e[tag=mgs.armed] & at @s ]
#

# Initialize mob if not yet initialized
execute unless entity @s[tag=mgs.mob_init] run function mgs:v5.1.0/mob/init

# Phase timer management: decrement timer
execute if score @s mgs.mob.timer matches 1.. run scoreboard players remove @s mgs.mob.timer 1

# Phase transitions when timer reaches 0
execute if score @s mgs.mob.timer matches 0 if entity @s[tag=mgs.mob_sleeping] run function mgs:v5.1.0/mob/wake_up
execute if score @s mgs.mob.timer matches 0 unless entity @s[tag=mgs.mob_sleeping] unless score @s mgs.mob.sleep_time matches 0 run function mgs:v5.1.0/mob/go_sleep

# If sleeping, skip everything
execute if entity @s[tag=mgs.mob_sleeping] run return 0

# Decrease weapon cooldown by 1
execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

# If cooldown is active, skip shooting
execute if score @s mgs.cooldown matches 1.. run return 0

# Pick target BEFORE paying the equipment-NBT gun copy: last attacker, otherwise nearest player.
# Scores (not @e[tag=] existence rescans) carry "did we find anyone" between the two paths.
scoreboard players set #mob_has_target mgs.data 0
execute store success score #mob_has_target mgs.data on attacker run tag @s add mgs.target

# Fall back to the nearest player. Two rules this block has to respect, both of which silently
# broke mobs before:
#  - the result goes to a scratch score, because `execute store success` writes 0 whenever a guard
#    on the same chain filters the command out. Writing straight to #mob_has_target zeroed the
#    attacker hit above, so any mob that had ever been shot never fired again.
#  - "is a player in range" is asked separately from `tag ... add`, which reports failure when the
#    tag is merely already present — otherwise one leaked tag wedges the mob permanently.
scoreboard players set #mob_near_target mgs.data 0
execute if score #mob_has_target mgs.data matches 0 if entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] run scoreboard players set #mob_near_target mgs.data 1
execute if score #mob_near_target mgs.data matches 1 run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add mgs.target
scoreboard players operation #mob_has_target mgs.data > #mob_near_target mgs.data

# No target in range, skip
execute if score #mob_has_target mgs.data matches 0 run return 0

# Copy gun data from equipment mainhand to shared storage
function mgs:v5.1.0/mob/copy_gun_data

# Check we have valid gun data (clean the target tag up on the way out)
execute unless data storage mgs:gun all.stats run return run tag @e[tag=mgs.target,limit=1] remove mgs.target

# Line-of-sight check: can the mob see the target? (limit=1 skips the @n distance sort — the
# tag is only ever on one entity)
scoreboard players set #can_see mgs.data 0
execute positioned as @e[tag=mgs.target,limit=1] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return run tag @e[tag=mgs.target,limit=1] remove mgs.target

# Tag as ticking (for compatibility with existing damage/raycast system)
tag @s add mgs.ticking

# Aim at target and fire
execute anchored eyes facing entity @e[tag=mgs.target,limit=1] feet run function mgs:v5.1.0/mob/fire_weapon

# Remove tags
tag @e[tag=mgs.target,limit=1] remove mgs.target
tag @s remove mgs.ticking

