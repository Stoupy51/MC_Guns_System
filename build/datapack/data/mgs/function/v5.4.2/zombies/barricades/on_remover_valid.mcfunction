
#> mgs:v5.4.2/zombies/barricades/on_remover_valid
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/barricades/handle_removing
#

# Run as the removing zombie, at it.
scoreboard players set #barricade_remover_valid mgs.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1

# This runs every tick of the 40-tick teardown, so the bang is rate-limited per listening player.
# `as` keeps the position, so ~ ~ ~ is still the zombie.
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.barricade.bang_at > #total_tick mgs.data run function mgs:v5.4.2/zombies/barricades/bang_for

