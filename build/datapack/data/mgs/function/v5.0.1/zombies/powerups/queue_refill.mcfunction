
#> mgs:v5.0.1/zombies/powerups/queue_refill
#
# @within	mgs:v5.0.1/zombies/start_round
#			mgs:v5.0.1/zombies/powerups/queue_draw
#

data modify storage mgs:data _pu_queue set value []

# Always include common power-ups in every cycle
data modify storage mgs:data _pu_queue append value 1
data modify storage mgs:data _pu_queue append value 2
data modify storage mgs:data _pu_queue append value 3
data modify storage mgs:data _pu_queue append value 4
data modify storage mgs:data _pu_queue append value 5

# Each rare power-up has an independent 25% chance to join this cycle
execute if score #zb_round mgs.data matches 6.. store result score #pu_rare_roll_6 mgs.data run random value 1..100
execute if score #zb_round mgs.data matches 6.. if score #pu_rare_roll_6 mgs.data matches 1..25 run data modify storage mgs:data _pu_queue append value 6
execute if score #zb_round mgs.data matches 6.. store result score #pu_rare_roll_7 mgs.data run random value 1..100
execute if score #zb_round mgs.data matches 6.. if score #pu_rare_roll_7 mgs.data matches 1..25 run data modify storage mgs:data _pu_queue append value 7
execute if score #zb_round mgs.data matches 6.. store result score #pu_rare_roll_8 mgs.data run random value 1..100
execute if score #zb_round mgs.data matches 6.. if score #pu_rare_roll_8 mgs.data matches 1..25 run data modify storage mgs:data _pu_queue append value 8
execute if score #zb_round mgs.data matches 6.. store result score #pu_rare_roll_9 mgs.data run random value 1..100
execute if score #zb_round mgs.data matches 6.. if score #pu_rare_roll_9 mgs.data matches 1..25 run data modify storage mgs:data _pu_queue append value 9
execute if score #zb_round mgs.data matches 6.. store result score #pu_rare_roll_10 mgs.data run random value 1..100
execute if score #zb_round mgs.data matches 6.. if score #pu_rare_roll_10 mgs.data matches 1..25 run data modify storage mgs:data _pu_queue append value 10

