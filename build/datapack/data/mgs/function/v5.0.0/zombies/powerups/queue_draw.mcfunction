
#> mgs:v5.0.0/zombies/powerups/queue_draw
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/powerups/check_drop
#

# Get current bag size (0 = empty or unset)
execute store result score #pu_q_len mgs.data run data get storage mgs:data _pu_queue

# Refill if empty
execute if score #pu_q_len mgs.data matches ..0 run function mgs:v5.0.0/zombies/powerups/queue_refill
execute if score #pu_q_len mgs.data matches ..0 run execute store result score #pu_q_len mgs.data run data get storage mgs:data _pu_queue

# Pick a random index within [0, size-1]
execute if score #pu_q_len mgs.data matches 1 store result score #pu_q_idx mgs.data run random value 0..0
execute if score #pu_q_len mgs.data matches 2 store result score #pu_q_idx mgs.data run random value 0..1
execute if score #pu_q_len mgs.data matches 3 store result score #pu_q_idx mgs.data run random value 0..2
execute if score #pu_q_len mgs.data matches 4 store result score #pu_q_idx mgs.data run random value 0..3
execute if score #pu_q_len mgs.data matches 5 store result score #pu_q_idx mgs.data run random value 0..4
execute if score #pu_q_len mgs.data matches 6 store result score #pu_q_idx mgs.data run random value 0..5
execute if score #pu_q_len mgs.data matches 7 store result score #pu_q_idx mgs.data run random value 0..6
execute if score #pu_q_len mgs.data matches 8 store result score #pu_q_idx mgs.data run random value 0..7
execute if score #pu_q_len mgs.data matches 9 store result score #pu_q_idx mgs.data run random value 0..8

# Store index into temp storage for macro call, then extract and remove
execute store result storage mgs:temp _pu_q.idx int 1 run scoreboard players get #pu_q_idx mgs.data
function mgs:v5.0.0/zombies/powerups/queue_extract with storage mgs:temp _pu_q

