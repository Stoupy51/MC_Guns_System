
#> mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/deny_recharging
#
# @executed	as @e[tag=mgs.kino]
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_theater_click
#

# @s = interaction entity; reach the player via 'on target'
execute on target run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_teleporter_is_recharging","color":"yellow"}]
execute on target at @s run function mgs:v5.1.0/zombies/feedback/sound_deny

