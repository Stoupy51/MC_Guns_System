
#> mgs:v5.0.0/player/set_pending_clicks
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.0.0/right_click
#

# Revoke advancement
advancement revoke @s only mgs:v5.0.0/right_click

# Detect if player is holding right-click (vs single tap)
# If pending_clicks >= 0, means it was still positive from previous tick (holding)
execute if score @s mgs.pending_clicks matches 0.. run scoreboard players set @s mgs.held_click 1
execute if score @s mgs.pending_clicks matches ..-1 run scoreboard players set @s mgs.held_click 0

# Check if we're mid-burst (burst started but not yet complete)
scoreboard players set #is_mid_burst mgs.data 0
execute if score @s mgs.burst_count matches 1.. run function mgs:v5.0.0/utils/copy_gun_data
execute if score @s mgs.burst_count matches 1.. if data storage mgs:gun all.stats{fire_mode:"burst"} run function mgs:v5.0.0/player/check_mid_burst

# Set pending clicks logic:
# - If mid-burst: always add (to maintain burst sequence)
# - Otherwise: set to 1 (normal behavior, will trigger held detection next tick if still holding)
execute if score #is_mid_burst mgs.data matches 1 run scoreboard players add @s mgs.pending_clicks 1
execute unless score #is_mid_burst mgs.data matches 1 run scoreboard players set @s mgs.pending_clicks 1

