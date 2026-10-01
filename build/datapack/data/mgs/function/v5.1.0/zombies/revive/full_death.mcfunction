
#> mgs:v5.1.0/zombies/revive/full_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/check_bounds_player
#

# A doppelganger forfeits their unrevived body, as when going down again.
execute if entity @s[tag=mgs.ww_active] run function mgs:v5.1.0/zombies/whos_who/forfeit

# A revive perk saves the player instead, checked before lose_all. Who's Who first (as in on_down): the body drops at a spawn;
# then solo Quick Revive with uses left: spend one and respawn at a spawn.
execute if score @s mgs.zb.perk.whos_who matches 1 run return run function mgs:v5.1.0/zombies/revive/void_revive_whos_who
execute store result score #zb_ingame_total mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if entity @s[tag=mgs.perk.quick_revive] if score #zb_ingame_total mgs.data matches ..1 unless score @s mgs.zb.qr_uses matches 3.. run return run function mgs:v5.1.0/zombies/revive/void_revive_solo_qr

# Counts as a down and strips perks.
scoreboard players add @s mgs.zb.downs 1
function mgs:v5.1.0/zombies/perks/lose_all

# No mannequin exists on this path.
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Respawned at round end.
gamemode spectator @s
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_fell_out_of_the_world","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"dark_red"}],[{"text":" ","color":"gray"}, {"translate":"mgs.fell_out_of_the_world"}]]

