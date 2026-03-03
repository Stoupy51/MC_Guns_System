
#> mgs:v5.0.0/multiplayer/custom/notify_selected
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/apply_found with storage mgs:temp _find_iter[0]
#
# @args		name (unknown)
#

$tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.custom_loadout_applied","color":"white"},{"text":"$(name)","color":"green","bold":true}]

