
#> mgs:v5.1.0/zombies/ability_menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/set_passive_1
#			mgs:v5.1.0/zombies/perks/set_passive_2
#

# Zonweeb variant only
execute unless data storage mgs:zombies game{variant:"zonweeb"} run return fail
# Show the ability selection dialog
dialog show @s mgs:v5.1.0/zombies/ability

