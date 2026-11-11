
#> mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/on_theater_click
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/zombies/kino_der_toten/on_right_click
#

# State 0 (idle): start linking, the player must now click the lobby pad.
execute if score #kino_tp_state mgs.data matches 0 run return run function mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/start_link
# State 2 (armed): teleport.
execute if score #kino_tp_state mgs.data matches 2 at @s run return run function mgs:v5.4.2/maps/zombies/kino_der_toten/teleporter/activate
# States 1 and 3 to 6 (linking, active, returning, cooldown): deny.
execute on target at @s run function mgs:v5.4.2/zombies/deny/message {msg:'{"translate":"mgs.the_teleporter_is_recharging","fallback":"The teleporter is recharging...","color":"yellow"}'}

