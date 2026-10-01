
#> mgs:v5.1.0/zombies/types/dog
#
# @executed	as @e[type=minecraft:wolf,tag=...]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[type=minecraft:wolf,tag=...] ]
#			mgs:v5.1.0/zombies/summon_dog_at [ as @n[tag=mgs.zb_dog_new] ]
#			mgs:v5.1.0/zombies/summon_zombie_at {level:"$(level)"}
#

tag @s add mgs.zb_scaled
data modify entity @s DeathTime set value -16s

# Same HP as the round's zombie: dogs threaten through speed and damage.
function mgs:v5.1.0/zombies/calc_zombie_hp

# A modifier, not a base value: every save/load round-trip (any /data modify or `store result entity`) runs
# TamableAnimal.setTame(false, true), which resets the MAX_HEALTH base of an untamed wolf to 8.
scoreboard players remove #zb_hp mgs.data 8
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_dog_hp with storage mgs:temp _zb_hp

# Always above the zombie cap (0.32): a dog pack cannot be outrun.
execute if score #zb_round mgs.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round mgs.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round mgs.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Below zombie melee (15.0), since dogs reach you far more often.
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# 1.5x a vanilla wolf, which also enlarges the hitbox.
attribute @s minecraft:scale base set 1.5

