
#> mgs:v5.0.1/zombies/traps/turret_fire
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.0.1/zombies/traps/active_tick with storage mgs:temp _trap_tick
#
# @args		rx (int)
#			ry (int)
#			rz (int)
#			sx (int)
#			sy (int)
#			sz (int)
#

# @s = trap center marker, at @s position
# Remember this trap's id so we can rotate the matching head display
scoreboard players operation #turret_tid mgs.data = @s mgs.zb.trap.id

# Tag every zombie inside the effect box as a candidate, then keep the one nearest the turret center
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add mgs._turret_cand
execute as @e[tag=mgs._turret_cand,sort=nearest,limit=1] run tag @s add mgs._turret_target
tag @e[tag=mgs._turret_cand] remove mgs._turret_cand

# No zombie in range: nothing to aim at or shoot
execute unless entity @e[tag=mgs._turret_target] run return 0

# Aim this turret's head display at the target (yaw + pitch via facing entity, smoothed by teleport_duration)
execute as @e[tag=mgs.trap_head] if score @s mgs.zb.trap.id = #turret_tid mgs.data at @s run tp @s ~ ~ ~ facing entity @n[tag=mgs._turret_target] eyes

# Fire the bullet from the barrel (block centre, ~1.6 up = head muzzle height) toward the target
execute positioned ~.5 ~1.6 ~.5 facing entity @n[tag=mgs._turret_target] eyes run function mgs:v5.0.1/zombies/traps/turret_shoot

# Clear the temporary target tag
tag @e[tag=mgs._turret_target] remove mgs._turret_target

