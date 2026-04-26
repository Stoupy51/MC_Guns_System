
#> mgs:v5.0.0/zombies/calc_zombie_hp_linear
#
# @within	mgs:v5.0.0/zombies/calc_zombie_hp
#

scoreboard players operation #zb_hp mgs.data = #zb_round mgs.data
scoreboard players remove #zb_hp mgs.data 1
scoreboard players operation #zb_hp mgs.data *= #100 mgs.data
scoreboard players operation #zb_hp mgs.data += #150 mgs.data
scoreboard players operation #zb_hp mgs.data *= #2 mgs.data
scoreboard players operation #zb_hp mgs.data /= #15 mgs.data

