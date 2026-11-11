
#> mgs:v5.4.2/zombies/powerups/insta_kill_melee_off
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_tick [ as @a[tag=mgs.ik_melee,scores={mgs.special.instant_kill=..0}] ]
#

attribute @s minecraft:attack_damage modifier remove mgs:insta_kill
tag @s remove mgs.ik_melee

