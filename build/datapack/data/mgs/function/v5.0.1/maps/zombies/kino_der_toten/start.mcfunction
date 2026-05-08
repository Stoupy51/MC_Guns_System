
#> mgs:v5.0.1/maps/zombies/kino_der_toten/start
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/calls/start
#

# Kino der Toten map start script
# Called once when zombies game transitions to active
# @within  #mgs:maps/start_script (via calls/start)

# Initialize kino-specific data scores
scoreboard players set #kino_tp_state mgs.data 0
scoreboard players set #kino_tp_timer mgs.data 0
scoreboard players set #kino_tp_cd mgs.data 0
scoreboard players set #kino_met_count mgs.data 0

# Set the lobby to theater door closed
execute positioned ~-19 ~0 ~-1 run fill ~ ~ ~ ~2 ~2 ~ cobblestone

# Summon all interactions
## Teleporter
execute positioned ~-57 ~-1 ~9 run summon interaction ~ ~ ~ {Tags:["mgs.kino","mgs.kino.teleporter_theater","bs.entity.interaction"],width:1.0f,height:2.0f}
execute positioned ~ ~ ~ run summon interaction ~ ~ ~ {Tags:["mgs.kino","mgs.kino.teleporter_lobby","bs.entity.interaction"],width:1.0f,height:1.0f}

## Meteorites
execute positioned ~-12 ~0 ~-5 run summon interaction ~ ~ ~ {Tags:["mgs.kino","mgs.kino.meteorite_1","bs.entity.interaction"],width:1.1f,height:2.0f}
execute positioned ~-58 ~-2 ~-22 run summon interaction ~ ~ ~ {Tags:["mgs.kino","mgs.kino.meteorite_2","bs.entity.interaction"],width:1.1f,height:2.0f}
execute positioned ~-54 ~4 ~39 run summon interaction ~ ~ ~ {Tags:["mgs.kino","mgs.kino.meteorite_3","bs.entity.interaction"],width:1.1f,height:2.0f}

# Register right-click events for all kino interactions (target = interaction entity itself)
execute as @e[tag=mgs.kino] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.1/maps/zombies/kino_der_toten/on_right_click",executor:"target"}

