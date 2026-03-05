
#> mgs:v5.0.0/multiplayer/timer_display
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Convert ticks to seconds
execute store result score #_timer_sec mgs.data run scoreboard players get #mp_timer mgs.data
scoreboard players operation #_timer_sec mgs.data /= #20 mgs.data
execute store result score #_timer_min mgs.data run scoreboard players get #_timer_sec mgs.data
scoreboard players operation #_timer_min mgs.data /= #60 mgs.data
scoreboard players operation #_timer_mod mgs.data = #_timer_sec mgs.data
scoreboard players operation #_timer_mod mgs.data %= #60 mgs.data

# Zero-padded seconds for sidebar
scoreboard players operation #_timer_tens mgs.data = #_timer_mod mgs.data
scoreboard players operation #_timer_tens mgs.data /= #10 mgs.data
scoreboard players operation #_timer_ones mgs.data = #_timer_mod mgs.data
scoreboard players operation #_timer_ones mgs.data %= #10 mgs.data

# Refresh sidebar with updated values
function #bs.sidebar:refresh {objective:"mgs.sidebar"}

