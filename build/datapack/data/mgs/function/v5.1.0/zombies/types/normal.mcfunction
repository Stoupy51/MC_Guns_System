
#> mgs:v5.1.0/zombies/types/normal
#
# @within	mgs:v5.1.0/zombies/types/armed {level:"$(level)"}
#			mgs:v5.1.0/zombies/types/fast {level:"$(level)"}
#			mgs:v5.1.0/zombies/types/tank {level:"$(level)"}
#

# Add scaled tag, and few data
tag @s add mgs.zb_scaled
data modify entity @s DeathTime set value -16s

# Compute round-scaled HP (base_health * 1.1^(round - 1)) and apply it to this zombie
function mgs:v5.1.0/zombies/calc_zombie_hp
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp

# Explicit speed per round, capped at 0.32 from round 13+
execute if score #zb_round mgs.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round mgs.data matches 2 run attribute @s minecraft:movement_speed base set 0.21
execute if score #zb_round mgs.data matches 3 run attribute @s minecraft:movement_speed base set 0.22
execute if score #zb_round mgs.data matches 4 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round mgs.data matches 5 run attribute @s minecraft:movement_speed base set 0.24
execute if score #zb_round mgs.data matches 6 run attribute @s minecraft:movement_speed base set 0.25
execute if score #zb_round mgs.data matches 7 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_round mgs.data matches 8 run attribute @s minecraft:movement_speed base set 0.27
execute if score #zb_round mgs.data matches 9 run attribute @s minecraft:movement_speed base set 0.28
execute if score #zb_round mgs.data matches 10 run attribute @s minecraft:movement_speed base set 0.29
execute if score #zb_round mgs.data matches 11 run attribute @s minecraft:movement_speed base set 0.30
execute if score #zb_round mgs.data matches 12 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round mgs.data matches 13.. run attribute @s minecraft:movement_speed base set 0.32

# For round 15+, 10% walkers (0.20 speed)
execute if score #zb_round mgs.data matches 15.. store result score #zb_speed_roll mgs.data run random value 1..10
execute if score #zb_round mgs.data matches 15.. if score #zb_speed_roll mgs.data matches 1 run attribute @s minecraft:movement_speed base set 0.20

# Fixed melee damage: 15.0 HP = 7.5 hearts and no knockback
attribute @s minecraft:attack_damage base set 15.0
attribute @s minecraft:knockback_resistance base set 1024

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s mgs.zb.rise_tick 20

