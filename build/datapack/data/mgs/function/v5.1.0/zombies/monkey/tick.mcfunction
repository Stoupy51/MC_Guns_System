
#> mgs:v5.1.0/zombies/monkey/tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick [ at @s ]
#

# Attraction is a zombies-game mechanic only
execute unless data storage mgs:zombies game{state:"active"} run return 0

# Keep the paired taunt on the (bouncing/flying) grenade so enemies path to the right spot
scoreboard players operation #monkey_cur_id mgs.data = @s mgs.monkey_id
tag @s add mgs.monkey_here
execute as @e[tag=mgs.monkey_taunt,distance=..80] if score @s mgs.monkey_id = #monkey_cur_id mgs.data run tp @s @n[tag=mgs.monkey_here]
tag @s remove mgs.monkey_here

# Aggro pulse every second. The fuse score (@s mgs.data) starts at 180 and this runs before the
# decrement, so skipping 175.. gives pulses at 160, 140, ..., 20 — the first lands ~1s after the
# throw, once the monkey is away from the thrower.
scoreboard players operation #monkey_phase mgs.data = @s mgs.data
scoreboard players operation #monkey_phase mgs.data %= #20 mgs.data
execute if score #monkey_phase mgs.data matches 0 unless score @s mgs.data matches 175.. run function mgs:v5.1.0/zombies/monkey/pulse

