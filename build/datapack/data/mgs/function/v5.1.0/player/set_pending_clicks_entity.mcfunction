
#> mgs:v5.1.0/player/set_pending_clicks_entity
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.1.0/right_click_entity
#

# Revoke this advancement, then run the normal click path (which revokes its own)
advancement revoke @s only mgs:v5.1.0/right_click_entity
function mgs:v5.1.0/player/set_pending_clicks

