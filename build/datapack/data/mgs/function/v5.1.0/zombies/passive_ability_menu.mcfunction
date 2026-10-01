
#> mgs:v5.1.0/zombies/passive_ability_menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#			mgs:v5.1.0/zombies/preload_complete [ as @a[scores={mgs.zb.in_game=1}] ]
#

execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
# The ability dialog follows.
dialog show @s mgs:v5.1.0/zombies/passive_ability

