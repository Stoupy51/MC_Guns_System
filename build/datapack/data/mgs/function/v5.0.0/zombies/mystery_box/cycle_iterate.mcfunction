
#> mgs:v5.0.0/zombies/mystery_box/cycle_iterate
#
# @within	mgs:v5.0.0/zombies/mystery_box/cycle_display
#			mgs:v5.0.0/zombies/mystery_box/cycle_iterate
#

execute if score #_mb_cycle mgs.data matches 1.. run data remove storage mgs:temp _mb_cycle_iter[0]
execute if score #_mb_cycle mgs.data matches 1.. run scoreboard players remove #_mb_cycle mgs.data 1
execute if score #_mb_cycle mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/cycle_iterate

