
#> mgs:v5.1.0/weapon/hit_direction
#
# @within	#mgs:signals/damage
#

# Red 36-way hit direction indicator, shown to player victims only
execute unless entity @s[type=player] run return 0

# Explosion self-hits have no meaningful direction (hitscan cannot self-hit)
execute if entity @s[tag=mgs.temp_shooter] run return 0

# Locate the shooter
scoreboard players set #hit_src mgs.data 0
execute at @s if entity @n[tag=mgs.ticking] run scoreboard players set #hit_src mgs.data 1
execute at @s if score #hit_src mgs.data matches 0 if entity @n[tag=mgs.temp_shooter] run scoreboard players set #hit_src mgs.data 2
execute if score #hit_src mgs.data matches 0 run return 0

# Yaw toward the shooter (x100): face a scratch marker at the victim toward the shooter, read it back
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["mgs.hit_dir_marker"]}
execute at @s if score #hit_src mgs.data matches 1 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.ticking] eyes
execute at @s if score #hit_src mgs.data matches 2 run tp @n[tag=mgs.hit_dir_marker] ~ ~ ~ facing entity @n[tag=mgs.temp_shooter] eyes
execute at @s store result score #hit_dir mgs.data run data get entity @n[tag=mgs.hit_dir_marker] Rotation[0] 100
execute at @s run kill @n[tag=mgs.hit_dir_marker]

# Sector 0..35 relative to the victim's facing (0 = front, clockwise; scoreboard %= is floorMod).
# The half-sector offset makes each sector straddle its direction instead of starting at it.
execute store result score #hit_yaw mgs.data run data get entity @s Rotation[0] 100
scoreboard players operation #hit_dir mgs.data -= #hit_yaw mgs.data
scoreboard players add #hit_dir mgs.data 500
scoreboard players operation #hit_dir mgs.data %= #36000 mgs.data
scoreboard players operation #hit_dir mgs.data /= #1000 mgs.data

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
execute if score #hit_dir mgs.data matches 8 run title @s title {"text":"I","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 9 run title @s title {"text":"J","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 10 run title @s title {"text":"K","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 11 run title @s title {"text":"L","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 12 run title @s title {"text":"M","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 13 run title @s title {"text":"N","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 14 run title @s title {"text":"O","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 15 run title @s title {"text":"P","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 16 run title @s title {"text":"Q","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 17 run title @s title {"text":"R","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 18 run title @s title {"text":"S","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 19 run title @s title {"text":"T","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 20 run title @s title {"text":"U","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 21 run title @s title {"text":"V","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 22 run title @s title {"text":"W","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 23 run title @s title {"text":"X","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 24 run title @s title {"text":"Y","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 25 run title @s title {"text":"Z","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 26 run title @s title {"text":"a","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 27 run title @s title {"text":"b","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 28 run title @s title {"text":"c","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 29 run title @s title {"text":"d","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 30 run title @s title {"text":"e","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 31 run title @s title {"text":"f","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 32 run title @s title {"text":"g","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 33 run title @s title {"text":"h","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 34 run title @s title {"text":"i","font":"mgs:hit_dir","color":"#FF2A2A"}
execute if score #hit_dir mgs.data matches 35 run title @s title {"text":"j","font":"mgs:hit_dir","color":"#FF2A2A"}

