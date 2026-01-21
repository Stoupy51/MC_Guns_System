
#> mgs:v5.0.0/player/set_pending_clicks
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.0.0/right_click
#			advancement mgs:v5.0.0/alt_right_click
#

# Detect if player is holding right-click (vs single tap)
# If pending_clicks is still non-negative when new click arrives, player is holding
# (Minecraft increments every 4-5 ticks randomly, so we check if previous click hasn't expired yet)
execute if score @s mgs.pending_clicks matches 0.. run scoreboard players set @s mgs.held_click 1
execute if score @s mgs.pending_clicks matches ..-1 run scoreboard players set @s mgs.held_click 0

# Revoke advancement and reset right click
advancement revoke @s only mgs:v5.0.0/right_click
advancement revoke @s only mgs:v5.0.0/alt_right_click
scoreboard players reset @s mgs.right_click
scoreboard players reset @s mgs.alt_right_click

# Set pending clicks (gives ~6 tick window for next click to be considered "held")
scoreboard players set @s mgs.pending_clicks 4

