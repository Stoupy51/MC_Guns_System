
#> mgs:v5.0.1/maps/zombies/kino_der_toten/meteorite/play_song
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/meteorite/on_click
#

# Play 115 for all in-game players at their own position
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/music/115_song record @s ~ ~ ~ 0.5 1

