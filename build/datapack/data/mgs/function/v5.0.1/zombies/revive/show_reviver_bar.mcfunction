
#> mgs:v5.0.1/zombies/revive/show_reviver_bar
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/revive/downed_tick [ at @s ]
#

# Resolve the nearest downed player's revive progress into a stable fake-player holder. A selector
# used as a score component's "name" does not reliably resolve in the actionbar packet (it rendered
# blank -> "/30t"), so we read the value here and display the holder instead.
execute store result score #rv_reviver_disp mgs.data run scoreboard players get @p[tag=mgs.downed_spectator,sort=nearest,distance=..2.5] mgs.zb.revive_p

# Check if reviver has Quick Revive perk
execute if entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.1/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.1/zombies/revive/show_reviver_bar_normal

