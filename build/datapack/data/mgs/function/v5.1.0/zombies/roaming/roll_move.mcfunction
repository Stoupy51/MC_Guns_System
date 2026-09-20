
#> mgs:v5.1.0/zombies/roaming/roll_move
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/try_use
#			mgs:v5.1.0/zombies/wunderfizz/try_use
#

scoreboard players set #roam_will_move mgs.data 0
execute if score #roam_uses mgs.data >= #roam_threshold mgs.data store result score #roam_move_roll mgs.data run random value 0..2
execute if score #roam_uses mgs.data >= #roam_threshold mgs.data if score #roam_move_roll mgs.data matches 0 run scoreboard players set #roam_will_move mgs.data 1

