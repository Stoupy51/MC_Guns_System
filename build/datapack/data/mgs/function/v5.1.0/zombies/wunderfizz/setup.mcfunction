
#> mgs:v5.1.0/zombies/wunderfizz/setup
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

scoreboard players set #wf_counter mgs.data 0
data modify storage mgs:temp _wf_iter set from storage mgs:zombies game.map.wunderfizz
execute if data storage mgs:temp _wf_iter[0] run function mgs:v5.1.0/zombies/wunderfizz/setup_iter

