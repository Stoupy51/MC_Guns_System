
#> mgs:v5.1.0/maps/zombies/kino_der_toten/meteorite/play_song
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/meteorite/on_click
#

# Play 115 for all in-game players at their own position
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/music/115_song record @s ~ ~ ~ 0.2 1

# Allow replaying the song by resetting meteorite states and counter
tag @e[tag=mgs.kino.met_active] remove mgs.kino.met_active
scoreboard players set #kino_met_count mgs.data 0

