
#> mgs:v5.1.0/zombies/passive_ability_menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#			mgs:v5.1.0/zombies/preload_complete [ as @a[scores={mgs.zb.in_game=1}] ]
#

# Zonweeb variant only
execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
# Show the passive selection dialog (ability dialog is shown after)
dialog show @s mgs:v5.1.0/zombies/passive_ability

