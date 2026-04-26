
#> mgs:v5.0.0/zombies/types/normal
#
# @within	mgs:v5.0.0/zombies/types/armed {level:"$(level)"}
#			mgs:v5.0.0/zombies/types/fast {level:"$(level)"}
#			mgs:v5.0.0/zombies/types/tank {level:"$(level)"}
#

# Add scaled tag
tag @s add mgs.zb_scaled

# Delay visual death by 20 ticks
data modify entity @s DeathTime set value -20s

# Compute BO2-derived HP for this round and apply it to this zombie
function mgs:v5.0.0/zombies/calc_zombie_hp
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.0.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp

# Speed tiers from BO2 behavior (multiplier 8): walk R1-5, run R6-8, sprint R9+
execute if score #zb_round mgs.data matches ..5 run attribute @s minecraft:movement_speed base set 0.18
execute if score #zb_round mgs.data matches 6..8 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round mgs.data matches 9 run attribute @s minecraft:movement_speed base set 0.30

# BO2-style walkers: R10+ has 10% chance to spawn as walk speed instead of sprint
execute if score #zb_round mgs.data matches 10.. store result score #zb_speed_roll mgs.data run random value 1..10
execute if score #zb_round mgs.data matches 10.. if score #zb_speed_roll mgs.data matches 1 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round mgs.data matches 10.. if score #zb_speed_roll mgs.data matches 2.. run attribute @s minecraft:movement_speed base set 0.30

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s mgs.zb.rise_tick 20

