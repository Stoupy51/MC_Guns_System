
#> mgs:v5.1.0/zombies/traps/turret_fire
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
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

# @s = trap center marker, at @s position
# Remember this trap's id so we can find/rotate the matching head display and use it as the muzzle
scoreboard players operation #turret_tid mgs.data = @s mgs.zb.trap.id

# Tag every zombie inside the effect box as a candidate, keep only those the head has line of sight to,
# then pick the one nearest the turret center
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz)] run tag @s add mgs._turret_cand
execute as @e[tag=mgs._turret_cand] run function mgs:v5.1.0/zombies/traps/turret_check_los
# Capture, via the tag command's success, whether a target was selected — avoids the global
# `unless entity @e[tag=mgs._turret_target]` scan below. limit=1 means this runs at most once;
# #turret_has_target stays 0 if there was no visible zombie (the body never executes).
scoreboard players set #turret_has_target mgs.data 0
execute as @e[tag=mgs._turret_visible,sort=nearest,limit=1] store success score #turret_has_target mgs.data run tag @s add mgs._turret_target
tag @e[tag=mgs._turret_cand] remove mgs._turret_cand
tag @e[tag=mgs._turret_visible] remove mgs._turret_visible

# No visible zombie in range: nothing to aim at or shoot
execute if score #turret_has_target mgs.data matches 0 run return 0

# Aim this turret's head display at the target (yaw + pitch via facing entity, smoothed by teleport_duration)
execute as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] at @s run tp @s ~ ~ ~ facing entity @n[tag=mgs._turret_target] eyes

# Fire the bullet straight from the head display itself (no manual offset) toward the target
execute as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] at @s facing entity @n[tag=mgs._turret_target] eyes positioned ^ ^ ^1 run function mgs:v5.1.0/zombies/traps/turret_shoot

# Clear the temporary target tag
tag @e[tag=mgs._turret_target] remove mgs._turret_target

