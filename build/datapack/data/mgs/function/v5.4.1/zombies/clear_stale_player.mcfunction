
#> mgs:v5.4.1/zombies/clear_stale_player
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/on_rejoin
#

function mgs:v5.4.1/zombies/reset_player
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_zombies_game_you_were_in_ended_while_you_were_away","fallback":"The zombies game you were in ended while you were away.","color":"gray"}]

