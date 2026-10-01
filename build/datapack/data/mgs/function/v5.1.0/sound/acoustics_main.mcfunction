
#> mgs:v5.1.0/sound/acoustics_main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/sound/main with storage mgs:gun all.sounds
#
# @args		crack (unknown)
#

$execute if score @s mgs.acoustics_level matches 0 run playsound mgs:common/$(crack)_crack_0_distant player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 1 run playsound mgs:common/$(crack)_crack_1_far player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 2 run playsound mgs:common/$(crack)_crack_2_midrange player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 3 run playsound mgs:common/$(crack)_crack_3_near player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 4 run playsound mgs:common/$(crack)_crack_4_closest player @s ~ ~ ~ 1.0
$execute if score @s mgs.acoustics_level matches 5 run playsound mgs:common/$(crack)_crack_5_water player @s ~ ~ ~ 1.0

# Each listener faces the source, so the sound is positioned right.
scoreboard players operation #origin_acoustics_level mgs.data = @s mgs.acoustics_level
execute as @a[distance=0.001..224] facing entity @s eyes run function mgs:v5.1.0/sound/propagation

