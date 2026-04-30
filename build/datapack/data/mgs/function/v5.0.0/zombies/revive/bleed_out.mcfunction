
#> mgs:v5.0.0/zombies/revive/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Kill mannequin, HUD display, and camera entity
kill @n[tag=mgs.downed_mannequin]
kill @n[tag=mgs.downed_hud]
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_cam] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run kill @s

# Dismount then enter full spectator mode to watch until next round
ride @s dismount
gamemode spectator @s

# Spectate a random alive in-game player
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
# Fallback if no alive players: teleport spectator somewhere reasonable
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title [{"text":"☠","color":"dark_red"}]
title @s subtitle [{"translate":"mgs.you_bled_out_respawning_next_round","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"dark_red"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_bled_out"}]]

