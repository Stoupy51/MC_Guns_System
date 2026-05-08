
#> mgs:v5.0.1/maps/zombies/kino_der_toten/meteorite/on_click
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/on_right_click
#

# @s = interaction entity itself
# Guard: this meteorite is already activated
execute if entity @s[tag=mgs.kino.met_active] run return fail

# Mark meteorite as activated and increment counter
tag @s add mgs.kino.met_active
scoreboard players add #kino_met_count mgs.data 1

# On third meteorite: play the 115 song
execute if score #kino_met_count mgs.data matches 3 run function mgs:v5.0.1/maps/zombies/kino_der_toten/meteorite/play_song

