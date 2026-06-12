
#> mgs:v5.0.1/grenade/spin_tick
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.1/grenade/tick
#

scoreboard players add @s mgs.grenade_spin 0
scoreboard players operation @s mgs.grenade_spin += #gr_speed mgs.data
scoreboard players operation @s mgs.grenade_spin %= #62832 mgs.data
execute store result storage mgs:temp _gr_spin.angle float 0.0001 run scoreboard players get @s mgs.grenade_spin
function mgs:v5.0.1/grenade/apply_spin with storage mgs:temp _gr_spin

