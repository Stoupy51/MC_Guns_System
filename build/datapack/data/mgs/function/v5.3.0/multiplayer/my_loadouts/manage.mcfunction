
#> mgs:v5.3.0/multiplayer/my_loadouts/manage
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/player/config/process
#

scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 80000
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.3.0/multiplayer/my_loadouts/manage_find

