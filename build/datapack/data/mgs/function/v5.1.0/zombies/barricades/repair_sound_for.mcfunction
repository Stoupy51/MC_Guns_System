
#> mgs:v5.1.0/zombies/barricades/repair_sound_for
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32]
#
# @within	mgs:v5.1.0/zombies/barricades/start_repairing_player [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] ]
#

scoreboard players operation @s mgs.zb.barricade.rep_at = #total_tick mgs.data
scoreboard players add @s mgs.zb.barricade.rep_at 80
playsound mgs:zombies/barricade/repair_no_cash block @s ~ ~ ~ 1.0 1.0

