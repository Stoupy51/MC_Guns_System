
#> mgs:v5.1.0/zoom/clear_state
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/on_weapon_switch
#

playsound mgs:common/lean_out player @s
scoreboard players reset @s mgs.zoom
scoreboard players set @s mgs.zoom_timer 0
effect clear @s slowness

