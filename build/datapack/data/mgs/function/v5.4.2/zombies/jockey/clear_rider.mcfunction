
#> mgs:v5.4.2/zombies/jockey/clear_rider
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/on_zombie_dying
#

execute on passengers if entity @s[tag=mgs.zb_jockey_rider] run function mgs:v5.4.2/zombies/jockey/remove_rider

