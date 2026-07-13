
#> mgs:v5.0.1/zombies/revive/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/revive/downed_tick
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Hide THIS player's mannequin and HUD by teleporting far below the world (id-matched: a
# "nearest" lookup could hide another downed player's mannequin when both went down together)
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] add mgs.downed_mine_temp
tp @n[tag=mgs.downed_mine_temp] ~ -10000 ~
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag=mgs.downed_mine_temp] remove mgs.downed_mannequin
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] run tag @s remove mgs.downed_hud
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] run kill @s

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

