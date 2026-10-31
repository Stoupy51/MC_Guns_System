
#> mgs:v5.3.0/zombies/types/apply
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#

execute if score #zb_type mgs.data matches 1 run return run function mgs:v5.3.0/zombies/types/fast
execute if score #zb_type mgs.data matches 2 run return run function mgs:v5.3.0/zombies/types/tank
execute if score #zb_type mgs.data matches 3 run return run function mgs:v5.3.0/zombies/types/armed
execute if score #zb_type mgs.data matches 4 run return run function mgs:v5.3.0/zombies/types/aura

