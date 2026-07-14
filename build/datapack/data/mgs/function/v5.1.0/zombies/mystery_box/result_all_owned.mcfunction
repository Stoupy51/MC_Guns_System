
#> mgs:v5.1.0/zombies/mystery_box/result_all_owned
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_result_one
#

execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.pid = #this_buyer mgs.data run function mgs:v5.1.0/zombies/mystery_box/deny_all_owned

