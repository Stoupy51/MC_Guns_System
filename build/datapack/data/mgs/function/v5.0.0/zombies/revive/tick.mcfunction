
#> mgs:v5.0.0/zombies/revive/tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Process each spectating (downed) player
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] at @s run function mgs:v5.0.0/zombies/revive/downed_tick

