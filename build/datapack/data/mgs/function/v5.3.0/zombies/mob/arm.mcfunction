
#> mgs:v5.3.0/zombies/mob/arm
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#

data modify storage mgs:temp _arm set value {active_time:60,sleep_time:40,prefix:""}
data modify storage mgs:temp _arm.entity set from storage mgs:temp _mob.entity
data modify storage mgs:temp _arm.prefix set string storage mgs:temp _arm.entity 0 10
execute if data storage mgs:temp _arm{prefix:"minecraft:"} run data modify storage mgs:temp _arm.entity set string storage mgs:temp _arm.entity 10

# The gun's level, else 1 for a named gun, else the round's tier.
execute store result storage mgs:temp _arm.level int 1 run scoreboard players get #zb_level mgs.data
execute if data storage mgs:temp _mob.gun.id run data modify storage mgs:temp _arm.level set value 1
execute if data storage mgs:temp _mob.gun.level run data modify storage mgs:temp _arm.level set from storage mgs:temp _mob.gun.level
function mgs:v5.3.0/mob/arm with storage mgs:temp _arm

execute if data storage mgs:temp _mob.gun.id run return run function mgs:v5.3.0/zombies/mob/give_gun with storage mgs:temp _mob.gun
function mgs:v5.3.0/utils/random_weapon_no_explosive

