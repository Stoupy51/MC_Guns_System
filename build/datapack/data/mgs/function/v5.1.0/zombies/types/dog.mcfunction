
#> mgs:v5.1.0/zombies/types/dog
#
# @executed	as @e[tag=...]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=...] ]
#			mgs:v5.1.0/zombies/summon_dog_at [ as @n[tag=mgs.zb_dog_new] ]
#

# Add scaled tag, and few data
tag @s add mgs.zb_scaled
data modify entity @s DeathTime set value -16s

# Same HP as the round's zombie — dogs get their threat from speed and damage, not durability
function mgs:v5.1.0/zombies/calc_zombie_hp

# Carried as a MODIFIER, not a base value. Wolf extends TamableAnimal, whose readAdditionalSaveData
# calls setTame(false, true) on any untamed wolf -> applyTamingSideEffects() -> MAX_HEALTH base is
# hard-reset to 8.0. Every /data modify entity and every `store result entity` round-trips the entity
# through save/load, so the angry_at retarget silently reset each dog's base to 8 and Health then
# clamped to it — hence the one-hit kills. Modifiers survive that reset; base values cannot.
scoreboard players remove #zb_hp mgs.data 8
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_dog_hp with storage mgs:temp _zb_hp

# Always faster than the zombie cap (0.32) — outrunning a dog pack should not be an option
execute if score #zb_round mgs.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round mgs.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round mgs.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Slightly below zombie melee (15.0), because dogs reach you far more often
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# Hellhound build: 1.5x a vanilla wolf, which also scales the hitbox so they're easier to hit
attribute @s minecraft:scale base set 1.5

