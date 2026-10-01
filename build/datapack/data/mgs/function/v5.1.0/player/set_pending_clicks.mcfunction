
#> mgs:v5.1.0/player/set_pending_clicks
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.1.0/right_click
#			mgs:v5.1.0/player/set_pending_clicks_entity
#

advancement revoke @s only mgs:v5.1.0/right_click

# pending_clicks still >= 0 from last tick means the button is held.
execute if score @s mgs.pending_clicks matches 0.. run scoreboard players set @s mgs.held_click 1
execute if score @s mgs.pending_clicks matches ..-1 run scoreboard players set @s mgs.held_click 0

# A negative pending_clicks with a partial burst means the burst was interrupted (an auto-reload mid-burst);
# without this reset the mid-burst path keeps adding to a very negative count and the weapon never fires again.
execute if score @s mgs.pending_clicks matches ..-1 run scoreboard players set @s mgs.burst_count 0

scoreboard players set #is_mid_burst mgs.data 0
execute if score @s mgs.burst_count matches 1.. run function mgs:v5.1.0/utils/copy_gun_data
execute if score @s mgs.burst_count matches 1.. if data storage mgs:gun all.stats{fire_mode:"burst"} run function mgs:v5.1.0/player/check_mid_burst

# Mid-burst: add, to keep the burst going; otherwise set to 1 (held detection follows next tick if still held).
execute if score #is_mid_burst mgs.data matches 1 run scoreboard players add @s mgs.pending_clicks 1
execute unless score #is_mid_burst mgs.data matches 1 run scoreboard players set @s mgs.pending_clicks 1

