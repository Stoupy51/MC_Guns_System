
#> mgs:v5.0.0/zombies/scale_zombie
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/summon_zombie_at {level:"$(level)"}
#
# @args		level (unknown)
#

tag @s add mgs.zb_scaled

$scoreboard players set #_zb_level mgs.data $(level)

# Level 1: default 20 HP (rounds 1-5) — no changes needed
# Level 2: 30 HP (rounds 6-10)
execute if score #_zb_level mgs.data matches 2 run attribute @s minecraft:max_health base set 30
execute if score #_zb_level mgs.data matches 2 run data modify entity @s Health set value 30f

# Level 3: 40 HP (rounds 11-15)
execute if score #_zb_level mgs.data matches 3 run attribute @s minecraft:max_health base set 40
execute if score #_zb_level mgs.data matches 3 run data modify entity @s Health set value 40f

# Level 4: 60 HP (rounds 16+)
execute if score #_zb_level mgs.data matches 4 run attribute @s minecraft:max_health base set 60
execute if score #_zb_level mgs.data matches 4 run data modify entity @s Health set value 60f

# Increase speed slightly at higher levels
execute if score #_zb_level mgs.data matches 3 run attribute @s minecraft:movement_speed base set 0.26
execute if score #_zb_level mgs.data matches 4 run attribute @s minecraft:movement_speed base set 0.30

