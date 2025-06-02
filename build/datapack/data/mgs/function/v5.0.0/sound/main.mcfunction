
#> mgs:v5.0.0/sound/main
#
# @within	mgs:v5.0.0/player/right_click with storage mgs:gun all.stats
#

# Simple weapon fire sound
$playsound mgs:$(base_weapon)/fire player @s ~ ~ ~ 0.25
$playsound mgs:$(base_weapon)/fire player @a[distance=0.01..48] 0.75 1 0.25

# Playsound depending on acoustics level
$execute if score @s mgs.acoustics_level matches 0 run playsound mgs:common/$(crack_type)_crack_0_distant player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 1 run playsound mgs:common/$(crack_type)_crack_1_far player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 2 run playsound mgs:common/$(crack_type)_crack_2_midrange player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 3 run playsound mgs:common/$(crack_type)_crack_3_near player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 4 run playsound mgs:common/$(crack_type)_crack_4_closest player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 5 run playsound mgs:common/$(crack_type)_crack_5_water player @s ~ ~ ~ 1.0

# Directs sound propagation to nearby players by aligning their view with the sound source for accurate positional audio
scoreboard players operation #origin_acoustics_level mgs.data = @s mgs.acoustics_level
execute as @a[distance=0.001..224] facing entity @s eyes run function mgs:v5.0.0/sound/propagation

# Simple weapon fire sound
$playsound mgs:$(base_weapon)/fire player @s ~ ~ ~ 0.25
$playsound mgs:$(base_weapon)/fire player @a[distance=0.01..48] 0.75 1 0.25

# Playsound depending on acoustics level
execute if score @s mgs.acoustics_level matches 0 run return run function mgs:v5.0.0/acoustics_0 {}
execute if score @s mgs.acoustics_level matches 1 run return run function mgs:v5.0.0/acoustics_1
execute if score @s mgs.acoustics_level matches 2 run return run function mgs:v5.0.0/acoustics_2
execute if score @s mgs.acoustics_level matches 3 run return run function mgs:v5.0.0/acoustics_3
execute if score @s mgs.acoustics_level matches 4 run return run function mgs:v5.0.0/acoustics_4
execute if score @s mgs.acoustics_level matches 5 run return run function mgs:v5.0.0/acoustics_water

