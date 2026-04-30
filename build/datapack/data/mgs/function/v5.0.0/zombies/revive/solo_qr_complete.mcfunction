
#> mgs:v5.0.0/zombies/revive/solo_qr_complete
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/solo_qr_tick
#

# Consume one Quick Revive use
scoreboard players add @s mgs.zb.qr_uses 1

# If used up all 3, remove the Quick Revive perk
execute if score @s mgs.zb.qr_uses matches 3.. run tag @s remove mgs.perk.quick_revive
execute if score @s mgs.zb.qr_uses matches 3.. run scoreboard players set @s mgs.zb.perk.quick_revive 0
execute if score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.quick_revive_used_up","color":"gray"}, "! (3/3)"]]

# Proceed with revive
function mgs:v5.0.0/zombies/revive/revive_complete

