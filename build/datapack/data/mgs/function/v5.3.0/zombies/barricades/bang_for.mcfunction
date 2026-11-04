
#> mgs:v5.3.0/zombies/barricades/bang_for
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/barricades/on_remover_valid [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] ]
#

scoreboard players operation @s mgs.zb.barricade.bang_at = #total_tick mgs.data
scoreboard players add @s mgs.zb.barricade.bang_at 35
playsound mgs:zombies/barricade/bang block @s ~ ~ ~ 1.0 1.0

