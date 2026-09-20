
#> mgs:v5.1.0/zombies/traps/turret_check_los
#
# @executed	as @e[tag=mgs._turret_cand]
#
# @within	mgs:v5.1.0/zombies/traps/turret_fire [ as @e[tag=mgs._turret_cand] ]
#

# @s = candidate zombie
scoreboard players set #turret_vis mgs.data 0
execute at @e[tag=mgs.trap_interact,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] positioned ~ ~-1.5 ~ store result score #turret_vis mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #turret_vis mgs.data matches 1 run tag @s add mgs._turret_visible

