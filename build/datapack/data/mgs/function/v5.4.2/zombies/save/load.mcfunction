
#> mgs:v5.4.2/zombies/save/load
#
# @within	mgs:v5.4.2/dialog/close_then
#
# @args		slot (unknown)
#

execute unless data storage mgs:zombies game{state:"lobby"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.a_zombies_game_is_running_stop_it_before_loading_a_save","fallback":"A zombies game is running: stop it before loading a save.","color":"red"}]
$data modify storage mgs:zombies_saves loading set from storage mgs:zombies_saves slots[$(slot)]
execute unless data storage mgs:zombies_saves loading.format run return run function mgs:v5.4.2/zombies/save/load_refused {reason:"This slot is empty."}
execute unless data storage mgs:zombies_saves loading{format:1} run return run function mgs:v5.4.2/zombies/save/load_refused {reason:"This save comes from a newer version of the pack."}

data modify storage mgs:temp _sv_map.map_id set from storage mgs:zombies_saves loading.map_id
function mgs:v5.4.2/zombies/load_map_from_storage with storage mgs:temp _sv_map
data remove storage mgs:temp map_load
execute unless score #map_load_found mgs.data matches 1 run return run function mgs:v5.4.2/zombies/save/load_refused {reason:"The map of this save no longer exists."}

# The saved players online join whoever is already in the game.
execute as @a run function mgs:v5.4.2/zombies/save/enlist_player
execute unless entity @a[scores={mgs.zb.in_game=1}] run return run function mgs:v5.4.2/zombies/save/load_refused {reason:"No player of this save is online."}

data modify storage mgs:zombies game.map_id set from storage mgs:zombies_saves loading.map_id
data modify storage mgs:zombies game.variant set from storage mgs:zombies_saves loading.variant
function mgs:v5.4.2/zombies/start
execute unless data storage mgs:zombies game{state:"preparing"} run data remove storage mgs:zombies_saves loading

