
#> mgs:v5.1.0/zombies/revive/full_death
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/check_bounds_player
#

# A doppelganger's unrevived body is forfeited (same rule as going down again)
execute if entity @s[tag=mgs.ww_active] run function mgs:v5.1.0/zombies/whos_who/forfeit

# A revive perk saves you from the void instead of a full elimination. Checked BEFORE lose_all
# strips the perks. Who's Who takes priority over solo Quick Revive (same order as revive/on_down):
# - Who's Who: keep playing as a doppelganger; the body can't live in the void, so it drops at a spawn.
# - Solo Quick Revive: in a solo game with uses left, spend one and respawn at a spawn point.
execute if score @s mgs.zb.perk.whos_who matches 1 run return run function mgs:v5.1.0/zombies/revive/void_revive_whos_who
execute store result score #zb_ingame_total mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if entity @s[tag=mgs.perk.quick_revive] if score #zb_ingame_total mgs.data matches ..1 unless score @s mgs.zb.qr_uses matches 3.. run return run function mgs:v5.1.0/zombies/revive/void_revive_solo_qr

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

