
#> mgs:v5.0.0/zombies/revive/progress_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick
#

# Increment revive progress
scoreboard players add @s mgs.zb.revive_p 1

# Check if revive is complete
# Use Quick Revive threshold if the reviver has the perk
execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] if score @s mgs.zb.revive_p matches 30.. run function mgs:v5.0.0/zombies/revive/revive_complete
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] if score @s mgs.zb.revive_p matches 60.. run function mgs:v5.0.0/zombies/revive/revive_complete

