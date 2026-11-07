
#> mgs:v5.4.0/maps/editor/invite_next
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/invite_selected
#			mgs:v5.4.0/maps/editor/invite_next
#

execute store result score #inv_id mgs.data run data get storage mgs:temp _inv_ids[0]
execute unless score #inv_id mgs.data matches 0 as @a if score @s bs.id = #inv_id mgs.data run function mgs:v5.4.0/players/editor_invite
data remove storage mgs:temp _inv_ids[0]
execute if data storage mgs:temp _inv_ids[0] run function mgs:v5.4.0/maps/editor/invite_next

