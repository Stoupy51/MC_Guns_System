
#> mgs:v5.3.0/zombies/passive_ability_menu
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/player/config/process
#			mgs:v5.3.0/zombies/preload_complete [ as @a[scores={mgs.zb.in_game=1}] ]
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
# The ability dialog follows.
scoreboard players set #dialog_shown mgs.data 1
dialog show @s mgs:v5.3.0/zombies/passive_ability

