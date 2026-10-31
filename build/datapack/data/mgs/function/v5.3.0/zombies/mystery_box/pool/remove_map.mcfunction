
#> mgs:v5.3.0/zombies/mystery_box/pool/remove_map
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/mystery_box/pool/clear_map with storage mgs:zombies game
#
# @args		map_id (unknown)
#

$data remove storage mgs:maps zombies[{id:"$(map_id)"}].mystery_box_pool
$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"$(map_id) uses the global mystery box pool again.","color":"green"}]

