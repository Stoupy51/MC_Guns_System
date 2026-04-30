
#> mgs:v5.0.0/zombies/revive/solo_qr_complete
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/solo_qr_tick
#

# Consume one Quick Revive use
scoreboard players add @s mgs.zb.qr_uses 1

# Always remove the QR tag so the player must rebuy each time
tag @s remove mgs.perk.quick_revive

# If all 3 uses are exhausted, keep the perk score at 1 to permanently block rebuy
# Otherwise reset to 0 so the machine allows a new purchase
execute if score @s mgs.zb.qr_uses matches 3.. run scoreboard players set @s mgs.zb.perk.quick_revive 1
execute unless score @s mgs.zb.qr_uses matches 3.. run scoreboard players set @s mgs.zb.perk.quick_revive 0
execute if score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_exhausted_3_3_no_more_self_revives_this_game","color":"dark_red"}]
execute unless score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_used_2_3_rebuy_for_another_self_revive","color":"gray"}]

# Proceed with revive
function mgs:v5.0.0/zombies/revive/revive_complete

