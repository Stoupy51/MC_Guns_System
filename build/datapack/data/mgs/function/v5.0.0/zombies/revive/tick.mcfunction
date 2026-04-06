
#> mgs:v5.0.0/zombies/revive/tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Process each downed player
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=1},gamemode=!spectator] at @s run function mgs:v5.0.0/zombies/revive/downed_tick

