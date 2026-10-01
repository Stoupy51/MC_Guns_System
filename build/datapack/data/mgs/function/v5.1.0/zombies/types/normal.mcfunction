
#> mgs:v5.1.0/zombies/types/normal
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/summon_zombie_at {level:"$(level)"}
#			mgs:v5.1.0/zombies/types/armed {level:"$(level)"}
#			mgs:v5.1.0/zombies/types/fast {level:"$(level)"}
#			mgs:v5.1.0/zombies/types/tank {level:"$(level)"}
#

tag @s add mgs.zb_scaled
data modify entity @s DeathTime set value -16s

# BO1 curve: +100 BO HP per round until round 9, then x1.1 per round.
function mgs:v5.1.0/zombies/calc_zombie_hp
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp

# Capped at 0.32 from round 36.
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
execute if score #zb_round mgs.data matches 11..29 run attribute @s minecraft:movement_speed base set 0.30
execute if score #zb_round mgs.data matches 30..35 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round mgs.data matches 36.. run attribute @s minecraft:movement_speed base set 0.32

# Speed 0.29+ is the BO2 sprint gait, which screams (3-5 s clips) instead of groaning (see vocals).
execute if score #zb_round mgs.data matches 10.. run tag @s add mgs.zb_sprint

# From round 15, 10% are walkers (0.20).
execute if score #zb_round mgs.data matches 15.. store result score #zb_speed_roll mgs.data run random value 1..10
execute if score #zb_round mgs.data matches 15.. if score #zb_speed_roll mgs.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round mgs.data matches 15.. if score #zb_speed_roll mgs.data matches 1 run tag @s remove mgs.zb_sprint

# 7.5 hearts, no knockback.
attribute @s minecraft:attack_damage base set 15.0
attribute @s minecraft:knockback_resistance base set 1024

# 20 ticks to rise 2 blocks.
scoreboard players set @s mgs.zb.rise_tick 20

