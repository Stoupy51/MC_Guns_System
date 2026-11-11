
#> mgs:v5.4.2/multiplayer/kill_cam/on_shoot
#
# @within	#mgs:signals/on_shoot
#			mgs:v5.4.2/dialog/close_then
#

execute unless score #kc_window mgs.data matches 1 run return fail
execute unless entity @s[type=player,scores={mgs.mp.in_game=1}] run return fail
data modify storage mgs:kill_cam pending_shots append value {}
execute store result storage mgs:kill_cam pending_shots[-1].id int 1 run scoreboard players get @s bs.id
data modify storage mgs:kill_cam pending_shots[-1].snd set from storage mgs:signals on_shoot.weapon.sounds.fire

