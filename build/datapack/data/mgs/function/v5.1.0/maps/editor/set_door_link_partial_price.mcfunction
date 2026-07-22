
#> mgs:v5.1.0/maps/editor/set_door_link_partial_price
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.1.0/maps/editor/show_element_config {partial_price:0}"}, "hover_event": {"action": "show_text", "value": "Sets partial_price on ALL doors with same link_id"}}, "\u270e", "]"],"  ",{"text":"ⓘ","color":"aqua","hover_event":{"action":"show_text","value":"Chip-in payments: points taken per right-click (0 = pay the full price at once).\nExample: price 5000 + partial_price 500 = 10 payments.\nDoor progress is GLOBAL — any mix of players can contribute, and the last\npayment is just whatever is left. Progress is shared by every linked door."}}]
#
# @args		partial_price (int)
#

$data modify storage mgs:temp _door_set set value {field:"partial_price",value:$(partial_price)}
function mgs:v5.1.0/maps/editor/set_door_link_apply

