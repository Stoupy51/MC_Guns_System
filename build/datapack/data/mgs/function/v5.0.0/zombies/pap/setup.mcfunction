
#> mgs:v5.0.0/zombies/pap/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

scoreboard players set #pap_counter mgs.data 0
data modify storage mgs:zombies pap_data set value {}
data modify storage mgs:temp _pap_iter set from storage mgs:zombies game.map.pap_machines
execute if data storage mgs:temp _pap_iter[0] run function mgs:v5.0.0/zombies/pap/setup_iter

