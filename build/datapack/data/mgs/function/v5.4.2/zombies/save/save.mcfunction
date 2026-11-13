
#> mgs:v5.4.2/zombies/save/save
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/request {slot:$(slot),name:"$(name)"}
#			string in mgs:v5.4.2/zombies/save/request {slot:$(slot),name:\"$(name)\"}
#
# @args		name (string)
#			slot (int)
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_zombies_game_is_active","fallback":"No zombies game is active.","color":"red"}]
execute unless score #zb_next_round mgs.data matches 1.. run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.a_game_can_only_be_saved_between_two_rounds","fallback":"A game can only be saved between two rounds.","color":"red"}]

$data modify storage mgs:zombies_saves _slot set value {format:1,pack:"5.4.2",name:"$(name)",players:[],map:{opened:[]}}
data modify storage mgs:zombies_saves _slot.map_id set from storage mgs:zombies game.map_id
data modify storage mgs:zombies_saves _slot.variant set from storage mgs:zombies game.variant
data modify storage mgs:zombies_saves _slot.round set from storage mgs:zombies game.round
execute store result storage mgs:zombies_saves _slot.saved_at long 1 run time query gametime

execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.4.2/zombies/save/capture_player
function mgs:v5.4.2/zombies/save/capture_map

$data modify storage mgs:zombies_saves slots[$(slot)] set from storage mgs:zombies_saves _slot
data remove storage mgs:zombies_saves _slot

$tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.game_saved_as","fallback":"Game saved as ","color":"green"},{"text":"$(name)","color":"gold"},{"text":".","color":"green"}]
function mgs:v5.4.2/zombies/stop

