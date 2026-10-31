
#> mgs:v5.3.0/zombies/mystery_box/pool/store_map
#
# @within	mgs:v5.3.0/zombies/mystery_box/pool/save_map with storage mgs:zombies game
#
# @args		map_id (unknown)
#

$data modify storage mgs:maps zombies[{id:"$(map_id)"}].mystery_box_pool set from storage mgs:temp _mb_pool
$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"Mystery box pool saved for $(map_id); it applies from the next game.","color":"green"}]

