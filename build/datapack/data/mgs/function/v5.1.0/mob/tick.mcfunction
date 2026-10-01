
#> mgs:v5.1.0/mob/tick
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.1.0/tick [ as @e[tag=mgs.armed] & at @s ]
#

execute unless entity @s[tag=mgs.mob_init] run function mgs:v5.1.0/mob/init

execute if score @s mgs.mob.timer matches 1.. run scoreboard players remove @s mgs.mob.timer 1

execute if score @s mgs.mob.timer matches 0 if entity @s[tag=mgs.mob_sleeping] run function mgs:v5.1.0/mob/wake_up
execute if score @s mgs.mob.timer matches 0 unless entity @s[tag=mgs.mob_sleeping] unless score @s mgs.mob.sleep_time matches 0 run function mgs:v5.1.0/mob/go_sleep

execute if entity @s[tag=mgs.mob_sleeping] run return 0

execute if score @s mgs.cooldown matches 1.. run scoreboard players remove @s mgs.cooldown 1

execute if score @s mgs.cooldown matches 1.. run return 0

# Target first, before the costly equipment NBT gun copy: last attacker, else the nearest player.
scoreboard players set #mob_has_target mgs.data 0
execute store success score #mob_has_target mgs.data on attacker run tag @s add mgs.target

# `on attacker` outlives the fight, so a dead (spectator) or creative attacker is dropped and the search below runs;
# the untag scan only runs in that rare case.
scoreboard players set #mob_dead_target mgs.data 0
execute if score #mob_has_target mgs.data matches 1 if entity @a[tag=mgs.target,gamemode=!adventure,gamemode=!survival] run scoreboard players set #mob_dead_target mgs.data 1
execute if score #mob_dead_target mgs.data matches 1 run scoreboard players set #mob_has_target mgs.data 0
execute if score #mob_dead_target mgs.data matches 1 run tag @a[tag=mgs.target] remove mgs.target

# The nearest-player result goes to a scratch score: `store success` writes 0 when a guard filters the command out,
# which zeroed the attacker hit above. The range test is separate from `tag ... add`, which fails when the tag is already there.
scoreboard players set #mob_near_target mgs.data 0
execute if score #mob_has_target mgs.data matches 0 if entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] run scoreboard players set #mob_near_target mgs.data 1
execute if score #mob_near_target mgs.data matches 1 run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add mgs.target
scoreboard players operation #mob_has_target mgs.data > #mob_near_target mgs.data

execute if score #mob_has_target mgs.data matches 0 run return 0

# From the mainhand equipment.
function mgs:v5.1.0/mob/copy_gun_data

# Also cleans the target tag up.
execute unless data storage mgs:gun all.stats run return run tag @e[tag=mgs.target,limit=1] remove mgs.target

# limit=1 skips the @n distance sort: only one entity carries the tag.
scoreboard players set #can_see mgs.data 0
execute positioned as @e[tag=mgs.target,limit=1] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return run tag @e[tag=mgs.target,limit=1] remove mgs.target

# The damage and raycast system expects it.
tag @s add mgs.ticking

execute anchored eyes facing entity @e[tag=mgs.target,limit=1] feet run function mgs:v5.1.0/mob/fire_weapon

tag @e[tag=mgs.target,limit=1] remove mgs.target
tag @s remove mgs.ticking

