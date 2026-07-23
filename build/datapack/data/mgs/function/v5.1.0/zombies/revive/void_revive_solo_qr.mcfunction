
#> mgs:v5.1.0/zombies/revive/void_revive_solo_qr
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/full_death
#

# Consume one Quick Revive use (same rebuy bookkeeping as solo_qr_complete)
scoreboard players add @s mgs.zb.qr_uses 1
tag @s remove mgs.perk.quick_revive
execute if score @s mgs.zb.qr_uses matches 3.. run scoreboard players set @s mgs.zb.perk.quick_revive 1
execute unless score @s mgs.zb.qr_uses matches 3.. run scoreboard players set @s mgs.zb.perk.quick_revive 0
execute if score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_exhausted_3_3_no_more_self_revives_this_game","color":"dark_red"}]
execute unless score @s mgs.zb.qr_uses matches 3.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.quick_revive_used_2_3_rebuy_for_another_self_revive","color":"gray"}]

# Count the down and strip perks (any down loses them), then clear any downed state defensively
scoreboard players add @s mgs.zb.downs 1
function mgs:v5.1.0/zombies/perks/lose_all
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Respawn at a safe spawn, healthy
gamemode adventure @s
function mgs:v5.1.0/zombies/revive/respawn_near_player
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s mgs.stam_seen 0

# Announce
title @s times 5 40 15
title @s title ["⚡"]
title @s subtitle [{"translate":"mgs.quick_revive_pulled_you_back_from_the_void","color":"aqua"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"aqua"},{"translate":"mgs.fell_out_but_quick_revive_pulled_them_back","color":"gray"}]

