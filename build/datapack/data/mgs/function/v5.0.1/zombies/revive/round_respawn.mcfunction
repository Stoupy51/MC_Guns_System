
#> mgs:v5.0.1/zombies/revive/round_respawn
#
# @within	mgs:v5.0.1/zombies/round_complete
#

# Respawn all spectator (bled-out) players
execute as @a[scores={mgs.zb.in_game=1},gamemode=spectator] run function mgs:v5.0.1/zombies/revive/do_round_respawn

