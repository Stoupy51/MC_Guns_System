
#> mgs:v5.0.1/zombies/create_sidebar
#
# @within	mgs:v5.0.1/zombies/preload_complete
#

scoreboard objectives add mgs.zb_sidebar dummy

# Seed the displayed round to the upcoming round (game.round + 1) so the sidebar
# shows "Round 1" immediately during prep instead of a stale value until start_round runs
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 1

# Prep context: game_tick isn't maintaining #zb_alive yet (and a previous game may have left a
# stale value), so seed it once here before the (now rescan-free) refresh_sidebar.
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]

function mgs:v5.0.1/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar mgs.zb_sidebar

