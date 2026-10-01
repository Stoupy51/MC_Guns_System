
#> mgs:v5.1.0/zombies/create_sidebar
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

scoreboard objectives add mgs.zb_sidebar dummy

# Shows the upcoming round (game.round + 1) during prep.
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 1

# game_tick does not maintain #zb_alive during prep, and a previous game may have left it stale.
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]

function mgs:v5.1.0/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar mgs.zb_sidebar

