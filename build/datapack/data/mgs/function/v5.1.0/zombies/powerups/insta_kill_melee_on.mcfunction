
#> mgs:v5.1.0/zombies/powerups/insta_kill_melee_on
#
# @executed	as @a[tag=!mgs.ik_melee,scores={mgs.special.instant_kill=1..}]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @a[tag=!mgs.ik_melee,scores={mgs.special.instant_kill=1..}] ]
#

# remove-then-add keeps this idempotent even if a stale modifier survived a game crash
attribute @s minecraft:attack_damage modifier remove mgs:insta_kill
attribute @s minecraft:attack_damage modifier add mgs:insta_kill 100000 add_value
tag @s add mgs.ik_melee

