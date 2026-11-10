
#> mgs:v5.4.1/multiplayer/kill_cam/on_death
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/enter_death_spectate
#

execute unless score #kc_window mgs.data matches 1 run return run function mgs:v5.4.1/multiplayer/kill_cam/check_window

# Once the match is decided only its deciding kill is logged, #kc_final going from 1 to 2 (see multiplayer/request_end).
execute if score #mp_end_tick mgs.data matches 1.. unless score #kc_final mgs.data matches 1 run return fail
execute if score #kc_final mgs.data matches 1 run scoreboard players set #kc_final mgs.data 2

data modify storage mgs:kill_cam deaths append value {}
execute store result storage mgs:kill_cam deaths[-1].t int 1 run scoreboard players get #total_tick mgs.data
execute store result storage mgs:kill_cam deaths[-1].victim int 1 run scoreboard players get @s bs.id
execute as @a[tag=mgs.temp_killer,limit=1] store result storage mgs:kill_cam deaths[-1].killer int 1 run scoreboard players get @s bs.id

