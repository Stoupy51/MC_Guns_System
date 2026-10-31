
#> mgs:v5.3.0/zombies/mystery_box/rise_slow
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.3.0/zombies/mystery_box/move_anim_ascend_step [ as @e[tag=...] & at @s ]
#			mgs:v5.3.0/zombies/mystery_box/move_anim_ascend_step [ as @e[tag=mgs.mb_bear] & at @s ]
#

execute if score @s mgs.mb.roll matches 0 run tp @s ^ ^0.06 ^
execute if score @s mgs.mb.roll matches 1 run tp @s ^-0.06 ^ ^
execute if score @s mgs.mb.roll matches 2 run tp @s ^ ^-0.06 ^
execute if score @s mgs.mb.roll matches 3 run tp @s ^0.06 ^ ^

