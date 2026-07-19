
#> mgs:v5.1.0/zombies/dog_max_ammo_fallback
#
# @within	mgs:v5.1.0/zombies/round_complete
#

execute as @r[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/dog_max_ammo_at_self

