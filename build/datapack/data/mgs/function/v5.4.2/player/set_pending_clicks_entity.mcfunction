
#> mgs:v5.4.2/player/set_pending_clicks_entity
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.4.2/right_click_entity
#			mgs:v5.4.2/dialog/close_then
#

# Revoked, then the normal click path runs (it revokes its own).
advancement revoke @s only mgs:v5.4.2/right_click_entity
function mgs:v5.4.2/player/set_pending_clicks

