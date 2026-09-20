
#> mgs:v5.1.0/zombies/whos_who/tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

execute as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}] at @s run function mgs:v5.1.0/zombies/whos_who/owner_tick

