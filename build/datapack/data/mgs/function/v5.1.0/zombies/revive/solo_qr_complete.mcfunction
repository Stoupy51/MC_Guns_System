
#> mgs:v5.1.0/zombies/revive/solo_qr_complete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/solo_qr_tick
#

# Consume one Quick Revive use
scoreboard players add @s mgs.zb.qr_uses 1

# Always remove the QR tags so the player must rebuy each time. perk.quick_revive is already gone
# (lose_all took it on the way down); zb_qr_armed is the snapshot this auto-revive ran on.
tag @s remove mgs.perk.quick_revive
tag @s remove mgs.zb_qr_armed

# Not owned any more either way. The exhausted case used to pin this score at 1 to block rebuy, but
# the score is what every ownership readout uses, so the perk stayed in the info paper and the perk
# item row after the last self-revive. mgs.zb.qr_uses is the cap now (perks/on_right_click).
scoreboard players set @s mgs.zb.perk.quick_revive 0
execute if score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_exhausted_3_3_no_more_self_revives_this_game","color":"dark_red"}]
execute unless score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_used_2_3_rebuy_for_another_self_revive","color":"gray"}]

# Proceed with revive
function mgs:v5.1.0/zombies/revive/revive_complete

## sourceMappingURL=solo_qr_complete.mcfunction.map
