
#> mgs:v5.4.2/zombies/mystery_box/sink_fast
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/move_anim_descend_step [ as @e[tag=...] & at @s ]
#

execute if score @s mgs.mb.roll matches 0 run tp @s ^ ^-0.18 ^
execute if score @s mgs.mb.roll matches 1 run tp @s ^0.18 ^ ^
execute if score @s mgs.mb.roll matches 2 run tp @s ^ ^0.18 ^
execute if score @s mgs.mb.roll matches 3 run tp @s ^-0.18 ^ ^

