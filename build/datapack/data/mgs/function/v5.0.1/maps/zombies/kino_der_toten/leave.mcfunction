
#> mgs:v5.0.1/maps/zombies/kino_der_toten/leave
#
# @within	mgs:v5.0.1/maps/zombies/kino_der_toten/calls/leave
#

# Kino der Toten map leave script (game ended / cleanup)
# @within  #mgs:maps/leave_script (via calls/leave)

# Kill all kino interaction entities
kill @e[tag=mgs.kino]

# Remove in-teleporter tag from all players
tag @a remove mgs.kino.in_tp

# Reset kino data scores
scoreboard players set #kino_tp_state mgs.data 0
scoreboard players set #kino_tp_timer mgs.data 0
scoreboard players set #kino_tp_cd mgs.data 0
scoreboard players set #kino_met_count mgs.data 0

