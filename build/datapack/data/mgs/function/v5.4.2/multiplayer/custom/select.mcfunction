
#> mgs:v5.4.2/multiplayer/custom/select
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/process
#

# id = trigger - 10000
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 10000

# A custom loadout is a negative mp.class.
scoreboard players operation @s mgs.mp.class = #loadout_id mgs.data
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

# For the notification.
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.4.2/multiplayer/custom/find_and_notify

