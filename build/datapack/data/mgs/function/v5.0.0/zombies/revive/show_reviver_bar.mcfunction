
#> mgs:v5.0.0/zombies/revive/show_reviver_bar
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick [ at @s ]
#

# Check if reviver has Quick Revive perk
execute if entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.0/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.0/zombies/revive/show_reviver_bar_normal

