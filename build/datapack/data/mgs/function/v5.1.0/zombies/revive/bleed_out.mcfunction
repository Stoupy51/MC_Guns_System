
#> mgs:v5.1.0/zombies/revive/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Hide THIS player's mannequin and HUD (id-matched: a "nearest" lookup could hide another downed
# player's mannequin when both went down together)
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id

# Tombstone: snapshot the inventory now (still intact) if a marker is waiting for this player
function mgs:v5.1.0/zombies/perks/tombstone_on_bleed_out

function mgs:v5.1.0/zombies/revive/hide_body

# Dismount then enter full spectator mode to watch until next round
ride @s dismount
gamemode spectator @s

# Spectate a random alive in-game player
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
# Fallback if no alive players: teleport spectator somewhere reasonable
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_bled_out_respawning_next_round","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"dark_red"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_bled_out"}]]

