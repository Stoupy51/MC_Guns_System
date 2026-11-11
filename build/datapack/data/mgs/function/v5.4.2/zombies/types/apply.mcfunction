
#> mgs:v5.4.2/zombies/types/apply
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mob/setup
#

execute if score #zb_type mgs.data matches 1 run return run function mgs:v5.4.2/zombies/types/fast
execute if score #zb_type mgs.data matches 2 run return run function mgs:v5.4.2/zombies/types/tank
execute if score #zb_type mgs.data matches 3 run return run function mgs:v5.4.2/zombies/types/armed
execute if score #zb_type mgs.data matches 4 run return run function mgs:v5.4.2/zombies/types/aura

