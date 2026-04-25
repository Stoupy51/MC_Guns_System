
#> mgs:v5.0.0/zombies/barriers/find_remover
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/intact_tick with storage mgs:temp _btick
#
# @args		radius (unknown)
#

# MACRO: @s = intact barrier marker, $(radius) = sphere radius
# Picks nearest eligible zombie and assigns it as remover
scoreboard players set #barrier_found_remover mgs.data 0
$execute as @e[tag=mgs.zombie_round,tag=!mgs.barrier_removing,distance=..$(radius),limit=1,sort=nearest] run function mgs:v5.0.0/zombies/barriers/start_removing_zombie
execute if score #barrier_found_remover mgs.data matches 1 run scoreboard players set @s mgs.zb.barrier.r_timer 40

