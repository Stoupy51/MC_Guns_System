
#> mgs:v5.1.0/zombies/revive/full_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/check_bounds_player
#

# Count it as a down and strip perks (same as a normal down/bleed-out)
scoreboard players add @s mgs.zb.downs 1
function mgs:v5.1.0/zombies/perks/lose_all

# Defensively clear any downed state (no mannequin is created on this path)
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Enter spectator and watch a random alive teammate (respawn handled at round end)
gamemode spectator @s
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_fell_out_of_the_world","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"dark_red"},[{"text":" ","color":"gray"}, {"translate":"mgs.fell_out_of_the_world"}]]

