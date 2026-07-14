
#> mgs:v5.1.0/zombies/revive/show_reviver_bar
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick [ at @s ]
#

# #rv_reviver_disp holds the downed player's revive progress (snapshotted in downed_tick while
# @s was the downed player — the reviver cannot re-select them: they spectate a camera entity
# that sits outside the revive range, which used to make this display a stuck "0").
# Convert ticks to seconds for display: sec = p/20, tenth = (p%20)/2
scoreboard players operation #rv_rev_sec mgs.data = #rv_reviver_disp mgs.data
scoreboard players operation #rv_rev_sec mgs.data /= #20 mgs.data
scoreboard players operation #rv_rev_tenth mgs.data = #rv_reviver_disp mgs.data
scoreboard players operation #rv_rev_tenth mgs.data %= #20 mgs.data
scoreboard players operation #rv_rev_tenth mgs.data /= #2 mgs.data

# Check if reviver has Quick Revive perk
execute if entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.1.0/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.1.0/zombies/revive/show_reviver_bar_normal

