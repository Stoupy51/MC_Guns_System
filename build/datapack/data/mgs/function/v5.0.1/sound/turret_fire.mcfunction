
#> mgs:v5.0.1/sound/turret_fire
#
# @executed	as @e[tag=mgs.trap_head,predicate=mgs:v5.0.1/zombies/traps/turret_id_match] & at @s & facing entity @n[tag=mgs._turret_target] eyes & positioned ^ ^ ^1
#
# @within	mgs:v5.0.1/zombies/traps/turret_shoot
#

# Compute the source environment acoustics at the turret, exactly like a firing player
function mgs:v5.0.1/sound/compute_acoustics
scoreboard players operation #origin_acoustics_level mgs.data = @s mgs.acoustics_level

# Close-range g3a3 mechanical report for nearby players (same mix as sound/fire_simple)
playsound mgs:g3a3/fire player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

# Propagate the 'large' crack to every listener, using each listener's own acoustics level
data modify storage mgs:temp _turret_snd set value {crack:"large"}
execute as @a[distance=0.001..224] facing entity @s eyes run function mgs:v5.0.1/sound/turret_propagation

