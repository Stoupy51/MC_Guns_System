
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
# Select a zombie in the effect box, then reposition to the turret head (+1) and face it before shooting
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,dx=$(sx),dy=$(sy),dz=$(sz),limit=1] positioned ~$(rx) ~$(ry) ~$(rz) positioned ~ ~1 ~ facing entity @s eyes run function mgs:v5.0.1/zombies/traps/turret_shoot

