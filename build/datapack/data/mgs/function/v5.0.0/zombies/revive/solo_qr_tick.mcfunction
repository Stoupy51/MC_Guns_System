
#> mgs:v5.0.0/zombies/revive/solo_qr_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/check_solo_qr
#

# Check player has uses remaining
execute if score @s mgs.zb.qr_uses matches 3.. run return 0

# Signal solo reviving so decay logic is skipped (set #zb_reviving=2)
scoreboard players set #zb_reviving mgs.data 2

# Increment revive_p at normal speed (1/tick)
scoreboard players add @s mgs.zb.revive_p 1

# Show solo QR auto-revive actionbar with seconds display
scoreboard players operation #rv_qr_sec mgs.data = @s mgs.zb.revive_p
scoreboard players operation #rv_qr_sec mgs.data /= #20 mgs.data
scoreboard players operation #rv_qr_tenth mgs.data = @s mgs.zb.revive_p
scoreboard players operation #rv_qr_tenth mgs.data %= #20 mgs.data
scoreboard players operation #rv_qr_tenth mgs.data /= #2 mgs.data
data modify storage smithed.actionbar:input message set value {json:[[{"text":"⚡ ","color":"aqua"}, {"translate":"mgs.solo_quick_revive"}],{"score":{"name":"#rv_qr_sec","objective":"mgs.data"},"color":"green"},{"text":".","color":"green"},{"score":{"name":"#rv_qr_tenth","objective":"mgs.data"},"color":"green"},{"translate":"mgs.s_10_0s","color":"gray"}],priority:"override",freeze:2}
function #smithed.actionbar:message

# Auto-revive once threshold reached
execute if score @s mgs.zb.revive_p matches 200.. run function mgs:v5.0.0/zombies/revive/solo_qr_complete

