
#> mgs:v5.4.1/zombies/traps/kill_zombie
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/traps/damage_fire
#			mgs:v5.4.1/zombies/traps/damage_electric
#

execute store result storage mgs:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 10
function mgs:v5.4.1/zombies/traps/apply_trap_damage with storage mgs:temp _trap_dmg

