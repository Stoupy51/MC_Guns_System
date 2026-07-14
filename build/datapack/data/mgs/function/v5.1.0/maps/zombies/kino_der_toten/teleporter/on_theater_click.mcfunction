
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_theater_click
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/on_right_click
#

# State 0 (idle): start linking — player must now click the lobby pad
execute if score #kino_tp_state mgs.data matches 0 run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/start_link
# State 2 (armed): lobby was linked, execute the actual teleport
execute if score #kino_tp_state mgs.data matches 2 at @s run return run function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/activate
# Any other state (linking/active/returning/cooldown): deny
function mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/deny_recharging

