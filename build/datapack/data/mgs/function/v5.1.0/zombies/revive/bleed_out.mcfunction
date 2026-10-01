
#> mgs:v5.1.0/zombies/revive/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#

scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Id-matched: two players downed together can be each other's nearest mannequin.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id

# Tombstone: snapshot the inventory while it is intact.
function mgs:v5.1.0/zombies/perks/tombstone_on_bleed_out

function mgs:v5.1.0/zombies/revive/hide_body

# Full spectator until the next round.
ride @s dismount
gamemode spectator @s

execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
# No alive player: stay where the camera was.
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_bled_out_respawning_next_round","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"dark_red"}],[{"text":" ","color":"gray"}, {"translate":"mgs.has_bled_out"}]]

