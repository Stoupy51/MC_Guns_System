
#> mgs:v5.4.1/zombies/ability_menu
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/set_passive_1
#			mgs:v5.4.1/zombies/perks/set_passive_2
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
scoreboard players set #dialog_shown mgs.data 1
dialog show @s mgs:v5.4.1/zombies/ability

