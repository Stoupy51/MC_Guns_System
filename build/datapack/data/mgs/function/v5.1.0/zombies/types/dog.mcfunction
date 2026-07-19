
#> mgs:v5.1.0/zombies/types/dog
#
# @executed	as @e[tag=mgs.dog_portal] & at @s
#
# @within	mgs:v5.1.0/zombies/summon_dog_at {level:"$(level)"}
#

# Add scaled tag, and few data
tag @s add mgs.zb_scaled
data modify entity @s DeathTime set value -16s

# 150% of the round's zombie HP, floored at 2x a vanilla zombie so round 5 dogs aren't one-shot
function mgs:v5.1.0/zombies/calc_zombie_hp
scoreboard players operation #zb_hp mgs.data *= #3 mgs.data
scoreboard players operation #zb_hp mgs.data /= #2 mgs.data
execute if score #zb_hp mgs.data matches ..39 run scoreboard players set #zb_hp mgs.data 40
execute if score #zb_hp mgs.data matches 2049.. run scoreboard players set #zb_hp mgs.data 2048
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp

# Always faster than the zombie cap (0.32) — outrunning a dog pack should not be an option
execute if score #zb_round mgs.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round mgs.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round mgs.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Slightly below zombie melee (15.0), because dogs reach you far more often
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# Hellhound build: 1.5x a vanilla wolf, which also scales the hitbox so they're easier to hit
attribute @s minecraft:scale base set 1.5

