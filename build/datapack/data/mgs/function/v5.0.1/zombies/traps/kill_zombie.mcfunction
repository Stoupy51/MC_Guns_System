
#> mgs:v5.0.1/zombies/traps/kill_zombie
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.0.1/zombies/traps/damage_fire
#			mgs:v5.0.1/zombies/traps/damage_electric
#

execute store result storage mgs:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 10
function mgs:v5.0.1/zombies/traps/apply_trap_damage with storage mgs:temp _trap_dmg

