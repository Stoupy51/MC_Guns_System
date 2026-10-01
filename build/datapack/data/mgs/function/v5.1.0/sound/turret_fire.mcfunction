
#> mgs:v5.1.0/sound/turret_fire
#
# @executed	as @e[tag=mgs.trap_head,predicate=mgs:v5.1.0/zombies/traps/turret_id_match] & at @s & facing entity @n[tag=mgs._turret_target] eyes & positioned ^ ^ ^1
#
# @within	mgs:v5.1.0/zombies/traps/turret_shoot
#

# The turret's acoustics, as for a firing player.
function mgs:v5.1.0/sound/compute_acoustics
scoreboard players operation #origin_acoustics_level mgs.data = @s mgs.acoustics_level

# The fire_simple mix.
playsound mgs:g3a3/fire player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

# Each listener's own acoustics level.
data modify storage mgs:temp _turret_snd set value {crack:"large"}
execute as @a[distance=0.001..224] facing entity @s eyes run function mgs:v5.1.0/sound/turret_propagation

