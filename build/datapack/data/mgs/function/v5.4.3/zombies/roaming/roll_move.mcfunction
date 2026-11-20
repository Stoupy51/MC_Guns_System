
#> mgs:v5.4.3/zombies/roaming/roll_move
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/zombies/mystery_box/try_use
#			mgs:v5.4.3/zombies/wunderfizz/try_use
#

scoreboard players set #roam_will_move mgs.data 0
execute if score #roam_uses mgs.data >= #roam_threshold mgs.data store result score #roam_move_roll mgs.data run random value 0..2
execute if score #roam_uses mgs.data >= #roam_threshold mgs.data if score #roam_move_roll mgs.data matches 0 run scoreboard players set #roam_will_move mgs.data 1

