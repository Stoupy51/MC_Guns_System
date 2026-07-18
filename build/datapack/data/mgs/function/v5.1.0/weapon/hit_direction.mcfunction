
#> mgs:v5.1.0/weapon/hit_direction
#
# @within	#mgs:signals/damage
#

# Red 8-way hit direction indicator, shown to player victims only
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no meaningful direction (hitscan cannot self-hit)
execute if entity @s[tag=mgs.temp_shooter] run return 0

# Locate the shooter
scoreboard players set #hit_src mgs.data 0
execute at @s if entity @n[tag=mgs.ticking] run scoreboard players set #hit_src mgs.data 1
execute at @s if score #hit_src mgs.data matches 0 if entity @n[tag=mgs.temp_shooter] run scoreboard players set #hit_src mgs.data 2
execute if score #hit_src mgs.data matches 0 run return 0

# Yaw toward the shooter (x10): face a scratch marker at the victim toward the shooter, read it back
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["mgs.hit_dir_marker"]}
execute at @s if score #hit_src mgs.data matches 1 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.ticking] eyes
execute at @s if score #hit_src mgs.data matches 2 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.temp_shooter] eyes
execute at @s store result score #hit_dir mgs.data run data get entity @n[tag=mgs.hit_dir_marker] Rotation[0] 10
execute at @s run kill @n[tag=mgs.hit_dir_marker]

# Sector 0..7 relative to the victim's facing (0 = front, clockwise; scoreboard %= is floorMod)
execute store result score #hit_yaw mgs.data run data get entity @s Rotation[0] 10
scoreboard players operation #hit_dir mgs.data -= #hit_yaw mgs.data
scoreboard players add #hit_dir mgs.data 225
scoreboard players operation #hit_dir mgs.data %= #3600 mgs.data
scoreboard players operation #hit_dir mgs.data /= #450 mgs.data

# Flash the matching arc glyph around the crosshair (~0.7s, no fade-in)
title @s times 0 8 6
execute if score #hit_dir mgs.data matches 0 run title @s title {"text":"A","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 1 run title @s title {"text":"B","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 2 run title @s title {"text":"C","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 3 run title @s title {"text":"D","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 4 run title @s title {"text":"E","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 5 run title @s title {"text":"F","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 6 run title @s title {"text":"G","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 7 run title @s title {"text":"H","font":"mgs:hit_dir","color":"#FF2A2A"}

