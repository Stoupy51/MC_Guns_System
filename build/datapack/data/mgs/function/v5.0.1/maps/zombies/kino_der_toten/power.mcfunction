
#> mgs:v5.0.1/maps/zombies/kino_der_toten/power
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/calls/power
#

# Kino der Toten power-on script
# Called once when the power switch is activated
# @within  #mgs:maps/on_power (via calls/power)

# Open the lobby-to-theater door
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~2 ~2 ~ air

