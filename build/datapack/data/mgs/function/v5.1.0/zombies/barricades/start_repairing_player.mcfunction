
#> mgs:v5.1.0/zombies/barricades/start_repairing_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/find_repairer
#

# Run as the player assigned as repairer, at the barricade.
tag @s add mgs.barricade_repairing
scoreboard players operation @s mgs.zb.barricade.repairing_id = #barricade_id mgs.data
scoreboard players set #barricade_found_repairer mgs.data 1

# Played once: the clip lasts longer than the 30-tick repair.
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.barricade.rep_at > #total_tick mgs.data run function mgs:v5.1.0/zombies/barricades/repair_sound_for

