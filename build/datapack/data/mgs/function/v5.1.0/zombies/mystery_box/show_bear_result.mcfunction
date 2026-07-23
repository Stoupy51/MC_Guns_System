
#> mgs:v5.1.0/zombies/mystery_box/show_bear_result
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_result_one
#

# Close this box's lid before it moves away
function mgs:v5.1.0/zombies/mystery_box/close_lid

# Mark this display as the moving bear so the move animation only touches it (not other pulls)
tag @s add mgs.mb_bear

# Hide every grayed disabled crate for the duration of the move (rebuilt when the box lands) so the
# destination spot doesn't show a disabled crate underneath the arriving chest.
kill @e[tag=mgs.mb_disabled]

# Replace display with teddy bear
loot replace entity @s contents loot mgs:zombies/roaming_bear
data merge entity @s {transformation:{translation:[0f,1.25f,0f],scale:[0.75f,0.75f,0.75f]}}

# Refund this box's buyer (the moving box eats the pull, no weapon given)
scoreboard players operation #this_buyer mgs.data = @s mgs.mb.buyer
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config

# Start move animation timer (this display is killed by the move at the ascend phase)
scoreboard players set #mb_move_timer mgs.data 280

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_is_moving_2","color":"yellow","bold":true}]
function mgs:v5.1.0/zombies/feedback/sound_box_bye_bye

