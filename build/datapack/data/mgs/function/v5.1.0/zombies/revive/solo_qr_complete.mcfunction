
#> mgs:v5.1.0/zombies/revive/solo_qr_complete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/solo_qr_tick
#

scoreboard players add @s mgs.zb.qr_uses 1

# The perk must be rebought after each use; lose_all already took perk.quick_revive.
tag @s remove mgs.perk.quick_revive
tag @s remove mgs.zb_qr_armed

# mgs.zb.qr_uses caps the uses (see perks/on_right_click).
scoreboard players set @s mgs.zb.perk.quick_revive 0
execute if score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_exhausted_3_3_no_more_self_revives_this_game","color":"dark_red"}]
execute unless score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_used_2_3_rebuy_for_another_self_revive","color":"gray"}]

function mgs:v5.1.0/zombies/revive/revive_complete

