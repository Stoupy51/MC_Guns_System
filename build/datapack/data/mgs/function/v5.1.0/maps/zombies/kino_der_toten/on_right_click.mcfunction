
#> mgs:v5.1.0/maps/zombies/kino_der_toten/on_right_click
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/start {run:"function mgs:v5.1.0/maps/zombies/kino_der_toten/on_right_click",executor:"target"} [ as @e[tag=mgs.kino] ]
#

# Run as the clicked interaction; `on target` reaches the player.
execute if entity @s[tag=mgs.kino.teleporter_theater] run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_theater_click
execute if entity @s[tag=mgs.kino.teleporter_lobby] run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_lobby_click
execute if entity @s[tag=mgs.kino.meteorite_1] run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag=mgs.kino.meteorite_2] run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/meteorite/on_click
execute if entity @s[tag=mgs.kino.meteorite_3] run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/meteorite/on_click

