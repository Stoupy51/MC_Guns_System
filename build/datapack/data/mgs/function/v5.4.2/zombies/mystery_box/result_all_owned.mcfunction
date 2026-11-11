
#> mgs:v5.4.2/zombies/mystery_box/result_all_owned
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/show_result_one
#

execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run function mgs:v5.4.2/zombies/deny/message {msg:'{"translate":"mgs.you_already_own_all_available_mystery_box_weapons_points_refunde","fallback":"You already own all available Mystery Box weapons. Points refunded.","color":"yellow"}'}

