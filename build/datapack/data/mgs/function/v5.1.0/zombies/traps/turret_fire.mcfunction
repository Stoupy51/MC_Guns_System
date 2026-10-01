
#> mgs:v5.1.0/zombies/traps/turret_fire
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/traps/active_tick with storage mgs:temp _trap_tick
#
# @args		rx (int)
#			ry (int)
#			rz (int)
#			sx (int)
#			sy (int)
#			sz (int)
#

# Run as the trap centre marker, at it.
scoreboard players operation #turret_tid mgs.data = @s mgs.zb.trap.id

# Candidates are the zombies in the box that the head can see; the nearest to the centre wins.
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add mgs._turret_cand
execute as @e[tag=mgs._turret_cand] run function mgs:v5.1.0/zombies/traps/turret_check_los
# The tag's `store success` tells whether a target was picked (limit=1), with no extra @e scan.
scoreboard players set #turret_has_target mgs.data 0
execute as @e[tag=mgs._turret_visible,sort=nearest,limit=1] store success score #turret_has_target mgs.data run tag @s add mgs._turret_target
tag @e[tag=mgs._turret_cand] remove mgs._turret_cand
tag @e[tag=mgs._turret_visible] remove mgs._turret_visible

execute if score #turret_has_target mgs.data matches 0 run return 0

# Smoothed by teleport_duration.
execute as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] at @s run tp @s ~ ~ ~ facing entity @n[tag=mgs._turret_target] eyes

execute as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] at @s facing entity @n[tag=mgs._turret_target] eyes positioned ^ ^ ^1 run function mgs:v5.1.0/zombies/traps/turret_shoot

tag @e[tag=mgs._turret_target] remove mgs._turret_target

