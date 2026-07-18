
#> mgs:v5.1.0/multiplayer/assign_bphase
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enforce_bounds
#

scoreboard players operation @s mgs.mp.bphase = #bphase_next mgs.data
scoreboard players add #bphase_next mgs.data 1
scoreboard players operation #bphase_next mgs.data %= #4 mgs.data

