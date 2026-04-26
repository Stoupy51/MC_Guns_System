
#> mgs:v5.0.0/zombies/types/normal
#
# @within	mgs:v5.0.0/zombies/types/armed {level:"$(level)"}
#			mgs:v5.0.0/zombies/types/fast {level:"$(level)"}
#			mgs:v5.0.0/zombies/types/tank {level:"$(level)"}
#
# @args		level (string)
#

tag @s add mgs.zb_scaled

$scoreboard players set #zb_level mgs.data $(level)

# Level 1: default 20 HP (rounds 1-5) — no changes needed
# Level 2: 30 HP (rounds 6-10)
execute if score #zb_level mgs.data matches 2 run attribute @s minecraft:max_health base set 30
execute if score #zb_level mgs.data matches 2 run data modify entity @s Health set value 30f

# Level 3: 40 HP (rounds 11-15)
execute if score #zb_level mgs.data matches 3 run attribute @s minecraft:max_health base set 40
execute if score #zb_level mgs.data matches 3 run data modify entity @s Health set value 40f

# Level 4: 60 HP (rounds 16+)
execute if score #zb_level mgs.data matches 4 run attribute @s minecraft:max_health base set 60
execute if score #zb_level mgs.data matches 4 run data modify entity @s Health set value 60f

# Increase speed slightly at higher levels
execute if score #zb_level mgs.data matches 3 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_level mgs.data matches 4 run attribute @s minecraft:movement_speed base set 0.30

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s mgs.zb.rise_tick 20

