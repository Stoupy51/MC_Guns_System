
#> mgs:v5.0.0/multiplayer/editor/append_perk_line_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_perk_line with storage mgs:temp
#
# @args		_perk_val (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{"translate": "mgs.perk","color":"white"},{"text":"$(_perk_val)","color":"aqua"}]}
function mgs:v5.0.0/multiplayer/editor/append_perk_line

