
#> mgs:v5.0.0/zombies/revive/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed

# Remove downed effects
effect clear @s slowness
effect clear @s weakness
effect clear @s mining_fatigue

# Restore health base before going to spectator
attribute @s minecraft:max_health base set 20

# Set player to spectator until next round
gamemode spectator @s

# Spectate a random alive in-game player (prefer non-downed)
execute at @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]

# Announce
title @s title [{"text":"\u2620","color":"dark_red"}]
title @s subtitle [{"translate":"mgs.you_bled_out_respawning_next_round","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"dark_red"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_bled_out"}]]

