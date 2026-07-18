
#> mgs:v5.1.0/zombies/powerups/insta_kill_melee_off
#
# @executed	as @a[tag=mgs.ik_melee,scores={mgs.special.instant_kill=..0}]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @a[tag=mgs.ik_melee,scores={mgs.special.instant_kill=..0}] ]
#

attribute @s minecraft:attack_damage modifier remove mgs:insta_kill
tag @s remove mgs.ik_melee

