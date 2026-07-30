
#> mgs:v5.1.0/zombies/barricades/start_repairing_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/find_repairer
#

# @s = player assigned as repairer, execution position = the barricade (find_repairer runs at it)
tag @s add mgs.barricade_repairing
scoreboard players operation @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data
scoreboard players set #barricade_found_repairer mgs.data 1

# Hammering, started once here rather than ticked from on_repairer_valid: the clip already runs longer
# than the 30-tick repair, so one play covers the whole action.
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.barricade.rep_at > #total_tick mgs.data run function mgs:v5.1.0/zombies/barricades/repair_sound_for

