
#> mgs:v5.1.0/zombies/mystery_box/show_bear_result
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_result_one
#

function mgs:v5.1.0/zombies/mystery_box/close_lid

# Only the display tagged mb_bear moves, so other pulls are untouched.
tag @s add mgs.mb_bear

# Only the destination's grayed crate goes, once it is known (move_anim_transition).

loot replace entity @s contents loot mgs:zombies/roaming_bear
data merge entity @s {transformation:{translation:[0f,1.25f,0f],scale:[0.75f,0.75f,0.75f]}}

# The moving box eats the pull: refund the buyer.
scoreboard players operation #this_buyer mgs.data = @s mgs.mb.buyer
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config

# The move kills this display during the ascend phase.
scoreboard players set #mb_move_timer mgs.data 280

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_is_moving_2","color":"yellow","bold":true}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0

