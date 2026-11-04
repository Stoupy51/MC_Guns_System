
#> mgs:v5.3.0/player/set_pending_clicks_entity
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.3.0/right_click_entity
#			mgs:v5.3.0/dialog/close_then
#

# Revoked, then the normal click path runs (it revokes its own).
advancement revoke @s only mgs:v5.3.0/right_click_entity
function mgs:v5.3.0/player/set_pending_clicks

