
#> mgs:v5.0.0/zombies/mystery_box/maybe_move_after_pull
#
# @within	mgs:v5.0.0/zombies/mystery_box/collect
#

scoreboard players add #mb_pulls mgs.data 1

# Every 4 successful pulls, roll a 1/3 chance to move.
execute if score #mb_pulls mgs.data matches 4.. store result score #mb_move_roll mgs.data run random value 0..2
execute if score #mb_pulls mgs.data matches 4.. if score #mb_move_roll mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/move_active_position
execute if score #mb_pulls mgs.data matches 4.. run scoreboard players set #mb_pulls mgs.data 0

