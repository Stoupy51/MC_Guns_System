
#> mgs:v5.1.0/zombies/traps/apply_trap_damage
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.1.0/zombies/traps/kill_zombie with storage mgs:temp _trap_dmg
#			mgs:v5.1.0/zombies/traps/turret_hit with storage mgs:temp _trap_dmg
#
# @args		amount (unknown)
#			type (unknown)
#

$damage @s $(amount) $(type)

