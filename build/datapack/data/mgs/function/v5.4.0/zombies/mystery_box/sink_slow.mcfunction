
#> mgs:v5.4.0/zombies/mystery_box/sink_slow
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/mystery_box/move_anim_descend_step [ as @e[tag=...] & at @s ]
#

execute if score @s mgs.mb.roll matches 0 run tp @s ^ ^-0.06 ^
execute if score @s mgs.mb.roll matches 1 run tp @s ^0.06 ^ ^
execute if score @s mgs.mb.roll matches 2 run tp @s ^ ^0.06 ^
execute if score @s mgs.mb.roll matches 3 run tp @s ^-0.06 ^ ^

