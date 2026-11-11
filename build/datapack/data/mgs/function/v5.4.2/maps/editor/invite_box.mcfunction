
#> mgs:v5.4.2/maps/editor/invite_box
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/invite
#			mgs:v5.4.2/maps/editor/invite_box
#

data modify storage mgs:temp _inv.id set from storage mgs:temp _plr_iter[0].id
data modify storage mgs:temp _inv.name set from storage mgs:temp _plr_iter[0].name
function mgs:v5.4.2/maps/editor/invite_box_add with storage mgs:temp _inv
data remove storage mgs:temp _plr_iter[0]
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.4.2/maps/editor/invite_box

