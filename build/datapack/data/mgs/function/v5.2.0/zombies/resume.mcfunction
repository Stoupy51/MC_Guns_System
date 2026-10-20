
#> mgs:v5.2.0/zombies/resume
#
# @within	mgs:v5.2.0/zombies/suspended_tick
#

function mgs:v5.2.0/zombies/unfreeze_world
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_game_resumes","color":"green"}]

