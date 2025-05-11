
#> stoupgun:v5.0.0/right_click/set_pending_clicks
#
# @within	advancement stoupgun:v5.0.0/right_click
#

# Revoke advancement
advancement revoke @s only stoupgun:right_click

# Set pending clicks and reset right click
scoreboard players set @s stoupgun.pending_clicks 4
scoreboard players reset @s stoupgun.right_click

