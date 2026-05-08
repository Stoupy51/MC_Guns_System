
#> mgs:v5.0.1/zombies/revive/tick
#
# @within	mgs:v5.0.1/zombies/game_tick
#

# Process each spectating (downed) player
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] at @s run function mgs:v5.0.1/zombies/revive/downed_tick

