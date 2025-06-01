
#> mgs:v5.0.0/player/set_pending_clicks
#
# @within	advancement mgs:v5.0.0/right_click
#			advancement mgs:v5.0.0/alt_right_click
#


# Revoke advancement and reset right click
advancement revoke @s only mgs:v5.0.0/right_click
advancement revoke @s only mgs:v5.0.0/alt_right_click
scoreboard players reset @s mgs.right_click
scoreboard players reset @s mgs.alt_right_click

# Set pending clicks
scoreboard players set @s mgs.pending_clicks 4

