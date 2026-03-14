
#> mgs:v5.0.0/zombies/traps/damage_fire
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.0.0/zombies/traps/active_tick with storage mgs:temp _trap_tick
#
# @args		rx (unknown)
#			ry (unknown)
#			rz (unknown)
#			sx (unknown)
#			sy (unknown)
#			sz (unknown)
#

$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:on_fire

