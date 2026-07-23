
#> mgs:v5.1.0/zombies/traps/damage_fire
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

# Zombies: lethal damage (1000% of each zombie's max health)
data modify storage mgs:temp _trap_dmg.type set value "minecraft:on_fire"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag=mgs.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function mgs:v5.1.0/zombies/traps/kill_zombie

# Players inside the trap: 5 fire damage (PhD Flopper owners are immune)
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={mgs.zb.in_game=1,mgs.special.phd_flopper=0},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:on_fire

