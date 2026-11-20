
#> mgs:v5.4.3/raycast/accuracy/get_value
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/player/shoot
#			mgs:v5.4.3/projectile/summon
#			mgs:v5.4.3/grenade/summon
#

## Order matters: sneak in the air counts as walk, then jump, sneak, sprint, walk, base.
data remove storage mgs:gun accuracy

execute unless predicate mgs:v5.4.3/is_on_ground if predicate mgs:v5.4.3/is_sneaking run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_walk

execute unless predicate mgs:v5.4.3/is_on_ground run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_jump

execute if predicate mgs:v5.4.3/is_sneaking if data storage mgs:gun all.stats.fire_modes[0].accuracy_sneak run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.fire_modes[0].accuracy_sneak
execute if predicate mgs:v5.4.3/is_sneaking run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_sneak

execute if predicate mgs:v5.4.3/is_sprinting run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_sprint

execute if predicate mgs:v5.4.3/is_moving run return run data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_walk

data modify storage mgs:gun accuracy set from storage mgs:gun all.stats.acc_base

